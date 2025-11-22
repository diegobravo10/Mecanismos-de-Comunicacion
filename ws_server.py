import asyncio
import websockets

clientes = set()

async def handler(websocket, path):
    clientes.add(websocket)
    print(f"Cliente conectado. Total: {len(clientes) - 1} clientes")

    try:
        async for mensaje in websocket:
            for ws in list(clientes):
                if ws.open:
                    await ws.send(mensaje)
    except:
        pass
    finally:
        clientes.remove(websocket)

async def main():
    server = await websockets.serve(handler, "0.0.0.0", 9000)
    print("Servidor WebSocket en ws://localhost:9000")
    await server.wait_closed()

asyncio.run(main())
