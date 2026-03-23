# HormigasAIS LBH Protocol Node Service
**Red distribuida soberana desde Android/Termux · Protocolo LBH v1.1**
DOI: [10.5281/zenodo.19177759](https://doi.org/10.5281/zenodo.19177759)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19177759.svg)](https://doi.org/10.5281/zenodo.19177759) [![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/HormigasAIS/lbh-node-service) [![LBH](https://img.shields.io/badge/LBH-v1.1-purple)](https://doi.org/10.5281/zenodo.17767205) [![Platform](https://img.shields.io/badge/platform-Android%20Termux-orange)](https://github.com/HormigasAIS/lbh-node-service)

---

## Ecosistema HormigasAIS

```
╔══════════════════════════════════════════════════════════════════════════════╗
║          HORMIGASAIS · ECOSISTEMA DISTRIBUIDO SOBERANO                      ║
║          MESENTERY v1.0 · DOI: 10.5281/zenodo.19177759                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  [![DOI][zenodo]] [![Status:active]] [![LBH:v1.1]] [![Android/Termux]]      ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────── PROTOCOLO LBH v1.1 ────────────────────────────┐
│  Formato binario 16 bytes · 89.3% reducción BW · DOI: 10.5281/zenodo.17767205│
│  [event_type 1B][order_id 8B][status 1B][timestamp 4B][CRC-16 2B]          │
└─────────────────────────────────┬──────────────────────────────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │     lbh-node-service       │
                    │   Go + Gin · ARM64         │
                    │                            │
                    │  REST  :8100 /v1/lbh/validate
                    │  gRPC  :7100 EmitirFeromona│
                    │  Bridge:9001 CENTINELA_V24 │
                    │                            │
                    │  SEGURIDAD:                │
                    │  ├ HMAC-SHA256 64 hex      │
                    │  ├ TTL (10s–3600s)         │
                    │  ├ Rate limit 10/60s       │
                    │  └ ACL + clasificación     │
                    │    SENSOR·DRONE·CONTRACT   │
                    └──────────────┬─────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
┌─────────▼──────────┐  ┌──────────▼─────────┐  ┌──────────▼──────────┐
│     A16_CORE       │  │     A20_NODE        │  │      SÉFORIS        │
│  192.168.1.5       │  │  192.168.1.6        │  │   (bajo demanda)    │
│  LBH-DDCD          │  │  AirCity            │  │                     │
│                    │  │                     │  │  v0.5 · lógico      │
│  sensor 30s:       │  │  bridge 30s:        │  │  v0.6 · físico      │
│  BATTERY 28°C      │  │  BATTERY            │  │  v0.7 · sync        │
│  WIFI -59dBm       │  │  WIFI               │  │                     │
│                    │  │                     │  │  Clusters A16↔A20   │
│  lbh_nodo.db       │  │  registrar_nodo.py  │  │  Estado fisico      │
│  7,500+ feromonas  │  │  loop 30s           │  │  Nodos fantasma     │
│                    │  │                     │  │  Alertas inactivos  │
│  loop A16_CORE ──────────────────────────────────────────────────────│
└─────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘
          │                        │                         │
          │  feromonas ────────────┘                         │
          │                                                  │
          └──────────────────────────┬───────────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │       hormigasais-core           │
                    │                                  │
                    │  db/lbh_nodo.db                  │
                    │  nodos_estado (A16_CORE, A20)    │
                    │  sync_nodos_remotos.py           │
                    │  alerta_nodos_inactivos.py       │
                    │  start_colonia.sh (boot)         │
                    │  levantar_a20.sh (rescue)        │
                    └────────────────┬────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
┌─────────▼──────────┐  ┌────────────▼───────────┐  ┌──────────▼──────────┐
│   CONTRATOS XOXO   │  │    ESPEJO SLACK         │  │  COLONY HEARTBEAT   │
│                    │  │                         │  │                     │
│  XOXO fiscalizador │  │  hormiga_slack          │  │  colony_heartbeat.py│
│  ├ Hormiga_10      │  │  scope: slack_only      │  │  cada 100 feromonas │
│  ├ Stanford        │  │  sig: 93cc56337ab6      │  │  → actualiza README │
│  └ Colonia acepta  │  │                         │  │  → push automático  │
│                    │  │  hormiga_slack_fiscal   │  │  → Gitea + GitHub   │
│  hormiga_slack     │  │  scope: colonia_interna │  │                     │
│  slack_fiscal      │  │  sig: dab3e970d4be      │  │  7,500+ feromonas   │
│  red_a16_a20       │  │                         │  │  README vivo        │
│  sig: 81e46806f1d0 │  │  DHT espejo SQLite      │  │                     │
│                    │  │  bot /lbh-check :5000   │  │  Gitea :3001        │
│                    │  │  #lbh-validations       │  │  GitHub HormigasAIS │
└────────────────────┘  └─────────────────────────┘  └─────────────────────┘

╔══════════════════════════════════════════════════════════════════════════════╗
║                    EVOLUCIÓN DEL ECOSISTEMA                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  v0.1–1.5  ████  Core protocol + transport                          ✅      ║
║  v1.6      ████  Daemon métricas + wiki Gitea                       ✅      ║
║  v1.7      ████  Arquitectura completa + docs RFC-0001→0006         ✅      ║
║  v1.8      ████  Network simulator + fanout híbrido n^(1/3)        ✅      ║
║  v1.9      ████  Testnet 3 nodos Android                            ✅      ║
║  v2.0-dev  ████  DHT Kademlia soberano                             ✅      ║
║            ████  REST /v1/lbh/validate + 4 puntos seguridad        ✅      ║
║            ████  Sensor daemon físico (batería + WiFi)             ✅      ║
║            ████  Red distribuida A16↔A20 real                      ✅      ║
║            ████  Colony Panel :8300 tiempo real                    ✅      ║
║            ████  SÉFORIS v0.7 diagnóstico                          ✅      ║
║            ████  MESENTERY v1.0 LICENSE                            ✅      ║
║            ████  Heartbeat README automático                        ✅      ║
║                                                                              ║
║  v2.0      ░░░░  AirCity producción                               → 2027   ║
║  v3.0      ░░░░  Open protocol + community                        → futuro ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║                      MESENTERY v1.0                                         ║
║              HormigasAIS Sovereign Specification License                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  BASE LEGAL:  CC BY 4.0 + LBH Clause                                        ║
║  ATRIBUCIÓN:  DOI 10.5281/zenodo.17767205 · CLHQ                            ║
║  SOBERANÍA:   Sin propiedad centralizada exclusiva                           ║
║  ÉTICA:       Sin daño civil · Sin vigilancia · Sin armas                    ║
║                                                                              ║
║  "A living system that connects, nourishes, and sustains                     ║
║   distributed nodes without domination"                                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║  LEYENDA                                                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  ┌──┐  Servicio / componente activo                                          ║
║  ▼     Flujo de feromonas / datos                                            ║
║  ████  Capacidad implementada              ░░░░  Planificado                 ║
║  ✅    Operativo en producción             →     Objetivo futuro             ║
║  [sig] Firma HMAC-SHA256 (primeros 16 hex)                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

CLHQ · Cristhiam Leonardo Hernández Quiñonez
San Miguel, El Salvador 🇸🇻 · 2026
DOI: 10.5281/zenodo.19177759
github.com/HormigasAIS/lbh-node-service
```

> Representacion documentativa — no refleja estado en tiempo real.

---

## Colony Panel — Sistema en vivo

[![Colony Panel](docs/panel_colony.png)](docs/panel_colony.png)

| Metrica | Valor |
|---|---|
| Feromonas acumuladas | 7,500+ |
| Nodos activos | 9 |
| Nodo master | A16 192.168.1.5 |
| Nodo sensor | A20 192.168.1.6 |
| Actualizacion | cada 3s |

```bash
python3 ~/hormigasais-lab/lbh_panel_web.py
# http://[IP-LOCAL]:8300
bash ~/hormigasais-core/scripts/start_colonia.sh
```

---

## Componentes y Servicios

- `hormigasais-core` nodos_estado · sync_nodos_remotos · start_colonia · levantar_a20
- Contratos **XOXO** hormiga_slack · slack_fiscal · red_a16_a20
- Espejo **Slack** hormiga_slack_fiscal · DHT espejo SQLite · /lbh-check
- Colony Heartbeat colony_heartbeat.py actualiza README cada 100 feromonas
- SEFORIS v0.7 observador diagnostico bajo demanda

---

## Evolucion del Ecosistema

| Version | Hito | Estado |
|---|---|---|
| v0.1-v1.5 | Core protocol + transport | OK |
| v1.6 | Daemon metricas + wiki Gitea | OK |
| v1.7 | Arquitectura completa + RFC-0001-0006 | OK |
| v1.8 | Network simulator + fanout hibrido | OK |
| v1.9 | Testnet 3 nodos Android | OK |
| v2.0-dev | DHT Kademlia + REST + seguridad | OK |
| v2.0-dev | Sensor daemon fisico | OK |
| v2.0-dev | Red distribuida A16+A20 | OK Mar 2026 |
| v2.0-dev | Colony Panel + SEFORIS v0.7 | OK Mar 2026 |
| v2.0-dev | MESENTERY v1.0 + Zenodo v2 | OK Mar 2026 |
| v2.0 | AirCity produccion | 2027 |
| v3.0 | Open protocol + community | futuro |

---

## MESENTERY v1.0 — Licencia Soberana

- **Base legal:** CC BY 4.0 + LBH Clause
- **Atribucion:** DOI 10.5281/zenodo.17767205 · CLHQ
- **Soberania:** Sin propiedad centralizada exclusiva
- **Etica:** Sin dano civil · Sin vigilancia · Sin armas

> A living system that connects, nourishes, and sustains distributed nodes without domination.

---

## Leyenda

| Simbolo | Significado |
|---|---|
| `┌──┐` | Servicio / componente activo |
| `▼` | Flujo de feromonas / datos |
| `████` | Capacidad implementada |
| `░░░░` | Planificado |
| OK | Operativo en produccion |
| [sig] | Firma HMAC-SHA256 primeros 16 hex |

---

## Inicio rapido

```bash
git clone https://github.com/HormigasAIS/lbh-node-service.git
cd lbh-node-service
go build -o main main.go
bash startup.sh
curl http://localhost:8100/ping
```

---

## Autor

**CLHQ — Cristhiam Leonardo Hernandez Quinonez**
San Miguel, El Salvador 2026
Desarrollado desde Android/Termux sin servidores sin nube.

DOI: [10.5281/zenodo.19177759](https://doi.org/10.5281/zenodo.19177759)
[github.com/HormigasAIS/lbh-node-service](https://github.com/HormigasAIS/lbh-node-service)

*HormigasAIS — La colonia es soberana*
