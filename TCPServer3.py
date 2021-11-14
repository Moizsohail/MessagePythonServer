"""
    Sample code for Multi-Threaded Server
    Python 3
    Usage: python3 TCPserver3.py localhost 12000
    coding: utf-8
    
    Author: Wei Song (Tutor for COMP3331/9331)
"""
import os
from socket import *
from threading import Thread
import argparse

from constants import *

# acquire server host and port from command line parameter
parser = argparse.ArgumentParser()
parser.add_argument('port',
                       type=int,
                       help='port to operate on')
parser.add_argument('-d', action='store_true',help="debug")
args = parser.parse_args()
print(args)

serverHost = "127.0.0.1"
serverPort = args.port
serverAddress = (serverHost, serverPort)

# define socket for the server side and bind address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)

"""
    Define multi-thread class for client
    This class would be used to define the instance for each connection from each client
    For example, client-1 makes a connection request to the server, the server will call
    class (ClientThread) to define a thread for client-1, and when client-2 make a connection
    request to the server, the server will call class (ClientThread) again and create a thread
    for client-2. Each client will be runing in a separate therad, which is the multi-threading
"""
class ClientThread(Thread):
    def __init__(self, clientAddress, clientSocket):
        Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSocket = clientSocket
        self.clientAlive = False
        self.isAuthenticated = False
        
        print("===== New connection created for: ", clientAddress)
        self.clientAlive = True
        
    def run(self):
        message = ''
        
        while self.clientAlive:
            # use recv() to receive message from the client
            
            message = self.recvFromClient()

            if not self.isAuthenticated:
                self.process_authentication(message)
                continue
            # if the message from client is empty, the client would be off-line then set the client as offline (alive=Flase)
            if message == '':
                self.clientAlive = False
                print("===== the user disconnected - ", clientAddress)
                break
            
            # handle message from the client
            if message == 'login':
                print("[recv] New login request")
                self.process_login()
            elif message == 'download':
                print("[recv] Download request")
                message = 'download filename'
                print("[send] " + message)
                self.clientSocket.send(message.encode())
            else:
                print("[recv] " + message)
                print("[send] Cannot understand this message")
                message = 'Cannot understand this message'
                self.clientSocket.send(message.encode())
    
    """
        You can create more customized APIs here, e.g., logic for processing user authentication
        Each api can be used to handle one specific function, for example:
        def process_login(self):
            message = 'user credentials request'
            self.clientSocket.send(message.encode())
    """
    def sendToClient(self,command):
        if args.d:
            print(f"[send] {command}")
        self.clientSocket.send(command.encode())
    def recvFromClient(self):
        msg = self.clientSocket.recv(BUFFER_SIZE).decode()
        if args.d:
            print(f"[recv] {msg}")
        return msg

    def process_authentication(self,username):
        
        ## TODO validate username
        foundPassword = None
        if os.path.isfile(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE,'r') as f:
                creds = f.readlines()
                for cred in creds:
                    print(cred)
                    usr,pwd = cred.split(" ")
                    if usr == username:
                        foundPassword = pwd
        
        if not foundPassword:
            self.sendToClient(NEW_USER)
        else:
            self.sendToClient(FOUND_USER)

        password = self.recvFromClient()
        if not foundPassword:
            with open(CREDENTIALS_FILE,'a') as f:
                f.write(f"{username} {password}")
            self.sendToClient(AUTHENTICATED)
        else:
            if foundPassword == password:
                self.isAuthenticated = True
                self.sendToClient(AUTHENTICATED)
            else:
                self.sendToClient(INVALID_CREDENTIALS)

        
    

print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")


while True:
    serverSocket.listen()
    clientSockt, clientAddress = serverSocket.accept()
    clientThread = ClientThread(clientAddress, clientSockt)
    clientThread.start()
