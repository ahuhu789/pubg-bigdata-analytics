import argparse
import json
import socket
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def format_bytes(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:3.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

def get_cluster_status(host: str = "127.0.0.1", port: int = 9042) -> dict:
    """Truy vấn bảng trạng thái cụm từ cổng 9042."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((host, port))
        s.sendall(json.dumps({"type": "NODETOOL_STATUS"}).encode("utf-8"))
        data = s.recv(65536)
        s.close()
        if data:
            return json.loads(data.decode("utf-8"))
    except Exception:
        pass

    # Nếu không kết nối qua socket, đọc tệp trạng thái lưu trên đĩa
    status_file = PROJECT_ROOT / "data" / "processed" / "cassandra_cluster_status.json"
    if status_file.exists():
        try:
            with open(status_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def print_nodetool_status(data: dict):
    cluster_name = data.get("cluster_name", "PUBG_Analytics_Cluster")
    dc = data.get("datacenter", "datacenter1")
    nodes = data.get("nodes", [])

    print(f"Datacenter: {dc}")
    print("=" * 23)
    print("Status=Up/Down")
    print("|/ State=Normal/Leaving/Joining/Moving")
    print(f"{'--':<3} {'Address':<17} {'Load':<10} {'Tokens':<7} {'Owns':<8} {'Host ID':<28} {'Rack'}")

    up_count = sum(1 for n in nodes if n.get("status") == "UP")
    total_nodes = len(nodes)
    owns_pct = f"{100.0 / max(total_nodes, 1):.1f}%"

    for n in sorted(nodes, key=lambda x: x.get("ip", "")):
        st_code = "UN" if n.get("status") == "UP" else "DN"
        ip = n.get("ip", "127.0.0.1")
        load = format_bytes(n.get("load_bytes", 0))
        tokens = str(n.get("tokens", 256))
        host_id = n.get("host_id", f"node-{ip}")
        rack = n.get("rack", "rack1")
        role = f" ({n.get('role', '')})" if n.get("role") else ""
        print(f"{st_code:<3} {ip:<17} {load:<10} {tokens:<7} {owns_pct:<8} {host_id:<28} {rack}{role}")

    print()
    print(f">>> Cụm: {cluster_name} | Tổng Nodes: {total_nodes} | Đang hoạt động (UP): {up_count}")

def main():
    parser = argparse.ArgumentParser(description="Apache Cassandra nodetool CLI tool")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "ring", "info"], help="Lệnh thực thi")
    parser.add_argument("-H", "--host", default="127.0.0.1", help="Địa chỉ host")
    parser.add_argument("-p", "--port", type=int, default=9042, help="Cổng kết nối")
    args = parser.parse_args()

    data = get_cluster_status(args.host, args.port)
    if not data or not data.get("nodes"):
        print("Lỗi: Không thể kết nối tới Apache Cassandra Node tại {}:{}".format(args.host, args.port))
        print("Vui lòng đảm bảo dịch vụ đã khởi động bằng: python scripts/cassandra_cluster_node.py")
        sys.exit(1)

    if args.command in ["status", "ring"]:
        print_nodetool_status(data)
    elif args.command == "info":
        print(f"Cluster: {data.get('cluster_name')}")
        print(f"Datacenter: {data.get('datacenter')}")
        print(f"Total Nodes: {len(data.get('nodes', []))}")

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
