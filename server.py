"""
    Sample code for Multi-Threaded Server
    Python 3
    Usage: python3 TCPserver3.py localhost 12000
    coding: utf-8
    
    Author: Wei Song (Tutor for COMP3331/9331)
"""
import datetime
import os
from socket import *
from socket import timeout as TimeoutException
from threading import Thread
import argparse

from constants import *
from offline import Offline
from user import AttemptsExceededUsers, User

# acquire server host and port from command line parameter
parser = argparse.ArgumentParser()
parser.add_argument("server_port", type=int, help="port to operate on")

parser.add_argument("block_duration", type=int, help="Block Duration")

parser.add_argument("timeout", type=int, help="Timeout")

parser.add_argument("-d", action="store_true", help="debug")
args = parser.parse_args()

offline = Offline()
susUsers = AttemptsExceededUsers(args.block_duration)

serverHost = "127.0.0.1"
serverPort = args.server_port
timeout = args.timeout

MAX_ATTEMPTS = 3
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
        message = ""
        try:
            while self.clientAlive:
                try:
                    if self.isAuthenticated:
                        self.clientSocket.settimeout(timeout)
                    try:
                        message = self.recvFromClient()
                        cmd = message[0]
                    except TimeoutException:
                        self.processInactivity()

                    self.clientSocket.settimeout(None)

                    if not self.isAuthenticated:
                        self.processAuthentication(cmd)
                        self.processOfflineQueue()

                    # handle message from the client
                    elif cmd == MESSAGE:
                        self.processMessage(message)
                    elif cmd == BROADCAST:
                        self.processBroadcast(message)
                    elif cmd == BLOCK:
                        self.processBlock(message)
                    elif cmd == UNBLOCK:
                        self.processUnblock(message)
                    elif cmd == START_PRIVATE:
                        self.processPrivateRequest(message)
                    elif cmd == PRIVATE_REQUEST_ACCEPTED:
                        self.processInitiateP2P(message)
                    elif cmd == PRIVATE_REQUEST_DENIED:
                        self.processDeniedP2PRequest(message)
                    elif cmd == WHOELSE:
                        self.processWhoElse()
                    elif cmd == WHOELSESINCE:
                        self.processWhoElseSince(message)
                    elif cmd == LOGOUT:
                        self.processLogout()
                    else:
                        if cmd in REQUIRES_PRINT:
                            raise CustomExceptions(message)
                        raise CustomExceptions(INVALID_COMMAND)
                except CustomExceptions as e:
                    self.sendToClient(str(e))
                    if str(e) in COMMON_EXIT_EXCEPTIONS:
                        raise e

        except CustomExceptions as e:
            if args.d:
                print(str(e))
            if self.user and self.user.online:
                self.user.signOut()

    def sendToClient(self, command, payload=None, user=None):
        message = f"{command}"
        if user:
            message += f" {self.user.username}"

        if payload:
            message += f" {payload}"
        if not (self.clientSocket if not user else user.clientSocket):
            print(user.username)
        (self.clientSocket if not user else user.clientSocket).send(message.encode())

        if args.d:
            print(
                f"[send to {user.username if user else (self.user.username if self.user else '')}] {message} "
            )

    def processOfflineQueue(self):
        if self.isAuthenticated:

            msgs = offline.fetch(self.user.username)
            if len(msgs) > 0:
                self.sendToClient(OFFLINE)
            for msg in msgs:
                self.sendToClient(MESSAGE, msg)

    def processDeniedP2PRequest(self, message):
        if len(message) < 2:
            raise CustomExceptions(INVALID_INPUT)
        username = message[1]
        user = users.get(username)
        if not user.online:
            raise CustomExceptions(f"{USER_NOT_ONLINE} {username}")
        if user.authenticateP2PRequest(username):
            raise CustomExceptions(INVALID_INPUT)

        self.sendToClient(f"{PRIVATE_REQUEST_DENIED} {username}", None, user)
        self.user.acceptingP2PConnectionsWith = None

    def isRegistered(self, username):
        with open(CREDENTIALS_FILE, "r") as f:
            creds = f.readlines()
            for cred in creds:
                usr, _ = cred.split(" ")

                if usr == username:
                    return True
        return False

    def processInitiateP2P(self, message):
        if len(message) < 2:
            raise CustomExceptions(INVALID_INPUT)
        username = message[1]
        user = users.get(username)
        if not user.online:
            raise CustomExceptions(f"{USER_NOT_ONLINE} {username}")
        if user.authenticateP2PRequest(username):
            raise CustomExceptions(INVALID_INPUT)
        if self.user.username == username:
            raise CustomExceptions(OPERATION_NOT_ALLOWED_ON_SELF)

        addr, port = message[2:]
        payload = f"{addr} {port}"
        self.sendToClient(PRIVATE_REQUEST_ACCEPTED, payload, user)
        self.user.acceptingP2PConnectionsWith = None

    def recvFromClient(self, socket=None):
        msg = (socket or self.clientSocket).recv(BUFFER_SIZE).decode()
        msg = msg.split(" ")
        if args.d:
            print(f"[recv by {self.user.username if self.user else ''}] {msg}")
        return msg

    def processPrivateRequest(self, message):
        if len(message) < 4:
            raise CustomExceptions(INVALID_INPUT)

        username = message[1]
        user = users.get(username)
        if username == self.user.username:
            raise CustomExceptions(OPERATION_NOT_ALLOWED_ON_SELF)
        if not user:
            raise CustomExceptions(f"{USER_NOT_FOUND} {username}")
        if not user.online:
            raise CustomExceptions(f"{USER_NOT_ONLINE} {username}")

        addr, port = message[2:]
        self.sendToClient(PRIVATE_REQUEST, f"{addr} {port}", user)

    def processWhoElseSince(self, message):
        if len(message) < 2:
            raise CustomExceptions(INVALID_INPUT)

        time = int(message[1])
        date = datetime.datetime.now() - datetime.timedelta(seconds=time)
        payload = " ".join(
            [
                username
                for username in users
                if username != self.user.username
                and self.user.username not in users[username].blockedUserNames
                and self.user.activeSince > date
            ]
        )
        self.sendToClient(LIST_OF_OTHER_USERS_SINCE, payload)

    def processWhoElse(self):
        payload = " ".join(
            [
                username
                for username in users
                if username != self.user.username
                and self.user.username not in users[username].blockedUserNames
            ]
        )
        self.sendToClient(LIST_OF_OTHER_USERS, payload)

    def processUnblock(self, message):
        if len(message) < 2:
            raise CustomExceptions(INVALID_INPUT)
        username = message[1]
        if username == self.user.username:
            raise CustomExceptions(OPERATION_NOT_ALLOWED_ON_SELF)
        if username in self.user.blockedUserNames:
            self.user.blockedUserNames.remove(username)
            self.sendToClient(UNBLOCKED)
        else:
            raise CustomExceptions(f"{ALREADY_UNBLOCKED} {username}")

    def processBlock(self, message):
        if len(message) < 2:
            raise CustomExceptions(INVALID_INPUT)
        username = message[1]
        if username == self.user.username:
            raise CustomExceptions(OPERATION_NOT_ALLOWED_ON_SELF)
        if username in self.user.blockedUserNames:
            raise CustomExceptions(f"{ALREADY_BLOCKED} {username}")

        if self.isRegistered(username):
            self.user.blockedUserNames += [username]
            self.sendToClient(f"{BLOCKED} {username}")
        else:
            raise CustomExceptions(f"{USER_NOT_FOUND} {username}")

    def processBroadcast(self, message):
        for username in users:
            user = users[username]
            if (
                user.online
                and username != self.user.username
                and username not in user.blockedUserNames
            ):
                text = " ".join(message[1:])
                self.sendToClient(MESSAGE, text, user)

    def notifyAll(self, text):
        for username in users:
            user = users[username]
            if (
                user.online
                and username != self.user.username
                and username not in user.blockedUserNames
            ):
                self.sendToClient(NOTIFICATION, text, user)

    def processMessage(self, message):
        if len(message) < 3:
            raise CustomExceptions(INVALID_INPUT)
        username = message[1]

        if username == self.user.username:
            raise CustomExceptions(OPERATION_NOT_ALLOWED_ON_SELF)

        text = " ".join(message[2:])
        user = users.get(username)

        if not self.isRegistered(username):
            raise CustomExceptions(f"{USER_NOT_FOUND} {username}")
        if user and self.user.username in user.blockedUserNames:
            raise CustomExceptions(f"{USER_IS_BLOCKED} {username}")
        if not user or not user.online:
            offline.queue(username, f"{self.user.username} {text}")
            raise CustomExceptions(f"{OFFLINE_MESSAGE_DELIVERED} {username}")

        self.sendToClient(MESSAGE, text, user)

    def processLogout(self):
        self.notifyAll(lifePotion("User logged out.", self.user.username))
        raise CustomExceptions(LOGOUT)

    def initUser(self, username, password):
        user = users.get(username)
        if user and user.online:
            raise CustomExceptions(f"{ALREADY_ACTIVE} {username}")
        if not user:
            self.user = User(
                username,
                password,
                args.block_duration,
                self.clientSocket,
                self.clientAddress,
            )
            users[username] = self.user
        else:
            self.user = user

    def processInactivity(self):
        self.notifyAll(lifePotion("User timed out.", self.user.username))
        raise CustomExceptions(INACTIVITY)

    def processAuthentication(self, username):
        ## TODO validate username
        susUsers.checkBlocked(username)
        foundPassword = None
        user = users.get(username)
        if user and user.online:
            raise CustomExceptions(f"ALREADY_ACTIVE")

        if os.path.isfile(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, "r") as f:
                creds = f.readlines()
                for cred in creds:
                    usr, pwd = cred.split(" ")
                    pwd = pwd.replace("\n", "")
                    if usr == username:
                        foundPassword = pwd

        if not foundPassword:
            self.sendToClient(NEW_USER)
        else:
            self.sendToClient(FOUND_USER)

        password = self.recvFromClient()[0]
        if not foundPassword:
            with open(CREDENTIALS_FILE, "a") as f:
                f.write(f"{username} {password}\n")
            self.executeLogin(username, password)
        else:
            attempts = 1
            while True:
                if attempts == MAX_ATTEMPTS:
                    susUsers.block(username)

                if foundPassword == password:
                    self.executeLogin(username, password)
                    break
                else:
                    self.sendToClient(INVALID_CREDENTIALS)
                    password = self.recvFromClient()[0]
                    attempts += 1

        if self.isAuthenticated:
            self.notifyAll(lifePotion("User logged in.", username))

    def executeLogin(self, username, password):
        self.initUser(username, password)
        self.isAuthenticated = True
        self.user.signIn(self.clientSocket, self.clientAddress)
        self.sendToClient(AUTHENTICATED)


print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")

while True:
    serverSocket.listen()
    sock, address = serverSocket.accept()
    clientThread = ClientThread(address, sock)
    clientThread.start()
