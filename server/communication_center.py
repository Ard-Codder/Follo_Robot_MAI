import tornado
from obtaining_drone_data import WebSocketHandler

def make_app():
    return tornado.web.Application([
        (r"/obtaining_drone_data", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("WebSocket server started")
    tornado.ioloop.IOLoop.current().start()