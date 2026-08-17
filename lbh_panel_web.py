#!/usr/bin/env python3
# HORMIGASAIS · lbh_panel_web.py v1.1 · LBH v1.1
# Interfaz de Monitoreo Soberana para la Colonia

from flask import Flask, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_PATH = '/data/data/com.termux/files/home/lbh-node-service/lbh_nodo.db'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>HormigasAIS · Panel Soberano</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: monospace; padding: 20px; }
        h1 { color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
        .card { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 5px; margin-bottom: 15px; }
        .metric { font-size: 24px; color: #3fb950; font-weight: bold; }
        .status { color: #58a6ff; }
        .footer { margin-top: 30px; font-size: 11px; color: #8b949e; text-align: center; }
    </style>
</head>
<body>
    <h1>🐜 HormigasAIS · Nodo A16 (San Miguel, SV)</h1>
    <div class="card">
        <h3>Estado del Entorno</h3>
        <p>Protocolo: <span class="status">LBH v1.1 (Soberano)</span></p>
        <p>Infraestructura: <span class="status">Edge Computing (Termux)</span></p>
    </div>
    <div class="card">
        <h3>Métricas de la Colonia</h3>
        <p>Feromonas Digitales Registradas:</p>
        <div class="metric">{{ total_feromonas }}</div>
    </div>
    <div class="footer">
        Infraestructura de Inteligencia Distribuida · 2026
    </div>
</body>
</html>
"""

def get_feromonas_count():
    if not os.path.exists(DB_PATH):
        return 0
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM feromonas")
        total = cursor.fetchone()[0]
        conn.close()
        return total
    except Exception:
        return 0

@app.route('/')
def home():
    total = get_feromonas_count()
    return render_template_string(HTML_TEMPLATE, total_feromonas=total)

@app.route('/api/status')
def status():
    return jsonify({"status": "active", "node": "A16_CORE", "feromonas": get_feromonas_count()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8300, debug=False)
