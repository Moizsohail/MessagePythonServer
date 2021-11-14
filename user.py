class User:
    def __init__(self,username,password,block_duration,clientSocket):
        self.username = username
        self.password = password
        self.blockDuration = block_duration
        self.blockedTill = None
        self.clientSocket = clientSocket
        self.isActive = True
    def is_blocked(self):
        if not self.blockedTill:
            return True
    
    