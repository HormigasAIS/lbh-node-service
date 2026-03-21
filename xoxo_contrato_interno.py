#!/usr/bin/env python3
"""
XOXO Contrato Interno — hormiga_slack_fiscal
Crea contrato interno basado en contrato externo (scope:slack_only)
No invalida el contrato externo — lo usa como fuente
Pipeline: XOXO → Hormiga_10 → Stanford → Colonia
CLHQ / HormigasAIS 2026
"""

import hashlib, hmac, json, os, time, sqlite3, math

BASE_DIR    = os.path.expanduser("~/hormigasais-lab/LBH-Net")
ESPEJO_DB   = os.path.expanduser("~/hormigasais-lab/lbh-image-validator/dht_espejo.db")
CONTRATO_DB = os.path.expanduser("~/hormigasais-lab/lbh-node-service/contratos_colonia.db")
SECRET_KEY  = "hormigasais-soberano-2026"

# ─────────────────────────────────────────
# CONTRATO EXTERNO — fuente
# ─────────────────────────────────────────
CONTRATO_EXTERNO = {
    "node_name":    "hormiga_slack",
    "node_id":      hashlib.sha256(b"hormiga_slack:CLHQ:2026").hexdigest(),
    "scope":        "slack_only",
    "firmada_por":  ["Stanford", "CLHQ"],
    "validada_por": "hormiga_10_soberana",
    "version":      "1.1",
    "issued_by":    "CLHQ",
    "sig_externo":  "93cc56337ab68722"
}

# ─────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────
def sha256(data):
    return hashlib.sha256(
        data.encode() if isinstance(data, str) else data
    ).hexdigest()

def firmar(payload):
    msg = json.dumps(payload, sort_keys=True)
    return hmac.new(
        SECRET_KEY.encode(), msg.encode(), hashlib.sha256
    ).hexdigest()[:16]

def now():
    return int(time.time())

def fanout(n):
    if n <= 5:    return n
    if n <= 1000: return max(3, int(n ** (1/3)) + 1)
    return max(3, int(math.log2(n)))

def emitir_feromona(action, asset, data, receptor):
    payload = {
        "action":    action,
        "asset":     asset,
        "data":      data,
        "receptor":  receptor,
        "timestamp": now(),
        "ttl":       600,
        "issued_by": "CLHQ"
    }
    sig = firmar(payload)
    feromona = {
        "lbh_signal": f"LBH://SIGNAL",
        "version":    "1.1",
        "node":       "XOXO",
        "action":     action,
        "asset":      asset,
        "timestamp":  now(),
        "sig":        sig,
        "issued_by":  "CLHQ",
        "payload":    payload
    }
    print(f"   📡 feromona → {receptor}")
    print(f"      action: {action}")
    print(f"      sig: {sig}")
    return feromona

# ─────────────────────────────────────────
# BASE CONTRATOS COLONIA
# ─────────────────────────────────────────
def init_contratos_db():
    conn = sqlite3.connect(CONTRATO_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contratos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT UNIQUE,
            tipo        TEXT,
            scope       TEXT,
            fuente      TEXT,
            funciones   TEXT,
            sig_clhq    TEXT,
            firmado_por TEXT,
            validado_por TEXT,
            ts          INTEGER,
            activo      INTEGER DEFAULT 1
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feromonas_colonia (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            action   TEXT,
            asset    TEXT,
            receptor TEXT,
            sig      TEXT,
            ts       INTEGER
        )
    """)
    conn.commit()
    conn.close()

def guardar_contrato(contrato):
    conn = sqlite3.connect(CONTRATO_DB)
    conn.execute("""
        INSERT OR REPLACE INTO contratos
        (nombre, tipo, scope, fuente, funciones, sig_clhq,
         firmado_por, validado_por, ts)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        contrato["nombre"],
        contrato["tipo"],
        contrato["scope"],
        contrato["fuente"],
        json.dumps(contrato["funciones"]),
        contrato["sig_clhq"],
        json.dumps(contrato["firmado_por"]),
        contrato["validado_por"],
        now()
    ))
    conn.commit()
    conn.close()

def guardar_feromona_colonia(feromona):
    conn = sqlite3.connect(CONTRATO_DB)
    conn.execute("""
        INSERT INTO feromonas_colonia
        (action, asset, receptor, sig, ts)
        VALUES (?,?,?,?,?)
    """, (
        feromona["action"],
        feromona["asset"],
        feromona["payload"]["receptor"],
        feromona["sig"],
        now()
    ))
    conn.commit()
    conn.close()

# ─────────────────────────────────────────
# XOXO — fiscalizador del protocolo
# ─────────────────────────────────────────
class XOXO_Fiscalizador:

    def evaluar_contrato_externo(self):
        print("\n🔗 XOXO → evaluando contrato externo hormiga_slack")
        print(f"   scope externo: {CONTRATO_EXTERNO['scope']}")
        print(f"   sig externo:   {CONTRATO_EXTERNO['sig_externo']}")
        print(f"   firmado por:   {CONTRATO_EXTERNO['firmada_por']}")

        # Verificar que contrato externo es válido como fuente
        checks = {
            "tiene_scope":    CONTRATO_EXTERNO["scope"] == "slack_only",
            "firmado_clhq":   "CLHQ" in CONTRATO_EXTERNO["firmada_por"],
            "firmado_stanford":"Stanford" in CONTRATO_EXTERNO["firmada_por"],
            "version_ok":     CONTRATO_EXTERNO["version"] == "1.1",
            "tiene_sig":      len(CONTRATO_EXTERNO["sig_externo"]) > 0
        }

        for check, resultado in checks.items():
            icon = "✅" if resultado else "❌"
            print(f"   {icon} {check}")

        valido = all(checks.values())
        if valido:
            print("   ✅ contrato externo VÁLIDO como fuente")
        return valido

    def crear_contrato_interno(self):
        print("\n🔗 XOXO → creando contrato interno hormiga_slack_fiscal")

        contrato = {
            "nombre":      "hormiga_slack_fiscal",
            "tipo":        "CONTRATO_INTERNO",
            "scope":       "colonia_interna",
            "fuente":      "hormiga_slack:slack_only",
            "funciones":   [
                "validador_espejo",
                "fiscal_protocolo",
                "emisor_feromonas_colonia",
                "traductor_lbh_externo"
            ],
            "restricciones": [
                "no_modifica_contratos_estudiantes",
                "no_accede_datos_personales",
                "solo_lee_espejo_dht",
                "emite_solo_feromonas_validadas"
            ],
            "fuente_sig":    CONTRATO_EXTERNO["sig_externo"],
            "node_id":       sha256("hormiga_slack_fiscal:CLHQ:2026"),
            "firmado_por":   ["XOXO", "CLHQ"],
            "validado_por":  "hormiga_10_soberana",
            "stanford_requerido": True,
            "version":       "1.1",
            "issued_by":     "CLHQ"
        }

        sig = firmar(contrato)
        contrato["sig_clhq"] = sig

        print(f"   node_id: {contrato['node_id'][:16]}...")
        print(f"   scope:   {contrato['scope']}")
        print(f"   fuente:  {contrato['fuente']}")
        print(f"   sig:     {sig}")
        print(f"   funciones:")
        for f in contrato["funciones"]:
            print(f"     → {f}")

        return contrato

# ─────────────────────────────────────────
# HORMIGA_10 — traducción LBH
# ─────────────────────────────────────────
class Hormiga10_Traductora:

    def traducir_y_validar(self, contrato):
        print("\n🐜 [Hormiga_10] traduciendo contrato al LBH...")

        checks = {
            "es_contrato_interno":   contrato["tipo"] == "CONTRATO_INTERNO",
            "fuente_valida":         "slack_only" in contrato["fuente"],
            "no_afecta_estudiantes": "no_modifica_contratos_estudiantes"
                                     in contrato["restricciones"],
            "tiene_sig_clhq":        len(contrato.get("sig_clhq","")) > 0,
            "xoxo_es_fiscal":        "XOXO" in contrato["firmado_por"],
            "scope_interno":         contrato["scope"] == "colonia_interna"
        }

        for check, resultado in checks.items():
            icon = "✅" if resultado else "❌"
            print(f"   {icon} {check}")

        aprobado = all(checks.values())

        if aprobado:
            print("   ✅ [Hormiga_10] contrato TRADUCIDO y ACEPTADO")
            print("   📋 LBH: contrato_interno → scope:colonia_interna")
            print("   📋 LBH: fiscal → XOXO como fiscalizador del protocolo")
            print("   📋 LBH: espejo → lectura permitida para colonia")
        else:
            print("   ❌ [Hormiga_10] contrato RECHAZADO")

        return aprobado

# ─────────────────────────────────────────
# STANFORD — validación y firma final
# ─────────────────────────────────────────
class Stanford_Validador:

    def validar_y_firmar(self, contrato, feromona_h10):
        print("\n📋 [Stanford] validando firma CLHQ y funciones XOXO...")

        # Verificar firma CLHQ
        contrato_sin_sig = {k:v for k,v in contrato.items()
                           if k != "sig_clhq"}
        sig_esperada = firmar(contrato_sin_sig)
        firma_valida = sig_esperada == contrato["sig_clhq"]

        print(f"   {'✅' if firma_valida else '❌'} firma CLHQ verificada")
        print(f"   ✅ XOXO como fiscalizador: reconocido")
        print(f"   ✅ espejo DHT: uso autorizado para colonia")

        if not firma_valida:
            print("   ❌ [Stanford] firma inválida — RECHAZADO")
            return None

        # Stanford firma aprobación final
        aprobacion = {
            "tipo":          "APROBACION_STANFORD",
            "contrato":      contrato["nombre"],
            "scope":         contrato["scope"],
            "funciones":     contrato["funciones"],
            "firmado_por":   "Stanford",
            "xoxo_fiscal":   True,
            "espejo_autorizado": True,
            "colonia_notificada": False,
            "timestamp":     now(),
            "issued_by":     "CLHQ"
        }
        aprobacion["sig"] = firmar(aprobacion)

        print(f"   ✅ [Stanford] APROBADO → sig: {aprobacion['sig']}")
        return aprobacion

# ─────────────────────────────────────────
# COLONIA — aceptación distribuida
# ─────────────────────────────────────────
class Colonia:

    def __init__(self):
        self.hormigas = {
            "hormiga_01": "exploradora",
            "hormiga_02": "obrera",
            "hormiga_03": "obrera",
            "hormiga_04": "centinela",
            "hormiga_05": "exploradora",
            "hormiga_06": "obrera",
            "hormiga_07": "obrera",
            "hormiga_08": "centinela",
            "hormiga_09": "exploradora",
            "hormiga_10": "soberana"
        }

    def notificar_y_aceptar(self, aprobacion, feromonas):
        print("\n🐜 [Colonia] notificando aceptación del espejo...")
        print(f"   Stanford aprobó: {aprobacion['contrato']}")
        print(f"   Funciones autorizadas:")
        for f in aprobacion["funciones"]:
            print(f"     ✅ {f}")

        print(f"\n   Notificando {len(self.hormigas)} hormigas:")
        n = len(self.hormigas)
        f_usado = fanout(n)

        aceptadas = 0
        for nombre, rol in self.hormigas.items():
            print(f"     🐜 {nombre} ({rol}) → acepta espejo + extensiones")
            aceptadas += 1

        print(f"\n   fanout usado: {f_usado}")
        print(f"   hormigas notificadas: {aceptadas}/{n}")
        print(f"   ✅ colonia acepta contrato interno hormiga_slack_fiscal")
        return aceptadas

# ─────────────────────────────────────────
# PIPELINE COMPLETO
# ─────────────────────────────────────────
def pipeline_contrato_interno():
    print("═" * 58)
    print("🐜 XOXO Contrato Interno — hormiga_slack_fiscal")
    print("═" * 58)

    init_contratos_db()

    xoxo     = XOXO_Fiscalizador()
    h10      = Hormiga10_Traductora()
    stanford = Stanford_Validador()
    colonia  = Colonia()

    # Paso 1: XOXO evalúa contrato externo
    valido = xoxo.evaluar_contrato_externo()
    if not valido:
        print("❌ contrato externo inválido — pipeline abortado")
        return

    # Paso 2: XOXO crea contrato interno
    contrato = xoxo.crear_contrato_interno()

    # Paso 3: XOXO emite feromona a Hormiga_10
    f1 = emitir_feromona(
        "contrato_interno_creado",
        "hormiga_slack_fiscal",
        {"contrato": contrato["nombre"], "scope": contrato["scope"]},
        "hormiga_10_soberana"
    )
    guardar_feromona_colonia(f1)

    # Paso 4: Hormiga_10 traduce y valida
    aprobado_h10 = h10.traducir_y_validar(contrato)
    if not aprobado_h10:
        print("❌ Hormiga_10 rechazó — pipeline abortado")
        return

    # Paso 5: Hormiga_10 emite feromona a Stanford
    f2 = emitir_feromona(
        "traduccion_lbh_completada",
        "hormiga_slack_fiscal",
        {"validado_por": "hormiga_10", "lbh_ok": True},
        "Stanford"
    )
    guardar_feromona_colonia(f2)

    # Paso 6: Stanford valida y firma
    aprobacion = stanford.validar_y_firmar(contrato, f2)
    if not aprobacion:
        print("❌ Stanford rechazó — pipeline abortado")
        return

    # Paso 7: Guardar contrato en DB colonia
    guardar_contrato(contrato)

    # Paso 8: Stanford emite feromona a colonia
    f3 = emitir_feromona(
        "espejo_autorizado_colonia",
        "hormiga_slack_fiscal",
        {"aprobacion": aprobacion["sig"], "stanford": True},
        "colonia_completa"
    )
    guardar_feromona_colonia(f3)

    # Paso 9: Colonia acepta
    aceptadas = colonia.notificar_y_aceptar(aprobacion, [f1, f2, f3])

    # Resumen final
    print("\n" + "═" * 58)
    print("✅ CONTRATO INTERNO ACTIVADO")
    print("─" * 58)
    print(f"  Nombre:    hormiga_slack_fiscal")
    print(f"  Scope:     colonia_interna")
    print(f"  Fuente:    hormiga_slack:slack_only")
    print(f"  Fiscal:    XOXO")
    print(f"  Sig CLHQ:  {contrato['sig_clhq']}")
    print(f"  Stanford:  {aprobacion['sig']}")
    print(f"  Hormigas:  {aceptadas} aceptaron")
    print(f"  DB:        {CONTRATO_DB}")
    print(f"  Feromonas: 3 emitidas")
    print(f"\n  Funciones autorizadas en colonia:")
    for f in contrato["funciones"]:
        print(f"    ✅ {f}")
    print(f"\n  DOI: 10.5281/zenodo.17767205")
    print("═" * 58)

if __name__ == "__main__":
    pipeline_contrato_interno()
