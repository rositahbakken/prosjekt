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
        req = None
        cont = None
        loggedin = False
        user = ''

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

        if req == "login" and cont and not loggedin:
            user = cont
            if user not in self.chatHandler.getUsers():
                self.chatHandler.addUser(user)
                self.chatHandler.addConnection(self.chatHandler)
                print(self.chatHandler.getHistory())
                print(user+" logged in!")
                self.loggedin = True
            else:
                print("Brukernavnet er opptatt, velg et annet.")

        elif req == "logout" and loggedin and not cont:
            self.chatHandler.removeUser()
            self.chatHandler.removeConnection(self.chatHandler)
            self.loggedin = False
            user = ''
            print(self.chatHandler.getActiveUser()+" logged out!")

        elif req == "msg" and cont:
            self.chatHandler.addHistory()
            self.connection.send(cont)

        elif req == "names" and not cont:
            print(self.chatHandler.getUsers())

        elif req == "help" and not cont:
            print("hjelpetext")

        else:
            print("Noe ble feil. Prøv igjen eller skriv 'help' om du trenger hjelp.")

