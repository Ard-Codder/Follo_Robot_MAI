import tornado.ioloop
import tornado.websocket


class WebSocketClient():
    def __init__(self):
        self.ws = None

    async def connect(self, ws_address):
        try:
            self.ws = await tornado.websocket.websocket_connect(ws_address)
            print("Connected to server")
        except tornado.httpclient.HTTPClientError as e:
            print("Error connecting to the server:", e)

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
