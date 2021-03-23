#-*-coding:utf-8-*-
import socket
import threading

def binder(client_socket, addr):
    # binder 함수는 서버에서 accept 가 되면 생성되는 socket 인스턴스를 통해 client 로 부터 데이터를 받으면 echo 형태로 재송신하는 메서드
    # 커넥션이 되면 접속 주소가 나온다
    print 'connected by', addr
    
    try:
        # 접속 상태에서는 클라이언트로부터 받을 데이터를 무한 대기.
        # 최초 4 바이트를 대기한다.
        data = client_socket.recv(4)
        
        # 최소 4 바이트는 전송할 데이터의 크기.
        # 그 크기는 little 앤디언으로 byte 에서 int 형식으로 변환한다.
        length = int.from_byte(data, 'little')
        
        # 다시 데이터를 수신
        data = client_socket.recv(length)
        
        # 수신 된 데이터를 str 형식으로 decode, 메시지를 콘솔에 출력, 수신 된 메세지 앞에 echo 를 붙인다.
        msg = data.decode()
        print 'received from', addr, msg
        msg = 'echo : ' + msg
        
        # 바이너리(byte) 형식으로 변환한다, 바이너리 데이터의 사이즈를 구한다.
        data = msg.encode()
        length = len(data)
        
        client_socket.sendall(length.to_bytes(4, byteorder='little'))
        
        # 데이터를 클라이언트로 전송한다.
        client_socket.sendall(data)
        
    except Exception as e:
        # 접속이 끊기면 except 가 발생한다
        print 'except: ', addr
    
    finally:
        # 접속이 끊기면 socket 리소스를 닫는다.
        client_socket.close()

# 소켓을 만든다
# 소켓 레벨과 데이터 형태를 설정한다.
# 서버는 복수 ip를 사용하는 pc의 경우는 ip를 지정하고 그렇지 않으면 None 이 아닌 ''로 설정한다.
# 포트는 pc 내에서 비어있는 포트를 사용한다. cmd 에서 netstat -an | find "LISTEN"으로 확인할 수 있다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 9999))
server_socket.listen(5)

try:
    # 서버는 여러 클라이언트를 상대하기 때문에 무한 루프를 사용한다.
    while True:
        # client 로 접속이 발생하면 accept 가 발생한다.
        # 그럼 client 소켓과 addr(주소)를 튜플로 받는다.
        client_socket, addr = server_socket.accept()
        
        # 쓰레드를 이용해서 client 접속 대기를 만들고 다시 accept 로 넘어가서 다른 client 를 대기한다.
        th = threading.Thread(target=binder, args=(client_socket, addr))
        th.start()
        
except Exception as e:
    print 'server'
    
finally:
    # 에러가 발생하면 서버 소켓을 닫는다.
    server_socket.close();
