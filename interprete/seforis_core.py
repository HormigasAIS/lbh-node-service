#!/usr/bin/env python3
import sqlite3, os, time
from datetime import datetime

DB_FEROMONAS = os.path.expanduser("~/hormigasais-lab/lbh-node-service/lbh_nodo.db")
DB_NODOS     = os.path.expanduser("~/hormigasais-core/db/lbh_nodo.db")

def leer_feromonas():
    try:
        conn = sqlite3.connect(DB_FEROMONAS)
        data = conn.execute("SELECT nodo, COUNT(*) FROM feromonas GROUP BY nodo ORDER BY COUNT(*) DESC").fetchall()
        conn.close()
        return data
    except Exception as e:
        print(f"ERROR feromonas: {e}")
        return []

def leer_fisicos():
    try:
        conn = sqlite3.connect(DB_NODOS)
        rows = conn.execute("SELECT nodo, ultimo_ts FROM nodos_estado").fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"ERROR fisicos: {e}")
        return []

def detectar_clusters(data):
    clusters = []
    valores = sorted([d[1] for d in data if d[1] > 50], reverse=True)
    for i in range(len(valores)-1):
        if abs(valores[i]-valores[i+1]) <= 5:
            clusters.append((valores[i], valores[i+1]))
    return clusters

def relacion_clusters(clusters):
    if len(clusters) < 2: return "sin_relacion"
    promedios = [(a+b)/2 for a,b in clusters]
    ratio = min(promedios)/max(promedios)
    if ratio > 0.95: return "equilibrio_total"
    if ratio > 0.6:  return "equilibrio_parcial"
    return "dominancia"

def main():
    print("\n SEFORIS v0.7 · Observador Integral")
    print("🕒", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-"*50)

    data = leer_feromonas()
    print("\n📊 Estado lógico (feromonas):")
    for nodo, total in data:
        print(f"   • {nodo}: {total:,}")

    clusters = detectar_clusters(data)
    print("\n🧠 Clusters detectados:")
    for a,b in clusters:
        print(f"   • {a:,} ↔ {b:,}")
    print(f"\n🔬 Relación: {relacion_clusters(clusters)}")

    fisicos = leer_fisicos()
    now = int(time.time())
    fantasmas = []
    print("\n⏱ Estado físico:")
    for nodo, ts in fisicos:
        delta = now - ts
        if delta <= 120:
            print(f"   ✅ {nodo} ACTIVO ({delta}s)")
        else:
            print(f"   ❌ {nodo} INACTIVO ({delta}s)")
            fantasmas.append(nodo)

    print("\n👻 Nodos fantasma:")
    if fantasmas:
        for n in fantasmas: print(f"   • {n}")
    else:
        print("   • Ninguno")

    print("\n🌱 Lectura:")
    if data and not fantasmas:
        print("   Colonia con actividad lógica y física sincronizada.")
    elif data and fantasmas:
        print("   Actividad lógica con nodos inactivos detectados.")
    else:
        print("   Sin actividad significativa.")

if __name__ == "__main__":
    main()
