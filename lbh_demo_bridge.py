#!/usr/bin/env python3
import os, json, urllib.request, time

# ── RUTAS DE INFRAESTRUCTURA ──────────────────────────
BASE = os.path.expanduser("~/hormigasais-lab/lbh-node-service")
SANDBOX = os.path.expanduser("~/hormigasais-sandbox/sandbox_status.json")
OUTPUT = os.path.join(BASE, "demo_state.json")

# URL del Nodo Maestro (Ajustar si cambia el puerto)
API_URL = "http://127.0.0.1:3002/api/stats"

def get_api_stats():
    try:
        with urllib.request.urlopen(API_URL, timeout=1.5) as r:
            return json.loads(r.read().decode())
    except:
        return {"total": 0, "nodes": []}

def get_sandbox():
    try:
        if os.path.exists(SANDBOX):
            with open(SANDBOX) as f:
                return json.load(f)
        return {"event": "WAITING", "health": "SCANNING", "recovery_time": 0}
    except:
        return {"event": "ERROR", "health": "OFFLINE", "recovery_time": 0}

def build_demo():
    api = get_api_stats()
    sandbox = get_sandbox()

    data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "production": {
            "total": api.get("total", 0),
            "nodes": len(api.get("nodes", [])) if isinstance(api.get("nodes"), list) else 0
        },
        "sandbox": {
            "event": sandbox.get("event", "N/A"),
            "health": sandbox.get("health", "UNKNOWN"),
            "recovery_time": sandbox.get("recovery_time", 0)
        }
    }

    with open(OUTPUT, "w") as f:
        json.dump(data, f, indent=4)

    print(f"🧠 [BRIDGE] Demo State Sincronizado: {data['timestamp']}")
    print(f"📊 Sandbox: {data['sandbox']['event']} | Recovery: {data['sandbox']['recovery_time']}s")

if __name__ == "__main__":
    build_demo()
