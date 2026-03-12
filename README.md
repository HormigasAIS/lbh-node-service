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
