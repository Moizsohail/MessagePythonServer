import datetime
class User:
    def __init__(self,username,password,block_duration,clientSocket):
        self.username = username
        self.password = password
        self.blockDuration = block_duration
        self.blockedTill = None
        self.clientSocket = clientSocket
        self.isActive = True
        self.activeSince = datetime.datetime.now()
        self.blockedUserNames = []

    def is_blocked(self):
        if not self.blockedTill:
            return True
    
    