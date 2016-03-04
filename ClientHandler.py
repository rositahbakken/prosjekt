__author__ = 'mytterland'

import socketserver
import ChatHandler
import json

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    chatHandler = ChatHandler()

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            self.received_string = self.connection.recv(4096)
            self.checkPayload()

            # TODO: Add handling of received payload from client

    def checkPayload(self):
    #     self.recieved_string = self.received_string.split(',')
    #     if self.recieved_string[0].matches("'request': <"+"login"+">") and self.received_string[1].matches("'content': <"+"[a-zA-z0-9_]+"+">"):
    #         username = self.received_string[1][11:self.received_string[1].length - 1]
    #         if username not in self.chatHandler.getActive_users():
    #             self.chatHandler.addUser(username)
    #             print(self.chatHandler.getHistory())
    #         else:
    #             print("brukernavnet er tatt, velg et annet")
    #
    #
    #     if self.recieved_string[0].matches("'request': <"+"logout"+">") and not self.received_string[1][11:self.received_string[1].length - 1]:
    #         self.chatHandler.removeUser()
        req = None
        cont = None

        if type(self.received_string) != str:
            try:
                jrec = json.loads(self.received_string)
                req = jrec["request"].encode()
                cont = jrec["content"].encode()
            except ValueError:
                print("Dette er ikke et JSON-objekt")

        else:
            jrec = json.loads(self.received_string)
            req = jrec["request"]
            cont = jrec["content"]

        if req == "login" and cont:
            user = cont
            if user not in self.chatHandler.getUsers():
                self.chatHandler.addUser(user)
                self.chatHandler.addConnection(self.chatHandler)
                print(self.chatHandler.getHistory())
            else:
                print("Brukernavnet er opptatt, velg et annet.")

        if req == "logout" and not cont:
            self.chatHandler.removeUser()
            self.chatHandler.removeConnection(self.chatHandler)

        if req == "msg" and cont:
            self.chatHandler.addHistory()
            self.connection.send(cont)

        if req == "names" and not cont:
            print(self.chatHandler.getUsers())

        if req == "help" and not cont:
            print("hjelpetext")


