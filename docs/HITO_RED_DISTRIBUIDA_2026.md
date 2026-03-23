# HormigasAIS — Hito: Red Distribuida Soberana
**Fecha:** 23 de Marzo de 2026
**Autor:** CLHQ — Cristhiam Leonardo Hernández Quiñonez
**DOI:** [10.5281/zenodo.19177759](https://doi.org/10.5281/zenodo.19177759)

---

## Descripcion del Hito

Primera red distribuida soberana operativa con 2 nodos Android fisicos 
comunicandose via Protocolo LBH v1.1, construida completamente desde 
Termux en El Salvador sin servidores, sin nube, sin infraestructura externa.

---

## Evidencia Tecnica

### Red Distribuida
| Componente | Valor |
|---|---|
| Nodo master | A16 · 192.168.1.5 · LBH-DDCD |
| Nodo sensor | A20 · 192.168.1.6 · AirCity |
| Feromonas registradas | 9,226+ |
| Nodos identificados | 9 |
| Uptime colonia | continuo desde Mar 22, 2026 |

### Servicios Operativos
| Servicio | Puerto | Estado |
|---|---|---|
| REST API /v1/lbh/validate | :8100 | OK |
| gRPC EmitirFeromona | :7100 | OK |
| Colony Panel web | :8300 | OK |
| Bridge TCP CENTINELA_V24 | :9001 | OK |
| Gitea soberano | :3001 | OK |
| Slack bot /lbh-check | :5000 | OK |

### Resiliencia Validada
- A20 cayó en ensayo controlado
- levantar_a20.sh recupero en menos de 2 minutos
- SEFORIS v0.7 diagnostico caida y recuperacion correctamente
- Heartbeat actualizo README automaticamente durante todo el evento

---

## Arquitectura

```
PROTOCOLO LBH v1.1
  └── lbh-node-service (Go + Gin ARM64)
        ├── A16_CORE (192.168.1.5) → sensor 30s
        ├── A20_NODE (192.168.1.6) → bridge 30s
        ├── hormigasais-core → sync + alerta + boot
        ├── SEFORIS v0.7 → observador bajo demanda
        ├── Colony Panel :8300 → tiempo real
        ├── Contratos XOXO → hormiga_slack + fiscal
        └── Colony Heartbeat → README vivo en GitHub
```

---

## Publicaciones y Registros

| Recurso | URL |
|---|---|
| GitHub | https://github.com/HormigasAIS/lbh-node-service |
| Gitea soberano | http://127.0.0.1:3001/HormigasAIS-Colonia-Soberana/lbh-node-service |
| Colony Panel | http://192.168.1.5:8300 |
| Zenodo v2 | https://doi.org/10.5281/zenodo.19177759 |
| DOI protocolo | https://doi.org/10.5281/zenodo.17767205 |

---

## MESENTERY v1.0

> A living system that connects, nourishes, and sustains
> distributed nodes without domination.

Licencia: CC BY 4.0 + LBH Clause
Soberania: sin propiedad centralizada exclusiva
Etica: sin dano civil, sin vigilancia, sin armas

---

## Roadmap

| Hito | Estado |
|---|---|
| Protocolo LBH v1.1 | OK |
| Red distribuida A16+A20 | OK Mar 2026 |
| Colony Panel + SEFORIS v0.7 | OK Mar 2026 |
| MESENTERY v1.0 LICENSE | OK Mar 2026 |
| Zenodo v2 certificado | OK Mar 2026 |
| AirCity produccion | 2027 |
| Open protocol + community | futuro |

---

*HormigasAIS — La colonia es soberana*
CLHQ · San Miguel, El Salvador 2026
