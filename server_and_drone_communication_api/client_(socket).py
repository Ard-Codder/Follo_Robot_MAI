import socket

# Создаем сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
server_address = ('localhost', 10000)
sock.connect(server_address)

try:
    # Отправляем данные на сервер
    message = input('Enter your message: ')
    sock.sendall(message.encode())

    # Получаем ответ от сервера
    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print('Received "%s"' % data.decode('utf-8'))
finally:
    # Закрываем соединение
    sock.close()
