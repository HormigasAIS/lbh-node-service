#!/usr/bin/env python3
import os, json, time, urllib.request, socket, sqlite3
from lbh_narrator_patch import build_narrative

BASE = os.path.expanduser("~/hormigasais-lab/lbh-node-service")
SANDBOX = os.path.expanduser("~/hormigasais-sandbox")

OUT = os.path.join(BASE, "demo_state.json")
SANDBOX_FILE = os.path.join(SANDBOX, "sandbox_status.json")

os.makedirs(BASE, exist_ok=True)

# ── IP DEL NODO ──────────────────────────
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

IP_EXTERNA = get_ip()

# ── MÉTRICAS LBH ──────────────────────────
def get_api_data():
    try:
        with urllib.request.urlopen("http://127.0.0.1:8100/metrics", timeout=1.5) as r:
            m = json.loads(r.read().decode())
        return {
            "total": m.get("total_feromonas", 0),
            "nodes": ["LBH_NODE"] * m.get("nodos_activos", 0),
            "status": "ONLINE"
        }
    except:
        return {"total": 0, "nodes": [], "status": "OFFLINE"}

# ── ÚLTIMA FEROMONA (NARRATIVA) ──────────────────────
def get_last_feromona():
    try:
        db = os.path.expanduser("~/hormigasais-core/db/lbh_nodo.db")
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT id, nodo, payload, firma, ts FROM feromonas ORDER BY id DESC LIMIT 1").fetchone()
        conn.close()
        if not row: return {}
        data = dict(row)
        data["fecha_legible"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data["ts"]))
        return data
    except:
        return {}

# ── SANDBOX EVOLUTIVO ──────────────────────────
def get_sandbox():
    if os.path.exists(SANDBOX_FILE):
        try:
            with open(SANDBOX_FILE) as f: return json.load(f)
        except: pass
    return {"event": "WAITING", "health": "UNKNOWN", "recovery_time": 0}

# ── BUILD NARRATIVO ──────────────────────────
def build():
    api = get_api_data()
    sandbox = get_sandbox()
    ultima = get_last_feromona()

    nodos_lista = api.get("nodes", [])
    if not isinstance(nodos_lista, list): nodos_lista = []
    
    demo = {
        "node": {
            "ip": IP_EXTERNA,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "ONLINE" if api.get("status") != "OFFLINE" else "CORE_OFFLINE"
        },
        "real_data": {
            "total_feromonas": api.get("total", 0),
            "nodos_conteo": len(nodos_lista),
            "nodos_activos": nodos_lista,
            "ultima_feromona": ultima
        },
        "sandbox": {
            "evento": sandbox.get("event", "N/A"),
            "health": sandbox.get("health", "UNKNOWN"),
            "recovery_time": sandbox.get("recovery_time", 0)
        }
    }

    # 🧠 PARCHE NARRATIVO: Integración del narrador modular
    demo = build_narrative(demo)
    
    with open(OUT, "w") as f:
        json.dump(demo, f, indent=4)
    print("🧠 [LBH v0.3] capa humana añadida | demo listo para UI pública")

if __name__ == "__main__":
    build()
