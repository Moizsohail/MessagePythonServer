"""
    Python 3
    Usage: python3 TCPClient3.py localhost 12000
    coding: utf-8
    
    Author: Wei Song (Tutor for COMP3331/9331)
"""
from socket import *
import sys
from threading import Thread

from constants import *
from p2p import P2P

# Server would be running on the same host as Client
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 TCPClient3.py SERVER_IP SERVER_PORT ======\n")
    exit(0)
serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
serverAddress = (serverHost, serverPort)

# define a socket for the client side, it would be used to communicate with the server
masterSocket = socket(AF_INET, SOCK_STREAM)
# build connection with the server and send message to it
masterSocket.connect(serverAddress)

p2p = P2P()

## Credentials
def sendToServer(message, p2p=None, payload=None):
    # if args.d:
    # print(f"[send] {message}")
    if payload:
        message += f" {payload}"
    (masterSocket if not p2p else p2p.client).send(message.encode())


def recvFromServer(p2p=None):
    msg = (
        (masterSocket if not p2p else p2p.server).recv(BUFFER_SIZE).decode().split(" ")
    )
    return msg


def authenticate(username):
    sendToServer(username)
    cmd = recvFromServer()[0]
    if cmd == NEW_USER:
        password = input("This is a new user. Enter a password: ")
    elif cmd == ALREADY_ACTIVE:
        print("The user is already online on another client")
        exit(0)
    else:
        password = input("Password: ")

    while True:
        sendToServer(password)
        cmd = recvFromServer()[0]
        ## TODO: Add blocking mech
        if cmd == AUTHENTICATED:
            break
        password = input("Invalid credentials. Enter a password: ")
    return username


username = input("Username: ")
authenticate(username)

print("Welcome to the greatest messaging application ever!")

startPrivateEvent = None


class KeyboardThread(Thread):
    def run(self):
        global startPrivateEvent
        while True:
            message = input("")
            cmd = message.split(" ")[0] if len(message.split(" ")) > 0 else ""
            if startPrivateEvent:
                if message.lower() in ["y", "yes"]:
                    sendToServer(
                        PRIVATE_REQUEST_ACCEPTED,
                        None,
                        f"{startPrivateEvent[0]} {p2p.addressAsString()}",
                    )
                    addr, port = startPrivateEvent[1:]
                    p2pConnectAddr = (addr, int(port))

                    p2p.connect(p2pConnectAddr, startPrivateEvent[0])
                    startPrivateEvent = None

                elif message.lower() in ["n", "no"]:
                    sendToServer(PRIVATE_REQUEST_DENIED, None, startPrivateEvent[0])
                    startPrivateEvent = None
                else:
                    print("Wrong Input. Try y or n")
            elif cmd == PRIVATE:
                msg = message.split(" ")
                if len(msg) < 3:
                    print("Invalid Command")
                elif not p2p.isClientConnected or msg[1] != p2p.connnectedWith:
                    print(f"Error. Private messaging to {msg[1]} not enabled")

                else:
                    sendToServer(message, p2p)
            elif cmd == START_PRIVATE:
                sendToServer(message, None, payload=p2p.addressAsString())
            elif cmd == STOP_PRIVATE:
                p2p.disconnect()
            else:
                sendToServer(message)


thread = KeyboardThread()
thread.daemon = True
thread.start()


class P2PServerThread(Thread):
    def __init__(self, p2p):
        Thread.__init__(self)
        self.p2p = p2p

    def run(self):
        self.p2p.acceptConnections()


p2pServerThread = P2PServerThread(p2p)
p2pServerThread.daemon = True
p2pServerThread.start()

while True:

    data = recvFromServer()
    cmd = data[0]

    if cmd == MESSAGE:
        print(f"{data[1]}: {' '.join(data[2:])}")

    elif cmd == LIST_OF_OTHER_USERS:
        if len(data[1:]) == 0:
            print("Nobody but you.")
        else:
            print("\n".join(data[1:]))

    elif cmd == PRIVATE_REQUEST:
        r = print("Do you want to initiate a private chat? (y/n)")
        startPrivateEvent = data[1:]
    elif cmd == PRIVATE_REQUEST_ACCEPTED:
        addr, port = data[2:]
        p2p.connect((addr, int(port)), data[1])
        print(f"{data[1]} accepts private messaging")

    elif cmd == LIST_OF_OTHER_USERS_SINCE:
        if len(data[1:]) == 0:
            print("Nobody but you.")
        else:
            print("\n".join(data[1:]))

    elif cmd == NOTIFICATION:
        print(" ".join(data[2:]))
    ## EXIT COMMANDS
    elif cmd in COMMON_EXIT_EXCEPTIONS:
        p2p.disconnect()
        print(MESSAGES[cmd])
        break

    elif cmd in REQUIRES_PRINT:
        print(MESSAGES[cmd])

    else:
        print("Message makes no sense")


# thread.stop()
masterSocket.close()
exit(0)
