#-*-coding:utf-8-*-

import socket
from threading import Thread


# 접속할 서버의 IP 주소, 포트 번호 - 서버에서 열어놓은 IP 와 PORT 가 같아야 연결 가능
HOST = 'localhost'
PORT = 8001

def rcvMsg(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            
            print data.decode()
        
        except Exception as e:
            print e

def runChat():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    t = Thread(target=rcvMsg, args=(sock,))
    t.daemon = True
    t.start()
    
    while True:
        msg = input()
        msg = str(msg)
        print msg
        
        if msg == '/quit':
            sock.send(msg.encode())
            break
        
        sock.send(msg.encode())

runChat()
