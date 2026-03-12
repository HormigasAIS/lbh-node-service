package usecase

import (
        "sync"
        "time"
)

type MetricaFeromona struct {
        TS   int64
        Nodo string
}

var (
        mu       sync.Mutex
        historial []MetricaFeromona
)

func RegistrarMetrica(nodo string) {
        mu.Lock()
        defer mu.Unlock()
        historial = append(historial, MetricaFeromona{
                TS:   time.Now().Unix(),
                Nodo: nodo,
        })
}

func ObtenerMetricas() map[string]interface{} {
        mu.Lock()
        defer mu.Unlock()

        ahora := time.Now().Unix()
        hora := ahora - 3600
        dia := ahora - 86400

        var ultima_hora, ultimas_24h int
        nodos := map[string]bool{}

        for _, m := range historial {
                if m.TS >= hora {
                        ultima_hora++
                }
                if m.TS >= dia {
                        ultimas_24h++
                }
                nodos[m.Nodo] = true
        }

        ultimo := int64(0)
        if len(historial) > 0 {
                ultimo = historial[len(historial)-1].TS
        }

        return map[string]interface{}{
                "total_feromonas":      len(historial),
                "feromonas_ultima_hora": ultima_hora,
                "feromonas_24h":        ultimas_24h,
                "nodos_activos":        len(nodos),
                "ultimo_ts":            ultimo,
        }
}
