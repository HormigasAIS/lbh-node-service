#!/usr/bin/env python3
# HORMIGASAIS · hormiga_slack_fiscal.py v0.2
import os, sys, datetime
try:
    import requests
except:
    print('requests no instalado: pip install requests --break-system-packages')
    sys.exit(1)

WEBHOOK = os.environ.get('SLACK_WEBHOOK','')

def send_alert(nodo, evento, estado):
    if not WEBHOOK:
        print('SLACK_WEBHOOK no configurado en ~/.bashrc')
        return
    ahora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    color = '#ffaa00' if estado == 'RESCUE' else '#36a64f'
    payload = {
        'text': 'ALERTA HormigasAIS',
        'attachments': [{
            'color': color,
            'title': f'Evento: {evento}',
            'fields': [
                {'title': 'Nodo', 'value': nodo, 'short': True},
                {'title': 'Timestamp', 'value': ahora, 'short': True},
                {'title': 'Accion', 'value': 'Reanimacion remota ejecutada', 'short': False}
            ],
            'footer': 'LBH Protocol v1.1 · San Miguel SV'
        }]
    }
    try:
        r = requests.post(WEBHOOK, json=payload, timeout=10)
        print(f'Alerta enviada: {nodo} {evento}')
    except Exception as e:
        print(f'Error Slack: {e}')

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        send_alert(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('Uso: hormiga_slack_fiscal.py NODO EVENTO ESTADO')
