from socket import *
from threading import Thread
from constants import *


def sendToServer(message, p2p, payload=None):
    # if args.d:
    # print(f"[send] {message}")
    if payload:
        message += f" {payload}"
    (p2p.client).send(message.encode())


class P2P:
    def __init__(self):

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(("", 0))
        hostname = gethostname()
        localIp = gethostbyname(hostname)
        self.address = localIp, self.server.getsockname()[1]
        self.client = None
        self.isClientConnected = False
        self.connnectedWith = None

    def connect(self, addr, username):
        if not self.isClientConnected:
            self.connnectedWith = username
            self.client = socket(AF_INET, SOCK_STREAM)
            self.client.connect(addr)
            self.isClientConnected = True
        else:
            print(f"Cannot connect! Already paired with {self.connnectedWith}")

    def addressAsString(self):
        ip, port = self.address
        return f"{ip} {port}"

    def disconnect(self):
        if self.client:
            self.client.close()
        if self.connnectedWith:
            print(f"Disconnecting private connection with {self.connnectedWith}")
        self.isClientConnected = False
        self.connnectedWith = None

    def acceptConnections(self):
        while True:
            self.server.listen()
            sock, address = self.server.accept()
            clientThread = ClientThread(address, sock, self.disconnect, self)
            clientThread.start()


def recvFromServer(clientSocket):
    msg = clientSocket.recv(BUFFER_SIZE).decode().split(" ")
    return msg


class ClientThread(Thread):
    def __init__(self, clientAddress, clientSocket, detachClbk, p2p):
        Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSocket = clientSocket
        self.detachClbk = detachClbk
        self.p2p = p2p

    def run(self):
        self.clientSocket.settimeout(120)
        try:
            while True:
                message = recvFromServer(self.clientSocket)
                if message[0] == "":
                    break
                if message[0] == STOP_PRIVATE:
                    self.detachClbk()
                    break
                elif message[0] in COMMON_EXIT_EXCEPTIONS:
                    self.detachClbk()
                    break
                if len(message) != 3:
                    break           
                text = " ".join(message[2:])
                username = message[1]
                print(f"{username}(private): {text}")
        except timeout:

            print("P2P connection is inactive for too long")
            sendToServer(INACTIVITY, self.p2p)
            self.detachClbk()
