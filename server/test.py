import tornado.ioloop
import tornado.web
import tornado.websocket
import json

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        self.clients.add(self)
        print("WebSocket opened")

    def on_message(self, message):
        data = json.loads(message)
        print("Received data:", data)
        for client in self.clients:
            if client != self:
                client.write_message(json.dumps(data))

    def on_close(self):
        self.clients.remove(self)
        print("WebSocket closed")

application = tornado.web.Application([
    (r'/ws', WebSocketHandler),
])

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
