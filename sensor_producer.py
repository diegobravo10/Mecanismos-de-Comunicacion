import pika
import json
import random
import time
from datetime import datetime

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

tipos_eventos = ["temperatura", "puerta", "movimiento", "alarma_manual"]

while True:
    tipo = random.choice(tipos_eventos)

    if tipo == "temperatura":
        valor = round(random.uniform(20, 60), 2)
    elif tipo == "puerta":
        valor = random.choice(["abierta", "cerrada"])
    elif tipo == "movimiento":
        valor = "detectado"
    else:
        valor = "activada"

    mensaje = {
        "sensor_id": f"S-{random.randint(100, 200)}",
        "tipo": tipo,
        "valor": valor,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    channel.basic_publish(
        exchange='',
        routing_key='sensores',
        body=json.dumps(mensaje)
    )

    print("Enviado:", mensaje)
    time.sleep(2)
