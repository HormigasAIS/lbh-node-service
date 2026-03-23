#!/usr/bin/env python3
# Simulacion avanzada 2.1 HormigasAIS AirCity
# Autor: CLHQ · 23 Mar 2026
# Max nodos simulados: 500,000
# Eficiente en Android ARM64

import sys, random, time, os
from datetime import datetime

MAX_NODOS      = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
FEROMONAS_BASE = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
REPORT = os.path.expanduser(
    f"~/hormigasais-lab/sim_status_v21_{datetime.now().strftime(chr(37)+chr(89)+chr(37)+chr(109)+chr(37)+chr(100)+chr(95)+chr(37)+chr(72)+chr(37)+chr(77)+chr(37)+chr(83))}.log")

def generar_colonia(n, base):
    feromonas = {f"SIM_NODE_{i}": base + random.randint(0,50) for i in range(1, n+1)}
    estado    = {nodo: "OK" for nodo in feromonas}
    return feromonas, estado

def mostrar_status(feromonas, estado, iteracion):
    activos = sum(1 for e in estado.values() if e=="OK")
    caidos  = len(estado) - activos
    total   = sum(feromonas.values())

    print()
    print(f"LBH COLONY STATUS {datetime.now().strftime(chr(37)+chr(72)+chr(58)+chr(37)+chr(77)+chr(58)+chr(37)+chr(83))}")
    print("-"*50)
    print(f"Iteracion:        {iteracion}")
    print(f"Nodos totales:    {len(estado):,}")
    print(f"Nodos activos:    {activos:,}")
    print(f"Nodos caidos:     {caidos:,}")
    print(f"Total feromonas:  {total:,}")
    print(f"Prom feromonas:   {total//len(feromonas):,} por nodo")
    print("-"*50)

    # Muestra solo muestra de 5 nodos activos y 5 caidos
    import random
    sample_act = random.sample([n for n,e in estado.items() if e=="OK"], min(5,activos))
    sample_cai = random.sample([n for n,e in estado.items() if e=="CAIDO"], min(5,caidos)) if caidos>0 else []
    if sample_act:
        print("Muestra activos:")
        for n in sample_act:
            print(f"  ACTIVO  {n:20} {feromonas[n]:,}")
    if sample_cai:
        print("Muestra caidos:")
        for n in sample_cai:
            print(f"  CAIDO   {n:20} {feromonas[n]:,}")
    print("-"*50)
    return activos, caidos, total

def diagnostico_seforis(feromonas, estado):
    print()
    print("SEFORIS v0.7 · Simulacion Distribuida")
    print("-"*50)

    valores = list(feromonas.values())
    valores.sort(reverse=True)

    # Clusters por rangos
    rangos = {}
    for v in valores:
        bucket = (v // 10) * 10
        rangos[bucket] = rangos.get(bucket, 0) + 1

    top5 = sorted(rangos.items(), key=lambda x: x[1], reverse=True)[:5]
    print("Top 5 clusters por densidad de feromonas:")
    for bucket, count in top5:
        print(f"  {bucket:>6}-{bucket+9} feromonas → {count:,} nodos")

    # Deteccion de sincronizacion
    activos_vals = [feromonas[n] for n,e in estado.items() if e=="OK"]
    if activos_vals:
        avg = sum(activos_vals) // len(activos_vals)
        sync = sum(1 for v in activos_vals if abs(v-avg) <= 5)
        pct  = sync * 100 // len(activos_vals)
        print(f"Sincronizacion colonia: {pct}% ({sync:,} nodos en equilibrio)")

    print("-"*50)

def caida_recuperacion(estado, pct=5):
    n      = len(estado)
    nodos  = list(estado.keys())
    caer   = max(1, n * pct // 100)
    sample = random.sample(nodos, caer)
    for nodo in sample:
        estado[nodo] = "CAIDO"
    return caer, sample

print(f"Simulacion avanzada v2.1 HormigasAIS")
print(f"Nodos: {MAX_NODOS:,} | Feromonas base: {FEROMONAS_BASE:,}")
print(f"Reporte: {REPORT}")
print("Generando colonia...")

feromonas, estado = generar_colonia(MAX_NODOS, FEROMONAS_BASE)
print(f"Colonia generada: {len(feromonas):,} nodos")

iteracion = 0
try:
    while True:
        iteracion += 1

        # Cada 5 iteraciones → caida/recuperacion
        if iteracion % 5 == 0:
            n_caidos, sample = caida_recuperacion(estado)
            mostrar_status(feromonas, estado, iteracion)
            time.sleep(2)
            for nodo in sample: estado[nodo]="OK"
            print(f"[iter {iteracion}] Caida: {n_caidos} nodos → recuperados")

        activos, caidos, total = mostrar_status(feromonas, estado, iteracion)
        diagnostico_seforis(feromonas, estado)

        # Log
        with open(REPORT, "a") as f:
            f.write(str(int(time.time()))+" | iter "+str(iteracion)+" | total "+str(total)+" | activos "+str(activos)+" | caidos "+str(caidos)+chr(10))

        time.sleep(5)

except KeyboardInterrupt:
    print()
    print(f"Simulacion detenida en iteracion {iteracion}")
    print(f"Reporte guardado en: {REPORT}")
