import argparse
from socket import *
from threading import Thread

from constants import *
from p2p import P2P


parser = argparse.ArgumentParser()
parser.add_argument("server_addr", type=str, help="port to operate on")

parser.add_argument("server_port", type=int, help="Block Duration")

args = parser.parse_args()

serverHost = args.server_addr
serverPort = args.server_port
serverAddress = (serverHost, serverPort)

# define a socket for the client side, it would be used to communicate with the server
masterSocket = socket(AF_INET, SOCK_STREAM)
# build connection with the server and send message to it
masterSocket.connect(serverAddress)


## Credentials
def sendToServer(message, p2p=None, payload=None):
    # if args.d:
    # print(f"[send] {message}")
    if payload:
        message += f" {payload}"
    (masterSocket if not p2p else p2p.client).send(message.encode())


p2p = P2P()


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
                if p2p.isClientConnected:
                    sendToServer(STOP_PRIVATE, p2p)
                    p2p.disconnect()
                else:
                    print("You need to be connected first to disconnect.")

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
        if p2p.isClientConnected:
            sendToServer(ALREADY_CONNECTED, None, p2p.connnectedWith)
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
        if p2p.isClientConnected:
            sendToServer(cmd, p2p)
        p2p.disconnect()
        displayMessage(data)
        break

    elif cmd in REQUIRES_PRINT:
        displayMessage(data)

    else:
        print("Message makes no sense")


# thread.stop()
masterSocket.close()
exit(0)
