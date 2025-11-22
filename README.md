# Sistema de Monitoreo Industrial en Tiempo Real

## Descripción

Este proyecto implementa un sistema distribuido de monitoreo industrial que procesa alertas enviadas por sensores simulados. El flujo completo incluye:

1. Productores de mensajes (sensores simulados).
2. Procesador de alertas conectado a RabbitMQ.
3. Servidor WebSocket para difundir alertas en tiempo real.
4. Cliente WebSocket para visualización inmediata en un dashboard web.

RabbitMQ se despliega mediante Docker Compose y actúa como broker central del sistema.

---

## Estructura del Proyecto

```
SISMONITOREO/
│── docker-compose.yml
│── requirements.txt
│── sensor_producer.py
│── alert_processor_ws.py
│── ws_server.py
│
└── web/
    └── ws_client.html
```

---

## Requisitos Previos

* Python 3.10 o superior
* Docker y Docker Compose instalados
* Navegador moderno (Chrome, Firefox, Edge)

---

# 1. Clonar el Repositorio

```
git clone https://github.com/diegobravo10/Mecanismos-de-Comunicacion.git
cd SISMONITOREO
```

---

# 2. Levantar RabbitMQ con Docker Compose

El sistema utiliza RabbitMQ como broker de mensajes. Para iniciarlo:

```
docker compose up -d
```

RabbitMQ quedará disponible en:

* Broker: localhost:5672
* Consola web: [http://localhost:15672](http://localhost:15672)
* Usuario: admin
* Contraseña: admin

---

# 3. Instalar Dependencias
Instalar dependencias:

```
pip install -r requirements.txt
```

---

# 4. Ejecutar los Módulos del Sistema

## A. Productor de Sensores

Simula sensores y envía eventos a RabbitMQ.

```
python sensor_producer.py
```

---

## B. Procesador de Alertas

Lee mensajes desde RabbitMQ, los clasifica y los reenvía al servidor WebSocket.

```
python alert_processor_ws.py
```

---

## C. Servidor WebSocket

Difunde las alertas procesadas a todos los operadores conectados.

```
python ws_server.py
```

Servidor disponible en:

```
ws://localhost:9000
```

---

# 5. Ejecutar el Cliente Web

El dashboard está en la carpeta web/.

Entrar a la carpeta:

```
cd web
```

Levantar un servidor local:

```
python -m http.server 8080
```

Abrir en el navegador:

```
http://localhost:8080/ws_client.html
```

El dashboard se conecta automáticamente al servidor WebSocket y muestra alertas en tiempo real.

---

# Funcionamiento General del Sistema

1. sensor_producer.py envía mensajes estructurados a RabbitMQ.
2. alert_processor_ws.py consume esos mensajes, los analiza y clasifica.
3. Las alertas procesadas se envían al servidor WebSocket.
4. ws_server.py distribuye cada alerta a todos los clientes conectados.
5. ws_client.html muestra las alertas inmediatamente sin recargar la página.

---

**Nota:** Los tres módulos (productor, procesador y servidor WS) deben ejecutarse simultáneamente.

Para realizar pruebas desde diferentes dispositivos dentro de la misma red local, es necesario actualizar la dirección del servidor WebSocket en el archivo ws_client.html. En la línea:
```
const wsUrl = "ws://localhost:9000/";
```

cambiar localhost por la dirección IP local del equipo donde se esté ejecutando el servidor WebSocket. Por ejemplo:
```
const wsUrl = "ws://192.168.1.10:9000/";
```

Así los otros dispositivos conectados a la misma red podrán acceder correctamente al servidor y recibir las alertas en tiempo real.

# Resultado y Conclusión


---


