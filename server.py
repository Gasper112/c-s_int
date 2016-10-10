#-*- coding:utf-8 -*-

import socket

sock = socket.socket()
sock.bind(('127.0.0.1',9090))
sock.listen(10)
conn, adr = sock.accept()

print ('connected:',adr)

while True:
    data = conn.recv(8000)
    print (data)

    if data == b'regdatade5ca21bdd336e242f3aac2875c9d297':
        conn.send(b'True')
        break
    else:
        conn.send(b'False')

    if not data:
        break



conn.close()
