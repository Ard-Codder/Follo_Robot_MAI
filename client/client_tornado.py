import tornado.ioloop
import tornado.websocket

class WebSocketClient:
    def __init__(self):
        self.ws = None

    async def connect(self):
        self.ws = await tornado.websocket.websocket_connect("ws://localhost:8888/obtaining_drone_data")
        print("Connected to server")

    async def send_data(self, data):
        if self.ws:
            self.ws.write_message(data)
            print("Sent data to server:", data)

    async def receive_data(self):
        while True:
            msg = await self.ws.read_message()
            if msg is None:
                break
            print("Received data from server:", msg)

if __name__ == "__main__":
    client = WebSocketClient()

    async def main():
        await client.connect()
        await client.send_data("Hello, server!")
        await client.receive_data()

    tornado.ioloop.IOLoop.current().run_sync(main)
