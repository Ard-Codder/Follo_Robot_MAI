import tornado

from communication_with_the_server import WebSocketClient

if __name__ == "__main__":
    client = WebSocketClient()


    async def main():
        ws_address = "ws://localhost:8888/obtaining_drone_data"
        await client.connect(ws_address)
        await client.send_data('5')
        await client.receive_data()

    tornado.ioloop.IOLoop.current().run_sync(main)

    client.disconnect()
    print('Client disconect')