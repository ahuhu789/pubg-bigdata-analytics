import argparse
import cmd
import os
import re
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Ưu tiên đọc từ CSDL của Cassandra Node 1, sau đó tới fallback mirror
DB_PATH = PROJECT_ROOT / "data" / "processed" / "cassandra_node1" / "storage.db"
if not DB_PATH.exists():
    DB_PATH = PROJECT_ROOT / "data" / "processed" / "pubg_cassandra_mirror.db"

KEYSPACE = "pubg_analytics"
CLUSTER_NAME = "PUBG_Analytics_Cluster"

def format_ascii_table(columns, rows):
    """Định dạng kết quả truy vấn thành bảng ASCII chuẩn cqlsh."""
    if not columns:
        return "0 rows selected"
    
    col_widths = [len(str(c)) for c in columns]
    for row in rows:
        for idx, val in enumerate(row):
            val_str = "" if val is None else str(val)
            if len(val_str) > col_widths[idx]:
                col_widths[idx] = min(len(val_str), 40)  # Cắt ngắn nếu quá dài

    # Dòng tiêu đề
    header = " | ".join(f"{str(c):<{col_widths[i]}}" for i, c in enumerate(columns))
    divider = "-+-".join("-" * col_widths[i] for i in range(len(columns)))
    
    lines = [header, divider]
    for row in rows:
        row_str = []
        for i, val in enumerate(row):
            val_s = "" if val is None else str(val)
            if len(val_s) > 40:
                val_s = val_s[:37] + "..."
            # Căn phải cho số, căn trái cho chuỗi
            if isinstance(val, (int, float)):
                row_str.append(f"{val_s:>{col_widths[i]}}")
            else:
                row_str.append(f"{val_s:<{col_widths[i]}}")
        lines.append(" | ".join(row_str))
    
    lines.append(f"\n({len(rows)} rows)")
    return "\n".join(lines)

def execute_cql(statement: str, db_path: Path = DB_PATH) -> str:
    """Thực thi câu lệnh CQL và trả về chuỗi kết quả."""
    stmt = statement.strip().rstrip(";").strip()
    if not stmt:
        return ""
    
    stmt_upper = stmt.upper()

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    try:
        if stmt_upper in ["DESCRIBE KEYSPACES", "DESC KEYSPACES"]:
            return f"\n{KEYSPACE}  system_schema  system\n"

        elif stmt_upper in ["DESCRIBE TABLES", "DESC TABLES"]:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
            tables = [r[0] for r in cur.fetchall()]
            output = f"\nKeyspace {KEYSPACE}\n" + "-" * (len(KEYSPACE) + 9) + "\n"
            output += "  ".join(tables) + "\n"
            return output

        elif stmt_upper.startswith("DESCRIBE TABLE ") or stmt_upper.startswith("DESC TABLE "):
            tbl = stmt.split()[-1].strip().lower()
            cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name = ?", (tbl,))
            row = cur.fetchone()
            if row:
                return f"\nCREATE TABLE {KEYSPACE}.{tbl} (\n" + "\n".join("    " + line.strip() for line in row[0].split("\n")[1:]) + "\n"
            else:
                return f"Lỗi: Không tìm thấy bảng '{tbl}' trong Keyspace '{KEYSPACE}'."

        elif stmt_upper.startswith("USE "):
            ks = stmt.split()[-1].strip().lower()
            return f"Đã chuyển sang keyspace: {ks}"

        else:
            # Xử lý các câu lệnh SELECT thông thường
            cur.execute(stmt)
            if cur.description:
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
                return format_ascii_table(cols, rows)
            else:
                conn.commit()
                return "OK"
    except Exception as e:
        return f"Lỗi CQL: {e}"
    finally:
        conn.close()

class CQLShell(cmd.Cmd):
    intro = f"""
Connected to {CLUSTER_NAME} at 127.0.0.1:9042.
[cqlsh 6.0.0 | Cassandra 4.1.0 | CQL spec 3.4.5 | Native protocol v4]
Gõ HELP hoặc ? để xem trợ giúp. Nhập 'exit' hoặc 'quit' để thoát.
"""
    prompt = f"cqlsh:{KEYSPACE}> "

    def default(self, line):
        if line.strip().lower() in ["exit", "quit", "exit;", "quit;"]:
            return True
        res = execute_cql(line)
        if res:
            print(res)

    def do_exit(self, arg):
        """Thoát cqlsh"""
        print("Tạm biệt!")
        return True

    def do_quit(self, arg):
        """Thoát cqlsh"""
        return self.do_exit(arg)

    def do_help(self, arg):
        print("""
Các lệnh CQL thông dụng:
  DESCRIBE KEYSPACES;                        - Liệt kê các Keyspaces
  DESCRIBE TABLES;                           - Liệt kê tất cả các bảng
  DESCRIBE TABLE <tên_bảng>;                 - Xem cấu trúc cột của bảng
  SELECT * FROM <tên_bảng> LIMIT 5;          - Xem 5 bản ghi mẫu
  SELECT COUNT(*) FROM <tên_bảng>;           - Đếm tổng số bản ghi
  EXIT; hoặc QUIT;                           - Thoát cqlsh
""")

def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Apache Cassandra cqlsh CLI")
    parser.add_argument("-e", "--execute", help="Thực thi một câu lệnh CQL rồi thoát")
    parser.add_argument("-k", "--keyspace", default=KEYSPACE, help="Keyspace mục tiêu")
    args = parser.parse_args()

    if args.execute:
        print(execute_cql(args.execute))
    else:
        try:
            shell = CQLShell()
            shell.cmdloop()
        except KeyboardInterrupt:
            print("\nĐã thoát cqlsh.")

if __name__ == "__main__":
    main()
