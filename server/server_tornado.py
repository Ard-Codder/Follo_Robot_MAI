import tornado.ioloop
import tornado.web
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

def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("WebSocket server started")
    tornado.ioloop.IOLoop.current().start()
