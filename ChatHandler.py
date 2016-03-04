__author__ = 'macsita'

class ChatHandler:

    def __init__(self, active_users, chat_history):
        self.active_users = active_users
        self.chat_history = chat_history


    def addUser(self, user):
        self.active_users.add(user)

    def removeUser(self, user):
        self.active_users.remove(user)

    def addHistory(self, chat_line):
        self.chat_history.remove(chat_line)

    def deleteHistory(self):
        self.chat_history = []


