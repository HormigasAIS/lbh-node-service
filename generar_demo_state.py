#!/usr/bin/env python3
import os, json, time, urllib.request, socket

# ── RUTAS DE INFRAESTRUCTURA ──────────────────────────
BASE = os.path.expanduser("~/hormigasais-lab/lbh-node-service")
SANDBOX = os.path.expanduser("~/hormigasais-sandbox")

OUT = os.path.join(BASE, "demo_state.json")
SANDBOX_FILE = os.path.join(SANDBOX, "sandbox_status.json")

# Asegurar que el directorio base existe
os.makedirs(BASE, exist_ok=True)

# ── DETECTAR IP (Soberanía de Red) ────────────────────
def get_ip():
    try:
        # Usamos 8.8.8.8 para identificar la interfaz activa en Termux
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

IP_EXTERNA = get_ip()

# ── DATOS REALES (API Localhost) ──────────────────────
def get_api_data():
    try:
        # IMPORTANTE: Usamos 127.0.0.1 para evitar latencia de red interna
        with urllib.request.urlopen("http://127.0.0.1:3002/api/stats", timeout=1.5) as r:
            return json.loads(r.read().decode())
    except:
        return {"total": 0, "nodes": [], "status": "OFFLINE"}

# ── DATOS SANDBOX (Evolución) ──────────────────────────
def get_sandbox():
    if os.path.exists(SANDBOX_FILE):
        try:
            with open(SANDBOX_FILE) as f:
                return json.load(f)
        except:
            pass
    return {
        "event": "WAITING",
        "health": "UNKNOWN",
        "recovery_time": 0
    }

# ── GENERAR ESTADO UNIFICADO ──────────────────────────
def build():
    api = get_api_data()
    sandbox = get_sandbox()
    
    # Validar lista de nodos para evitar errores de conteo
    nodos_lista = api.get("nodes", [])
    if not isinstance(nodos_lista, list):
        nodos_lista = []

    demo = {
        "node": {
            "ip": IP_EXTERNA,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "ONLINE" if api.get("status") != "OFFLINE" else "CORE_OFFLINE"
        },
        "real_data": {
            "total_feromonas": api.get("total", 0),
            "nodos_conteo": len(nodos_lista),
            "nodos_activos": nodos_lista
        },
        "sandbox": {
            "evento": sandbox.get("event", "N/A"),
            "salud": sandbox.get("health", "UNKNOWN"),
            "tiempo_recuperacion": sandbox.get("recovery_time", 0)
        }
    }

    # Guardar estado para el Dashboard
    with open(OUT, "w") as f:
        json.dump(demo, f, indent=4)

    print(f"🧠 [LBH-BRIDGE] demo_state.json actualizado | IP: {IP_EXTERNA} | Evento: {demo['sandbox']['evento']}")

if __name__ == "__main__":
    build()
