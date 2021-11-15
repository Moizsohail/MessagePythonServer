import datetime


class User:
    def __init__(self, username, password, block_duration, clientSocket, clientAddress):
        self.username = username
        self.password = password
        self.blockDuration = block_duration
        self.blockedTill = None
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.isActive = True
        self.activeSince = datetime.datetime.now()
        self.blockedUserNames = []
        self.acceptingP2PConnectionsWith = None

    def authenticateP2PRequest(self, username):
        return self.acceptingP2PConnectionsWith == username

    def is_blocked(self):
        if not self.blockedTill:
            return True
