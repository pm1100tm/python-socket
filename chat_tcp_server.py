#-*-coding:utf-8-*-

import SocketServer
import threading

HOST = 'localhost'  # 서버의 ip 열기 (이 서버의 ip 로 클라이언트가 접속을 해야 함) 그 전에 ping 을 먼저 확인하도록
PORT = 8001
lock = threading.Lock()


class UserManager:
    """ 사용자 관리 및 채팅 메시지 전송을 담당하는 클래스
        1. 채팅 서버로 입장한 사용자의 등록
        2. 채팅을 종료하는 사용자의 퇴장 관리
        3. 사용자가 입장하고 퇴장하는 관리
        4. 사용자가 입력한 메시지를 채팅 서버에 접속한 모두에게 전송
    """
    
    def __init__(self):
        # 사용자의 등록 정보를 담을 객체 {사용자이름 : (소켓, 주소), ...}
        self.users = {}
    
    def addUser(self, username, conn, addr):
        """ 사용자 ID를 self.users 에 추가하는 함수
            :param username: 유저명
            :param conn: 접속 객체
            :param addr: 호스트
            :return: username 등록한 사용자 명
        """
        if username in self.users:
            conn.send('이미 등록된 사용자입니다\n'.encode())
            return None
        
        # 새로운 사용자 등록함. 쓰레드 동기화를 막기위한 락. 업데이트 후 락 해제
        lock.acquire()
        self.users[username] = (conn, addr)
        lock.release()
        
        self.sendMessageToAll('[%s]님이 입장했습니다.' % username)
        print '+++ 대화 참여자 수 [%d]' % len(self.users)
        
        return username
    
    def removeUser(self, username):
        """ 사용자 ID 를 self.users 에서 제거하는 함수
            :param username: 유저 명
            :return: -
        """
        if username not in self.users:
            return
        
        lock.acquire()
        del self.users[username]
        lock.release()
        
        self.sendMessageToAll('[%s]님이 퇴장했습니다.' % username)
        print '--- 대화 참여자 수 [%d]' % len(self.users)
        
    def messageHandler(self, username, msg):
        """ 전송한 msg를 처리하는 함수
            :param username:
            :param msg:
            :return:
        """
        if msg[0] != '/':  # 보낸 메세지의 첫문자가 / 가 아니면
            self.sendMessageToAll('[%s] %s' % (username, msg))
            return
        
        if msg.strip() == '/quit':  # 보낸 메세지가 quit 이면
            self.removeUser(username)
            return -1
        
    def sendMessageToAll(self, msg):
        """ 채팅방에 참여한 모든 유저들에게 메세지를 보내는 함수
            :param msg: 메세지
            :return: -
        """
        for conn, addr in self.users.values():
            conn.send(msg.encode())


class MyTcpHandler(SocketServer.BaseRequestHandler):
    # UserManager() 객체 생성
    userman = UserManager()
    
    def handle(self):
        """ 클라이언트가 접속시 클라이언트 주소 출력
        :return: -
        """
        print '[%s] 연결됨' % self.client_address[0]
        
        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            print msg + '==============================================================='
            
            while msg:
                print msg.decode()
                print msg + '==============================================================='
                
                if self.userman.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                
                msg = self.request.recv(1024)
                
        except Exception as e:
            print e
        
        print '[%s] 접속종료' % self.client_address[0]
        self.userman.removeUser(username)
        
    def registerUsername(self):
        while True:
            self.request.send('로그인 ID:'.encode())
            user_name = self.request.recv(1024)
            user_name = user_name.decode().strip()
            
            if self.userman.addUser(user_name, self.request, self.client_address):
                print 'registerUsername ok' + user_name
                return user_name


class ChattingServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def runServer():
    print '+++ 채팅 서버를 시작합니다.'
    print '+++ 채텅 서버를 끝내려면 Ctrl-C를 누르세요.'
    
    try:
        server = ChattingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
        
    except KeyboardInterrupt:
        print '--- 채팅 서버를 종료합니다.'
        server.shutdown()
        server.server_close()
        
runServer()
