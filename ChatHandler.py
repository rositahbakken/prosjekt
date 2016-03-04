__author__ = 'macsita'

class ChatHandler:

    this_user = None
    connections = []
    active_users = []
    chat_history = []

    def __init__(self, active_users, chat_history):
        self.active_users = active_users
        self.chat_history = chat_history


    def addUser(self, user):
        self.active_users.add(user)
        self.this_user = user

    # def removeUser(self):
    #     self.active_users.remove(self.this_user)
    #     self.this_user = None

    def addHistory(self, chat_line):
        self.chat_history.add(chat_line)

    def deleteHistory(self):
        self.chat_history = []

    def getUsers(self):
        return self.active_users

    def getHistory(self):
        return self.chat_history

    def getActiveUser(self):
        return self.this_user

    def addConnection(self, chatHandler):
        self.connections.append(chatHandler)

    def removeConnection(self, chatHandler):
        self.connections.remove(chatHandler)

