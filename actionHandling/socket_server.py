import asyncio
from websockets.asyncio.server import serve
import websockets
import random
import json

class SocketServer:
    connected_clients = set()

    async def connectionReceived(self, websocket):
        print(f"Received connection from {websocket}")
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                pass
        finally:
            self.connected_clients.remove(websocket)


    async def startServer(self):
        async with serve(self.connectionReceived, "localhost", 8765) as server:
            await server.serve_forever()

    
    async def sendAction(self, action):
        actionObject = {
            "message": {
                "text": action
            }
        }
        for client in self.connected_clients:
            try:
                await client.send(json.dumps(actionObject))
            except websockets.exceptions.ConnectionClosed:
                # Handle disconnection if needed
                self.connected_clients.remove(client)


async def testAction(server: SocketServer):
    actions = ["sb1", "sb2", "sb3", "sb4", "a", "y", "zr", "zl", "sb5", "sb6", "sb7", "sb8"]
    while True:
        await asyncio.sleep(1)
        randomAction = random.choice(actions)
        print(f'Sending command: ' + randomAction)
        await server.sendAction(randomAction)

async def main():
    socketServer = SocketServer()
    await asyncio.gather(
        socketServer.startServer(),
        testAction(socketServer),
        # Add other concurrent tasks here if needed
    )

if __name__ == "__main__":
    asyncio.run(main())
