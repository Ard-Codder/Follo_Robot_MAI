import tornado.websocket

clients = []


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        if self not in clients:
            clients.append(self)
            print("New client connected")

    def on_message(self, message):
        for client in clients:
            client.write_message(message)

    def on_close(self):
        if self in clients:
            clients.remove(self)
            print("Client disconnected")
