import tornado
from communication_with_the_server import WebSocketClient

client = WebSocketClient()


async def main():
    ws_address = "ws://localhost:8888/obtaining_drone_data"
    await client.connect(ws_address)
    await client.send_data('5')
    await client.receive_data()
    print('Client disconnect')
    tornado.ioloop.IOLoop.current().stop()


async def run_main():
    await main()
    tornado.ioloop.IOLoop.current().stop()


tornado.ioloop.IOLoop.current().add_callback(run_main)
tornado.ioloop.IOLoop.current().start()
