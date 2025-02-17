import asyncio
from websockets.asyncio.server import serve
import random

class SocketServer:
    clients = []

    async def connectionReceived(self, websocket):
        print(f"Received connection from {websocket}")
        self.clients.append(websocket)


    async def startServer(self):
        async with serve(self.connectionReceived, "localhost", 8765) as server:
            await server.serve_forever()

    
    async def sendAction(self, action):
        for client in self.clients:
            await client.send(action)


async def testAction(server: SocketServer):
    actions = ["left", "right", "up", "down", "a", "y", "zr", "zl", "rleft", "rright", "rup", "rdown"]
    while True:
        await asyncio.sleep(1)
        randomAction = random.choice(actions)
        server.sendAction(randomAction)

if __name__ == "__main__":
    socketServer = SocketServer()
    asyncio.run(socketServer.startServer())
    asyncio.run(testAction(socketServer))

