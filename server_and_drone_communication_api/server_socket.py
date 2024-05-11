import socket

# Создаем сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_address = ('localhost', 10000)
sock.bind(server_address)

# Начинаем прослушивание входящих подключений
sock.listen(1)

while True:
    # Принимаем входящее подключение
    print('Waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('Connection from', client_address)

        # Получаем данные от клиента
        while True:
            data = connection.recv(1024)
            if data:
                print('Received "%s"' % data)

                # Отправляем ответ клиенту
                message = input('Enter your message: ')
                connection.sendall(message.encode())
            else:
                print('No more data from', client_address)
                break
    finally:
        # Закрываем соединение
        connection.close()
