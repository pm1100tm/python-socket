#-*-coding:utf-8-*-
import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 접속할 서버의 ip 주소와 포트번호를 설정
socket.connect(('localhost', 8000))

# 전송할 데이터를 보냄
for i in range(1, 10):
    socket.send('hello'.encode())
