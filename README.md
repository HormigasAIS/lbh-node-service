# 🐜 LBH-Node-Service

Microservicio soberano del protocolo LBH (Lenguaje Binario HormigasAIS).

## Descripción

Nodo de comunicación M2M para el ecosistema HormigasAIS — implementa REST y gRPC simultáneos para emisión y verificación de feromonas digitales entre nodos de la red.

## Arquitectura

| Interfaz | Puerto | Uso |
|---|---|---|
| REST (Gin) | :8100 | Feromonas HTTP — externos |
| gRPC | :7100 | Comunicación M2M — nodos LBH |
| SQLite | local | Persistencia soberana sin cloud |

## Endpoints REST

| Método | Ruta | Descripción |
|---|---|---|
| GET | /ping | Estado del nodo |
| POST | /feromona | Emitir feromona LBH |
| GET | /feromonas | Listar feromonas registradas |

## Inicio rápido

```bash
# REST
./main

# gRPC
./main --server=grpc
Ecosistema
Parte de HormigasAIS-AirCity — piloto Aeropuerto del Pacífico, El Salvador 2027.
Protocolo: LBH-Protocol | Versión: v0.2.0

## 🗺️ Arquitectura de la Colonia
┌─────────────────────────────────────────────────────────┐
│                  HormigasAIS — Colonia Soberana          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   CENTINELA_V24 (BLE)                                    │
│        │  0x01A2B3C4|TS|SIG:hmac                        │
│        ▼                                                 │
│   cmd/bridge_centinela :9001                             │
│        │  valida HMAC → parsea LBH                      │
│        ▼                                                 │
│   lbh-node-service                                       │
│   ├── REST  :8100                                        │
│   │   ├── POST /feromona   ← emisión                    │
│   │   ├── GET  /feromonas  ← historial                  │
│   │   ├── GET  /metrics    ← telemetría                 │
│   │   └── GET  /ping       ← salud                      │
│   ├── gRPC  :7100          ← nodos M2M                  │
│   └── SQLite               ← persistencia soberana      │
│                                                          │
│   SCRIPTS                                                │
│   ├── startup.sh       → levanta toda la Colonia        │
│   ├── resumen_colonia.sh → panel de comando             │
│   └── sync_mirror.sh   → Gitea ↔ GitHub                │
│                                                          │
│   ESPEJOS                                                │
│   ├── Gitea  → HormigasAIS-Colonia-Soberana (local)     │
│   └── GitHub → github.com/HormigasAIS                   │
└─────────────────────────────────────────────────────────┘
| Componente | Tecnología | Puerto | Rol |
|---|---|---|---|
| lbh-node-service | Go + Gin | :8100 | Nodo central REST |
| gRPC server | Go + protobuf | :7100 | Comunicación M2M |
| bridge_centinela | Go | :9001 | Gateway BLE→LBH |
| SQLite | gorm | local | Persistencia soberana |
| startup.sh | Bash | — | Auto-inicio Colonia |
