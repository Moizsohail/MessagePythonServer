"""
    Python 3
    Usage: python3 TCPClient3.py localhost 12000
    coding: utf-8
    
    Author: Wei Song (Tutor for COMP3331/9331)
"""
from socket import *
import sys
from threading import Event, Thread
from types import resolve_bases

from constants import *

# Server would be running on the same host as Client
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 TCPClient3.py SERVER_IP SERVER_PORT ======\n")
    exit(0)
serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
serverAddress = (serverHost, serverPort)

# define a socket for the client side, it would be used to communicate with the server
clientSocket = socket(AF_INET, SOCK_STREAM)
# build connection with the server and send message to it
clientSocket.connect(serverAddress)

## Credentials


def sendToServer(message):
    # if args.d:
    print(f"[send] {message}")
    clientSocket.send(message.encode())


def recvFromServer():
    msg = clientSocket.recv(BUFFER_SIZE).decode().split(" ")
    # if args.d:
    print(f"[recv] {msg}")
    return msg


username = input("Username: ")
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
    if cmd == AUTHENTICATED:
        break
    password = input("Invalid credentials. Enter a password: ")


print("Welcome to the greatest messaging application ever!")


class RespondingThread(Thread):
    def run(self):
        while True:
            message = input("")
            sendToServer(message)


thread = RespondingThread()
thread.daemon = True
thread.start()


while True:

    data = recvFromServer()
    cmd = data[0]

    # parse the message received from server and take corresponding actions
    if cmd == "":
        print("[recv] Message from server is empty!")

    elif cmd == MESSAGE:
        print(f"{data[1]}: {' '.join(data[2:])}")

    elif cmd == LIST_OF_OTHER_USERS:
        if len(data[1:]) == 0:
            print("Nobody but you.")
        else:
            print("\n".join(data[1:]))

    elif cmd == LIST_OF_OTHER_USERS_SINCE:
        if len(data[1:]) == 0:
            print("Nobody but you.")
        else:
            print("\n".join(data[1:]))

    ## EXIT COMMANDS
    elif cmd in COMMON_EXIT_EXCEPTIONS:
        print(MESSAGES[cmd])
        break

    elif cmd in REQUIRES_PRINT:
        print(MESSAGES[cmd])

    else:
        print("[recv] Message makes no sense")


# thread.stop()
clientSocket.close()
exit(0)
