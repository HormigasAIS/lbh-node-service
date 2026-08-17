# LBH · CAPA NARRATIVA v0.1
# Convierte métricas en lenguaje humano para dashboard público

def build_narrative(demo):
    try:
        ultima = demo.get("real_data", {}).get("ultima_feromona", {})
        total = demo.get("real_data", {}).get("total_feromonas", 0)
        nodos = demo.get("real_data", {}).get("nodos_conteo", 0)

        quien = ultima.get("nodo", "sistema desconocido")
        payload = ultima.get("payload", "sin señal")
        ts = ultima.get("ts", 0)

        import time
        cuando = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)) if ts else "tiempo no disponible"

        demo["human_readable"] = {
            "resumen": f"El hormiguero ha registrado {total} feromonas desde {nodos} nodos activos.",
            "ultima_emision": {
                "quien": quien,
                "que": payload,
                "cuando": cuando
            },
            "estado_red": "activa" if total > 0 else "silencio"
        }

        return demo

    except Exception as e:
        demo["human_readable"] = {
            "resumen": "El narrador LBH está en sincronización.",
            "estado_red": "degradada"
        }
        return demo
