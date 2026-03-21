#!/usr/bin/env python3
"""
LBH Sensor — Hello World del mundo físico
Lee sensores reales del Android y envia feromonas via /v1/lbh/validate
CLHQ / HormigasAIS 2026
"""

import json, os, subprocess, time, urllib.request

ENDPOINT = "http://localhost:8100/v1/lbh/validate"

def leer_bateria():
    try:
        r = subprocess.run(
            ["termux-battery-status"],
            capture_output=True, text=True, timeout=5)
        return json.loads(r.stdout)
    except Exception as e:
        return {"error": str(e)}

def leer_wifi():
    try:
        r = subprocess.run(
            ["termux-wifi-connectioninfo"],
            capture_output=True, text=True, timeout=5)
        return json.loads(r.stdout)
    except Exception as e:
        return {"error": str(e)}

def enviar_feromona(sensor_type, data, nodo="LBH-DDCD"):
    # Usar URL publica como proxy — datos reales van en nodo
    payload = json.dumps({
        "url":  "https://raw.githubusercontent.com/HormigasAIS/LBH-Net/main/README.md",
        "nodo": f"{nodo}:{sensor_type}:{json.dumps(data)[:30]}",
        "type": "SENSOR",
        "ttl":  60
    }).encode()

    req = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            resp = json.loads(r.read())
            return resp
    except Exception as e:
        return {"error": str(e)}

def main():
    print("═" * 50)
    print("🐜 LBH Sensor — Hello World físico")
    print("═" * 50)

    # Batería
    print("\n📡 Leyendo batería...")
    bat = leer_bateria()
    print(f"   health:      {bat.get('health','?')}")
    print(f"   plugged:     {bat.get('plugged','?')}")
    print(f"   temperature: {bat.get('temperature','?')}°C")
    print(f"   percentage:  {bat.get('percentage','?')}%")

    # Enviar feromona batería
    print("\n📡 Enviando feromona SENSOR batería...")
    r = enviar_feromona("BATTERY", bat)
    if "feromona" in r:
        f = r["feromona"]
        print(f"   ✅ estado:  {f.get('estado','?')}")
        print(f"   ✅ action:  {f.get('action','?')}")
        print(f"   ✅ sig:     {f.get('sig','?')}")
        print(f"   ✅ type:    {f.get('type','?')}")
    else:
        print(f"   ⚠️  {r}")

    # WiFi
    print("\n📡 Leyendo WiFi...")
    wifi = leer_wifi()
    print(f"   ssid:    {wifi.get('ssid','?')}")
    print(f"   ip:      {wifi.get('ip','?')}")
    print(f"   rssi:    {wifi.get('rssi','?')} dBm")

    # Enviar feromona WiFi
    print("\n📡 Enviando feromona SENSOR WiFi...")
    r = enviar_feromona("WIFI", wifi)
    if "feromona" in r:
        f = r["feromona"]
        print(f"   ✅ estado:  {f.get('estado','?')}")
        print(f"   ✅ sig:     {f.get('sig','?')}")
    else:
        print(f"   ⚠️  {r}")

    print("\n" + "═" * 50)
    print("✅ Hello World físico completado")
    print(f"   nodo: LBH-DDCD")
    print(f"   endpoint: {ENDPOINT}")
    print(f"   DOI: 10.5281/zenodo.17767205")
    print("═" * 50)

if __name__ == "__main__":
    main()
