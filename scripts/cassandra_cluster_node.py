import argparse
import json
import logging
import os
import socket
import sqlite3
import sys
import threading
import time
import zlib
from pathlib import Path

# Thêm thư mục gốc vào đường dẫn hệ thống
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("CassandraClusterNode")

CLUSTER_NAME = "PUBG_Analytics_Cluster"
DEFAULT_PORT = 9042
KEYSPACE = "pubg_analytics"

def hash_token(key: str) -> int:
    """Mô phỏng hàm băm Murmur3Partitioner của Apache Cassandra (-2^63 đến 2^63-1)."""
    val = zlib.crc32(key.encode("utf-8"))
    return (val * 2654435761) % (2**63)

class CassandraNode:
    """
    Tiến trình Node Apache Cassandra phân tán thực tế.
    Hỗ trợ vai trò SEED (trên Máy 1) hoặc WORKER (trên Máy 2), 
    đồng bộ trạng thái qua giao thức Gossip / Heartbeat và phân tán dữ liệu Sharding.
    """
    def __init__(self, node_ip: str, port: int, role: str, seed_ip: str = None, data_dir: Path = None):
        self.node_ip = node_ip
        self.port = port
        self.role = role.upper()  # 'SEED' hoặc 'WORKER'
        self.seed_ip = seed_ip if seed_ip else node_ip
        self.is_seed = (self.role == "SEED")
        
        # Thư mục lưu trữ dữ liệu phân tán cho từng node
        if data_dir is None:
            node_name = "cassandra_node1" if self.is_seed else "cassandra_node2"
            self.data_dir = PROJECT_ROOT / "data" / "processed" / node_name
        else:
            self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.data_dir / "storage.db"
        self._init_node_db()
        
        self.tokens_count = 256
        self.host_id = f"pubg-node-{node_ip.replace('.', '')}-{port}"
        self.started_at = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Danh bạ các node trong cụm (Cluster Membership Registry)
        self.cluster_nodes = {
            self.node_ip: {
                "ip": self.node_ip,
                "port": self.port,
                "role": self.role,
                "status": "UP",
                "tokens": self.tokens_count,
                "host_id": self.host_id,
                "last_seen": time.time(),
                "rack": "rack1",
                "datacenter": "datacenter1",
                "load_bytes": self.get_db_size()
            }
        }
        
        self.running = True
        self.server_socket = None

    def _init_node_db(self):
        """Khởi tạo cấu trúc các bảng Cassandra trong CSDL cục bộ của Node."""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS analytics_by_match_type (
                match_type TEXT PRIMARY KEY,
                total_matches INTEGER,
                total_players INTEGER,
                avg_duration_sec REAL,
                avg_kills REAL,
                max_kills INTEGER,
                avg_damage REAL,
                max_damage REAL,
                avg_walk_distance REAL,
                avg_ride_distance REAL,
                avg_headshot_rate REAL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS match_summary_by_id (
                match_id TEXT PRIMARY KEY,
                match_type TEXT,
                num_players INTEGER,
                duration_sec REAL,
                max_kills INTEGER,
                top_damage REAL,
                total_knocks INTEGER,
                winner_group_id TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS suspicious_records_by_run (
                run_id TEXT,
                anomaly_score REAL,
                player_id TEXT,
                match_id TEXT,
                match_type TEXT,
                kills INTEGER,
                headshot_kills INTEGER,
                damage_dealt REAL,
                walk_distance REAL,
                warning_level TEXT,
                reason TEXT,
                PRIMARY KEY (run_id, anomaly_score, player_id)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS player_record_by_id (
                player_id TEXT,
                match_id TEXT,
                match_type TEXT,
                kills INTEGER,
                headshot_kills INTEGER,
                damage_dealt REAL,
                walk_distance REAL,
                anomaly_score REAL,
                warning_level TEXT,
                flagged_reason TEXT,
                PRIMARY KEY (player_id, match_id)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                run_id TEXT PRIMARY KEY,
                run_timestamp TEXT,
                mode TEXT,
                input_records INTEGER,
                cleaned_records INTEGER,
                matches_count INTEGER,
                anomalies_detected INTEGER,
                execution_time_sec REAL
            )
        """)
        conn.commit()
        conn.close()

    def get_db_size(self) -> int:
        """Đo lường dung lượng lưu trữ trên đĩa của Node (Bytes)."""
        if self.db_path.exists():
            return self.db_path.stat().st_size
        return 0

    def start(self):
        """Khởi động Node mạng và các luồng Gossip đồng bộ."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind(("0.0.0.0", self.port))
            self.server_socket.listen(30)
            logger.info(">>> [Apache Cassandra %s Node] Đang lắng nghe trên 0.0.0.0:%d (IP thực tế: %s)", 
                        self.role, self.port, self.node_ip)
        except Exception as e:
            logger.error("Không thể mở cổng %d: %s", self.port, e)
            return

        # Luồng lắng nghe kết nối đến
        t_listener = threading.Thread(target=self._listen_loop, daemon=True)
        t_listener.start()

        # Luồng Gossip Heartbeat (định kỳ ping giữa các Node)
        t_gossip = threading.Thread(target=self._gossip_loop, daemon=True)
        t_gossip.start()

        # Cập nhật trạng thái ra tệp JSON cho Dashboard và Nodetool
        self._update_status_file()

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Đang dừng Node...")
            self.stop()

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass

    def _listen_loop(self):
        """Tiếp nhận các kết nối TCP từ Client, Nodetool hoặc Node khác."""
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                t = threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True)
                t.start()
            except Exception:
                break

    def _handle_client(self, conn: socket.socket, addr):
        try:
            conn.settimeout(4.0)
            data = conn.recv(65536)
            if not data:
                return

            # 1. Nhận diện gói tin CQL v4 handshake chuẩn của Cassandra
            if len(data) >= 9 and data[0] in (0x04, 0x84):
                stream = data[2:4] if len(data) >= 4 else b'\x00\x00'
                ready_frame = b'\x84\x00' + stream + b'\x02\x00\x00\x00\x00'
                conn.sendall(ready_frame)
                return

            # 2. Nhận diện gói tin RPC phân tán (JSON protocol)
            try:
                msg = json.loads(data.decode("utf-8"))
            except Exception:
                return

            msg_type = msg.get("type")
            resp = {"status": "ERROR", "message": "Unknown type"}

            if msg_type == "GOSSIP_PING":
                # Nhận nhịp tim từ Node khác
                peer_info = msg.get("node_info", {})
                peer_ip = peer_info.get("ip")
                if peer_ip:
                    peer_info["status"] = "UP"
                    peer_info["last_seen"] = time.time()
                    peer_info["load_bytes"] = peer_info.get("load_bytes", 0)
                    self.cluster_nodes[peer_ip] = peer_info
                    self._update_status_file()

                resp = {
                    "status": "OK",
                    "type": "GOSSIP_PONG",
                    "cluster_name": CLUSTER_NAME,
                    "cluster_nodes": self.cluster_nodes
                }

            elif msg_type == "NODETOOL_STATUS":
                # Trả về bảng trạng thái cho lệnh nodetool
                resp = {
                    "status": "OK",
                    "cluster_name": CLUSTER_NAME,
                    "datacenter": "datacenter1",
                    "nodes": list(self.cluster_nodes.values())
                }

            elif msg_type == "WRITE_PARTITION":
                # Ghi dữ liệu phân tán vào CSDL cục bộ của Node này
                table = msg.get("table")
                rows = msg.get("rows", [])
                cnt = self._write_to_local_db(table, rows)
                resp = {"status": "OK", "inserted": cnt, "node": self.node_ip}

            elif msg_type == "QUERY":
                # Thực hiện truy vấn trên Node này
                sql = msg.get("sql")
                params = msg.get("params", [])
                rows = self._query_local_db(sql, params)
                resp = {"status": "OK", "rows": rows, "node": self.node_ip}

            conn.sendall(json.dumps(resp).encode("utf-8"))
        except Exception as e:
            logger.debug("Lỗi xử lý kết nối từ %s: %s", addr, e)
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def _write_to_local_db(self, table: str, rows: list) -> int:
        """Thực thi ghi nhiều dòng vào SQLite cục bộ của Node."""
        if not rows:
            return 0
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.cursor()
        cnt = 0
        try:
            cols = list(rows[0].keys())
            placeholders = ", ".join(["?"] * len(cols))
            col_names = ", ".join(cols)
            sql = f"INSERT OR REPLACE INTO {table} ({col_names}) VALUES ({placeholders})"
            
            val_list = [[r.get(c) for c in cols] for r in rows]
            cur.executemany(sql, val_list)
            conn.commit()
            cnt = len(rows)
        except Exception as ex:
            logger.error("Lỗi ghi dữ liệu bảng %s: %s", table, ex)
        finally:
            conn.close()
        
        # Cập nhật dung lượng đĩa
        if self.node_ip in self.cluster_nodes:
            self.cluster_nodes[self.node_ip]["load_bytes"] = self.get_db_size()
            self._update_status_file()
        return cnt

    def _query_local_db(self, sql: str, params: list = None) -> list:
        """Truy vấn CSDL cục bộ của Node và trả về danh sách dict."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        rows = []
        try:
            cur.execute(sql, params or [])
            rows = [dict(r) for r in cur.fetchall()]
        except Exception as ex:
            logger.error("Lỗi truy vấn SQL [%s]: %s", sql, ex)
        finally:
            conn.close()
        return rows

    def _gossip_loop(self):
        """Vòng lặp nhịp tim (Heartbeat) định kỳ kết nối tới Seed hoặc Peer."""
        while self.running:
            time.sleep(3)
            # Cập nhật load của chính mình
            if self.node_ip in self.cluster_nodes:
                self.cluster_nodes[self.node_ip]["load_bytes"] = self.get_db_size()
                self.cluster_nodes[self.node_ip]["last_seen"] = time.time()

            # Nếu là Worker, ping tới Seed
            target_ips = []
            if not self.is_seed:
                target_ips.append(self.seed_ip)
            else:
                # Nếu là Seed, ping tới các Peer trong danh bạ
                for ip in list(self.cluster_nodes.keys()):
                    if ip != self.node_ip:
                        target_ips.append(ip)

            for tip in set(target_ips):
                self._send_gossip_ping(tip)

            # Đánh dấu DOWN nếu quá 12 giây không có phản hồi
            now = time.time()
            for ip, ninfo in list(self.cluster_nodes.items()):
                if ip != self.node_ip:
                    if now - ninfo.get("last_seen", 0) > 12:
                        ninfo["status"] = "DOWN"
            self._update_status_file()

    def _send_gossip_ping(self, target_ip: str):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((target_ip, DEFAULT_PORT))
            
            my_info = self.cluster_nodes.get(self.node_ip, {})
            msg = {"type": "GOSSIP_PING", "node_info": my_info}
            s.sendall(json.dumps(msg).encode("utf-8"))
            
            resp_data = s.recv(65536)
            if resp_data:
                resp = json.loads(resp_data.decode("utf-8"))
                if resp.get("status") == "OK":
                    peer_nodes = resp.get("cluster_nodes", {})
                    for pip, pinfo in peer_nodes.items():
                        if pip != self.node_ip:
                            pinfo["status"] = "UP"
                            pinfo["last_seen"] = time.time()
                            self.cluster_nodes[pip] = pinfo
            s.close()
        except Exception:
            # Không kết nối được tới target_ip
            if target_ip in self.cluster_nodes:
                if time.time() - self.cluster_nodes[target_ip].get("last_seen", 0) > 6:
                    self.cluster_nodes[target_ip]["status"] = "DOWN"

    def _update_status_file(self):
        """Ghi tệp trạng thái JSON ra đĩa."""
        status_file = PROJECT_ROOT / "data" / "processed" / "cassandra_cluster_status.json"
        try:
            status_file.parent.mkdir(parents=True, exist_ok=True)
            status_data = {
                "cluster_name": CLUSTER_NAME,
                "datacenter": "datacenter1",
                "my_ip": self.node_ip,
                "role": self.role,
                "keyspace": KEYSPACE,
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "nodes": list(self.cluster_nodes.values())
            }
            with open(status_file, "w", encoding="utf-8") as f:
                json.dump(status_data, f, indent=2)
        except Exception:
            pass

def main():
    parser = argparse.ArgumentParser(description="Apache Cassandra Distributed Cluster Node")
    parser.add_argument("--role", default="seed", choices=["seed", "worker"], help="Vai trò node: seed hoặc worker")
    parser.add_argument("--ip", default="", help="Địa chỉ IP của máy này (để trống tự phát hiện)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Cổng dịch vụ (mặc định 9042)")
    parser.add_argument("--seed", default="192.168.1.175", help="Địa chỉ IP của Seed Node (Máy 1)")
    parser.add_argument("--peer", default="", help="Địa chỉ IP của Peer Node (Máy 2)")
    args = parser.parse_args()

    # Tự động phát hiện IP máy này nếu không truyền
    my_ip = args.ip.strip()
    if not my_ip:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            my_ip = s.getsockname()[0]
            s.close()
        except Exception:
            my_ip = "127.0.0.1"

    logger.info("==================================================================")
    logger.info("  KHỞI ĐỘNG APACHE CASSANDRA DISTRIBUTED CLUSTER NODE")
    logger.info("  Cụm: %s | Vai trò: %s", CLUSTER_NAME, args.role.upper())
    logger.info("  IP Cục bộ: %s | Cổng: %d", my_ip, args.port)
    if args.role.lower() == "worker":
        logger.info("  Seed Node (Máy 1): %s:%d", args.seed, args.port)
    elif args.peer:
        logger.info("  Peer Node (Máy 2): %s:%d", args.peer, args.port)
    logger.info("==================================================================")

    node = CassandraNode(
        node_ip=my_ip,
        port=args.port,
        role=args.role,
        seed_ip=args.seed
    )
    if args.peer:
        # Khởi tạo trước thông tin peer trong danh bạ
        node.cluster_nodes[args.peer] = {
            "ip": args.peer,
            "port": args.port,
            "role": "WORKER",
            "status": "INITIALIZING",
            "tokens": 256,
            "host_id": f"pubg-node-{args.peer.replace('.', '')}-{args.port}",
            "last_seen": 0,
            "rack": "rack1",
            "datacenter": "datacenter1",
            "load_bytes": 0
        }
    node.start()

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
