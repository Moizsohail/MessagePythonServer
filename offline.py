class Offline:
    def __init__(self):
        self.map = {}

    def queue(self, username, message):
        entry = self.map.get(username)
        if not entry:
            self.map[username] = [message]
        else:
            self.map[username].append(message)

    def fetch(self, username):
        messages = self.map.get(username) or []
        self.map = {}
        return messages
