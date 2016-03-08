__author__ = 'macsita'

class ChatHandler:

    connections = []
    #active_users = []
    #chat_history = []

    def __init__(self): # ( active_users, chat_history)
        self.active_users = [] #= active_users
        self.chat_history = [] #chat_history
        #self.this_user = None


    def addUser(self, user):
        self.active_users.append(user)

    def removeUser(self, this_user):
        self.active_users.remove(this_user)


    def addHistory(self, chat_line):
        self.chat_history.append(chat_line)

    def deleteHistory(self):
        self.chat_history = []

    def getUsers(self):
        return self.active_users

    def getHistory(self):
        return self.chat_history

    def addConnection(self, conn):
        self.connections.append(conn)

    def getConnection(self):
        return self.connections

    def removeConnection(self, chatHandler):
        self.connections.remove(chatHandler)




