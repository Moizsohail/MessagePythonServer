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
from user import User

# acquire server host and port from command line parameter
parser = argparse.ArgumentParser()
parser.add_argument('server_port',
                       type=int,
                       help='port to operate on')

parser.add_argument('block_duration',
                       type=int,
                       help='Block Duration')

parser.add_argument('timeout',
                       type=int,
                       help='Timeout')

parser.add_argument('-d', action='store_true',help="debug")
args = parser.parse_args()


serverHost = "127.0.0.1"
serverPort = args.server_port
serverAddress = (serverHost, serverPort)

# define socket for the server side and bind address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)

users = {}

class ClientThread(Thread):
    def __init__(self, clientAddress, clientSocket):
        Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSocket = clientSocket
        self.clientAlive = False
        self.isAuthenticated = False
        self.user = None
        print("===== New connection created for: ", clientAddress)
        self.clientAlive = True
        
    def run(self):
        message = ''
        try:
            while self.clientAlive:
                
                self.clientSocket.settimeout(10000)
                try:
                    message = self.recvFromClient()
                    cmd = message[0]
                except timeout:
                    self.processInactivity()
                    
                self.clientSocket.settimeout(None)


                if not self.isAuthenticated:
                    self.processAuthentication(cmd)
                
                # handle message from the client
                elif cmd == MESSAGE:
                    self.processMessage(message)
                elif cmd == WHOELSE:
                    self.processWhoElse()
                elif cmd == LOGOUT:
                    self.processLogout()
                
        
        except CustomExceptions as e:
            if str(e) in COMMON_EXIT_EXCEPTIONS and self.user:
                del users[self.user.username]
            self.sendToClient(str(e))
 
    def sendToClient(self,command,payload=None,username=None):
        message = f"{command}"
        if not username:
            if payload:
                message += f" {payload}"
            self.clientSocket.send(message.encode())
        else:
            user = users.get(username)
            if not user:
                raise CustomExceptions(USER_NOT_FOUND)
            message += f" {self.user.username}"
            if payload:
                message += f" {payload}"
            user.clientSocket.send(message.encode())
        if args.d:
            print(f"[send] {message} ")

    def recvFromClient(self):
        msg = self.clientSocket.recv(BUFFER_SIZE).decode()
        msg = msg.split(" ")
        if args.d:
            print(f"[recv] {msg}")
        return msg

    def processMessage(self,message):
        username = message[1]
        text = " ".join(message[2:])
        self.sendToClient(MESSAGE,text,username)
    
    def processWhoElse(self):
        payload = " ".join([username for username in users if username != self.user.username])
        self.sendToClient(LIST_OF_OTHER_USERS,payload)

    def processLogout(self):
        raise CustomExceptions(LOGOUT)

    def initUser(self,username,password):
        if users.get(username):
            raise CustomExceptions(ALREADY_ACTIVE)
        
        self.user = User(username,password,args.block_duration,self.clientSocket)
        users[username] = self.user
        
    def processInactivity(self):
        raise CustomExceptions(INACTIVITY)

    def processAuthentication(self,username):
        ## TODO validate username
        foundPassword = None
        if users.get(username):
            raise CustomExceptions(ALREADY_ACTIVE)

        if os.path.isfile(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE,'r') as f:
                creds = f.readlines()
                for cred in creds:
                    usr,pwd = cred.split(" ")
                    pwd = pwd.replace("\n","")
                    if usr == username:
                        foundPassword = pwd
        
        if not foundPassword:
            self.sendToClient(NEW_USER)
        else:
            self.sendToClient(FOUND_USER)

        password = self.recvFromClient()[0]
        if not foundPassword:
            with open(CREDENTIALS_FILE,'a') as f:
                f.write(f"{username} {password}\n")
            self.sendToClient(AUTHENTICATED)
            self.initUser(username,password)
            self.isAuthenticated = True
        else:
            while True:
                if foundPassword == password:
                    self.isAuthenticated = True
                    self.sendToClient(AUTHENTICATED)
                    self.initUser(username,password)
                    break
                else:
                    self.sendToClient(INVALID_CREDENTIALS)
                    password = self.recvFromClient()[0]
                    

        
    

print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")


while True:
    serverSocket.listen()
    clientSockt, clientAddress = serverSocket.accept()
    clientThread = ClientThread(clientAddress, clientSockt)
    clientThread.start()
