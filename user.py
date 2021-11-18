import datetime

from constants import TOO_MANY_ATTEMPTS, CustomExceptions


class User:
    def __init__(self, username, password, block_duration, clientSocket, clientAddress):
        self.username = username
        self.password = password
        self.blockDuration = block_duration
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.activeSince = datetime.datetime.now()
        self.blockedUserNames = []
        self.acceptingP2PConnectionsWith = None
        self.online = False

    def signIn(self, clientSocket, clientAddress):
        self.online = True
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress

    def signOut(self):
        self.online = False
        self.clientAddress = None
        self.acceptingP2PConnectionsWith = None
        if self.clientSocket:
            self.clientSocket.close()
            self.clientSocket = None

    def authenticateP2PRequest(self, username):
        return self.acceptingP2PConnectionsWith == username


class AttemptsExceededUsers:
    def __init__(self, blockDuration):
        self.data = {}
        self.blockDuration = blockDuration

    def block(self, username):
        self.data = {
            username: datetime.datetime.now()
            + datetime.timedelta(seconds=self.blockDuration)
        }
        raise CustomExceptions(TOO_MANY_ATTEMPTS)

    def checkBlocked(self, username):
        time = self.data.get(username)
        now = datetime.datetime.now()
        if time and time >= now:
            raise CustomExceptions(TOO_MANY_ATTEMPTS)
