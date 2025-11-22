import pika
import json
import websockets
import asyncio
from datetime import datetime

WS_SERVER_URL = "ws://localhost:9000"

def clasificar(msg):
    tipo = msg["tipo"]
    valor = msg["valor"]

    if tipo == "temperatura":
        if valor > 45:
            return {
                "alerta": "Temperatura crítica",
                "nivel": "crítico",
                "mensaje": "Temperatura supera los 45°C"
            }
        else:
            return {
                "alerta": "Temperatura normal",
                "nivel": "normal",
                "mensaje": "Temperatura estable"
            }

    if tipo == "movimiento":
        return {
            "alerta": "Movimiento detectado",
            "nivel": "advertencia",
            "mensaje": "Movimiento en zona"
        }

    if tipo == "puerta":
        if valor == "abierta":
            return {
                "alerta": "Puerta abierta",
                "nivel": "advertencia",
                "mensaje": "Apertura registrada"
            }
        else:
            return {
                "alerta": "Puerta cerrada",
                "nivel": "normal",
                "mensaje": "Cierre correcto"
            }

    if tipo == "alarma_manual":
        return {
            "alerta": "Alarma manual",
            "nivel": "crítico",
            "mensaje": "Emergencia activada"
        }

async def enviar(alerta):
    async with websockets.connect(WS_SERVER_URL) as ws:
        await ws.send(json.dumps(alerta))

def procesar(ch, method, properties, body):
    msg = json.loads(body)

    base = clasificar(msg)
    base.update({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sensor_id": msg["sensor_id"],
        "tipo": msg["tipo"],
        "valor": msg["valor"]
    })

    print("Procesado:", base)
    asyncio.get_event_loop().run_until_complete(enviar(base))



credentials = pika.PlainCredentials("admin", "admin")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,
        credentials=credentials
    )
)

channel = connection.channel()
channel.queue_declare(queue='sensores')

print("Procesador esperando mensajes...")
channel.basic_consume(queue='sensores', on_message_callback=procesar, auto_ack=True)

channel.start_consuming()
