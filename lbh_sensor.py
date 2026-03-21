#!/usr/bin/env python3
"""
LBH Sensor Daemon — sensores fisicos Android → feromonas LBH
Fix: sig 64 hex + subtype + BSSID/IP/RSSI + daemon loop
CLHQ / HormigasAIS 2026
"""

import json, os, subprocess, time, urllib.request, hashlib, hmac, signal, sys

ENDPOINT   = "http://localhost:8100/v1/lbh/validate"
NODO       = "LBH-DDCD"
SECRET_KEY = "hormigasais-soberano-2026"
INTERVALO  = 30  # segundos entre lecturas
LOG_FILE   = os.path.expanduser(
    "~/hormigasais-lab/lbh-node-service/sensor.log")

running = True

def signal_handler(sig, frame):
    global running
    print("\n🐜 Sensor daemon detenido")
    running = False
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ─────────────────────────────────────────
# FIRMA — 64 hex completo
# ─────────────────────────────────────────
def firmar(data):
    msg = json.dumps(data, sort_keys=True)
    return hmac.new(
        SECRET_KEY.encode(), msg.encode(), hashlib.sha256
    ).hexdigest()  # 64 hex — sin truncar

# ─────────────────────────────────────────
# LOG SOBERANO
# ─────────────────────────────────────────
def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{ts}] 🐜 {msg}"
    print(linea)
    with open(LOG_FILE, "a") as f:
        f.write(linea + "\n")

# ─────────────────────────────────────────
# SENSORES — con subtype
# ─────────────────────────────────────────
def leer_bateria():
    try:
        r = subprocess.run(
            ["termux-battery-status"],
            capture_output=True, text=True, timeout=5)
        data = json.loads(r.stdout)
        return {
            "type":        "SENSOR",
            "subtype":     "BATTERY",
            "health":      data.get("health", "?"),
            "plugged":     data.get("plugged", "?"),
            "temperature": data.get("temperature", 0),
            "percentage":  data.get("percentage", 0),
            "ts":          int(time.time())
        }
    except Exception as e:
        return {"type": "SENSOR", "subtype": "BATTERY", "error": str(e)}

def leer_wifi():
    try:
        r = subprocess.run(
            ["termux-wifi-connectioninfo"],
            capture_output=True, text=True, timeout=5)
        data = json.loads(r.stdout)
        return {
            "type":    "SENSOR",
            "subtype": "WIFI",
            "bssid":   data.get("bssid", "?"),
            "ip":      data.get("ip", "?"),
            "rssi":    data.get("rssi", 0),
            "link_speed": data.get("link_speed_mbps", 0),
            "ts":      int(time.time())
        }
    except Exception as e:
        return {"type": "SENSOR", "subtype": "WIFI", "error": str(e)}

# ─────────────────────────────────────────
# ENVIAR FEROMONA
# ─────────────────────────────────────────
def enviar_feromona(sensor_data):
    subtype = sensor_data.get("subtype", "UNKNOWN")
    nodo_id = f"{NODO}:{subtype}"

    # Firma soberana del sensor
    sig_sensor = firmar(sensor_data)

    payload = json.dumps({
        "url":  "https://raw.githubusercontent.com/HormigasAIS/LBH-Net/main/README.md",
        "nodo": nodo_id,
        "type": "SENSOR",
        "ttl":  INTERVALO * 2
    }).encode()

    req = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            resp = json.loads(r.read())
            feromona = resp.get("feromona", {})
            return {
                "ok":      True,
                "estado":  feromona.get("estado", "?"),
                "sig_lbh": feromona.get("sig", "?"),
                "sig_sensor": sig_sensor[:16] + "...",
                "sig_sensor_full": sig_sensor
            }
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ─────────────────────────────────────────
# CICLO DAEMON
# ─────────────────────────────────────────
def ciclo():
    log(f"iniciando lectura — nodo: {NODO}")

    # Batería
    bat = leer_bateria()
    log(f"BATTERY temp:{bat.get('temperature')}°C "
        f"pct:{bat.get('percentage')}% "
        f"health:{bat.get('health')}")
    r = enviar_feromona(bat)
    if r["ok"]:
        log(f"BATTERY → feromona OK | "
            f"sig_lbh:{r['sig_lbh']} | "
            f"sig_sensor:{r['sig_sensor']}")
    else:
        log(f"BATTERY → error: {r.get('error')}")

    # WiFi
    wifi = leer_wifi()
    log(f"WIFI ip:{wifi.get('ip')} "
        f"rssi:{wifi.get('rssi')}dBm "
        f"bssid:{wifi.get('bssid')}")
    r = enviar_feromona(wifi)
    if r["ok"]:
        log(f"WIFI → feromona OK | "
            f"sig_lbh:{r['sig_lbh']} | "
            f"sig_sensor:{r['sig_sensor']}")
    else:
        log(f"WIFI → error: {r.get('error')}")

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    print("═" * 52)
    print("🐜 LBH Sensor Daemon")
    print(f"   nodo:      {NODO}")
    print(f"   endpoint:  {ENDPOINT}")
    print(f"   intervalo: {INTERVALO}s")
    print(f"   sig:       HMAC-SHA256 64 hex")
    print(f"   subtypes:  BATTERY | WIFI")
    print(f"   log:       sensor.log")
    print("═" * 52)
    print("Ctrl+C para detener\n")

    ciclo_num = 0
    while running:
        ciclo_num += 1
        print(f"\n── Ciclo {ciclo_num} ──────────────────────────")
        ciclo()
        if running:
            log(f"esperando {INTERVALO}s...")
            time.sleep(INTERVALO)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        ciclo()
    else:
        main()
