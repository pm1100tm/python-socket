#-*-coding:utf-8-*-

# 소켓을 사용하기 위해서는 socket 을 import
# 로컬은 127.0.0.1의 ip로 접속한다.
import socket
HOST = '127.0.0.1'

# port 는 위 서버에서 설정한 9999로 접속을 한다.
PORT = 9999

# 소켓을 만든다.
# connect 함수로 접속을 한다.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 10번의 루프로 send receive 를 한다.
for i in range(1, 10):
    # 메시지는 hello 로 보낸다.
    msg = 'hello'
    
    # 메시지를 바이너리 형식으로 변환한다.
    data = msg.encode()
    length = len(data)
    
    # server 로 리플 엔디언 형식으로 데이터 길이를 전송한다.
    client_socket.sendall(length.to_bytes(4, byteorder='little'))
    
    # 데이터를 전송한다.
    client_socket.sendall(data)

    data = client_socket.recv(4)
    length = int.from_bytes(data, "little")

    # 데이터 길이를 받는다.
    data = client_socket.recv(length);
    
    # 데이터를 수신한다.
    msg = data.decode();
    
    # 데이터를 출력한다.
    print 'Received from : ', msg

client_socket.close();