import socket
import os
def sendFile():
        sock = socket.socket()
        addr="77.37.196.166"
        port=8000
        data="admin"
        try:
            sock.connect((addr,port))
            sock.send(data.encode("utf-8"))
            data = sock.recv(1024).decode()
            print(data)
            if data=="none":
                 os.system("touch /home/admin/t.t")
            sock.close()
        except Exception as exc:
            print(exc)
            error = 'ошибка номер ....'
            print("ошибка с текстом, строка, линия и т.п. тип ошибки(что пишет компилятор): "+str(error))
            
sendFile()
