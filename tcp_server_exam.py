#-*-coding:utf-8-*-
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ip 주소, 포트번호 지정
server_socket.bind(('localhost', 8000))

# 클라이언트의 요청을 기다리는 상태
server_socket.listen(0)

# 클라이언트의 요청을 수락함. IP, PORT 등 데이터를 리턴함
client_socket, addr = server_socket.accept()

# 클라이언트로 데이터를 받음. 출력되는 버퍼 사이즈 (만약 2를 하면, 2개의 데이터만 전송됨)
data = client_socket.recv(65535)

# 받은데이터를 해석함.
print '받은 데이터', data.decode()
