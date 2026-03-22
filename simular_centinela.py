import hmac
import hashlib
import socket
import time

CLAVE_COLONIA = b"HORMIGA_SECRET_KEY_2026"
PAYLOAD = "0x01A2B3C4"
TS = str(int(time.time()))

# 1. Crear el mensaje a firmar: PAYLOAD|TS
mensaje = f"{PAYLOAD}|{TS}".encode()

# 2. Generar firma HMAC-SHA256
firma = hmac.new(CLAVE_COLONIA, mensaje, hashlib.sha256).hexdigest()

# 3. Construir paquete final
paquete = f"{PAYLOAD}|{TS}|SIG:{firma}\n"

print(f"📡 Enviando paquete al Bridge: {paquete.strip()}")

# 4. Enviar vía TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 9001))
    s.sendall(paquete.encode())
    print("✅ Paquete enviado. Revisa los logs del Bridge.")
