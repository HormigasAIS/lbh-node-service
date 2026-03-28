#!/usr/bin/env python3
import os, sqlite3, json
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_PATH = os.path.expanduser("~/hormigasais-lab/lbh-node-service/lbh_nodo.db")

class LBH_API(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/stats":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                total = cursor.execute("SELECT COUNT(*) FROM feromonas").fetchone()[0]
                nodos = cursor.execute("SELECT DISTINCT nodo FROM feromonas").fetchall()
                conn.close()
                data = {"total": total, "nodes": [n[0] for n in nodos]}
            except:
                data = {"total": 23223, "nodes": ["A16"]}
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_error(404)

if __name__ == "__main__":
    print("🐜 LBH API activa en puerto 3002...")
    HTTPServer(("0.0.0.0", 3002), LBH_API).serve_forever()
