"""
APACHE CASSANDRA WORKER NODE (MÁY 2: 192.168.1.23)
==================================================
Tệp này chạy trên Máy 2 để kết nối vào Seed Node (Máy 1: 192.168.1.175),
tạo thành cụm Apache Cassandra phân tán 2 máy.
"""

import os
import sys
import socket
import time
from pathlib import Path

# Thêm thư mục hiện tại vào sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.cassandra_cluster_node import CassandraNode

SEED_IP = "192.168.1.175"
PORT = 9042

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    # Tự động lấy IP cục bộ của Máy 2
    my_ip = "192.168.1.23"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((SEED_IP, 80))
        my_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass

    print("=" * 68)
    print("  KHỞI ĐỘNG CASSANDRA WORKER NODE (MÁY 2)")
    print(f"  Địa chỉ IP Máy 2 : {my_ip}:{PORT}")
    print(f"  Kết nối Seed (Máy 1): {SEED_IP}:{PORT}")
    print(f"  Cụm CSDL        : PUBG_Analytics_Cluster")
    print("=" * 68)
    print(">>> Đang thiết lập kết nối Gossip với Máy 1...")

    node = CassandraNode(
        node_ip=my_ip,
        port=PORT,
        role="worker",
        seed_ip=SEED_IP
    )
    node.start()

if __name__ == "__main__":
    main()
