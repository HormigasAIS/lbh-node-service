from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/api/stats')
def get_stats():
    try:
        conn = sqlite3.connect('lbh_nodo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM auditoria WHERE timestamp >= datetime('now', '-24 hours')")
        count = cursor.fetchone()[0]
        return jsonify({"feromonas_24h": count, "nodo": "A16-Soberano-Salvador"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
