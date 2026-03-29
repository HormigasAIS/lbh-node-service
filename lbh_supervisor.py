#!/usr/bin/env python3
import os, subprocess, socket, json, time

BASE = os.path.expanduser("~/hormigasais-lab/lbh-node-service")
STATUS_FILE = os.path.join(BASE, "nodo_status.json")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally: s.close()
    return ip

def is_running(process_name):
    return subprocess.getoutput(f"pgrep -f '{process_name}'").strip() != ""

def ensure_process(name, cmd):
    if not is_running(name):
        subprocess.Popen(cmd, shell=True)
        return "started"
    return "running"

ip = get_ip()
status = {
    "node_id": "A16",
    "role": "master",
    "ip": ip,
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "services": {
        "gitea": ensure_process("gitea", "nohup gitea web -c ~/gitea/custom/conf/app.ini > /dev/null 2>&1 &"),
        "lbh_api": ensure_process("lbh_api.py", f"cd {BASE} && nohup python3 lbh_api.py > lbh_api.log 2>&1 &"),
        "dashboard": ensure_process("http.server 8080", f"nohup python3 -m http.server 8080 --bind {ip} --directory {BASE} > {BASE}/dashboard_web.log 2>&1 &")
    }
}

with open(STATUS_FILE, "w") as f:
    json.dump(status, f, indent=4)
print("🧠 SÉFORIS: Identidad A16-Master confirmada.")
