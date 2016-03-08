__author__ = 'mytterland'

import socketserver
from ChatHandler import *
import json
import time
import datetime

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
        self.chatHandler.addConnection(self.connection)
        self.user = ''
        self.loggedin = False

        # Loop that listens for messages from the client
        while True:
            self.received_string = self.connection.recv(4096)
            self.received_string = self.received_string.decode()
            self.checkPayload()

            # TODO: Add handling of received payload from client

    def checkPayload(self):
        req = None
        cont = None
        #loggedin = False

        if type(self.received_string) != str:
            try:
                jrec = json.loads(self.received_string)
                req = jrec["request"].encode()
                cont = jrec["content"].encode()
            except TypeError or ValueError:
                print("Dette er ikke et JSON-objekt")

        else:
            jrec = json.loads(self.received_string)
            req = jrec["request"]
            cont = jrec["content"]

        if req == "login" and cont and not self.loggedin:
            self.user = cont
            if self.user not in self.chatHandler.getUsers():
                #self.chatHandler.addConnection(self.chatHandler)
                for i in self.chatHandler.getHistory():
                    self.connection.send(i.encode())
                    time.sleep(0.01)
                self.loggedin = True
                tid = time.time()
                now = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                response = {"timestamp": now, "sender": "Server", "response": "login", "content": "Suksessfull innlogging."}
                jsonresponse = json.dumps(response)
                self.connection.send(jsonresponse.encode())
                thread = self.chatHandler.getConnection()
                tid = time.time()
                thisTime = datetime.datetime.fromtimestamp(tid).strftime("%H:%M:%S")
                response = {"timestamp": thisTime, "sender": "Server", "response": "info", "content": self.user+" logget på!"}
                jsonresponse = json.dumps(response)
                for i in thread:
                    i.send(jsonresponse.encode())
                self.chatHandler.addUser(self.user)
            else:
                tid = time.time()
                now = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                response = {"timestamp": now, "sender": "Server", "response": "login", "content": "Brukernavnet er opptatt, vennligst velg et annet."}
                jsonresponse = json.dumps(response)
                self.connection.send(jsonresponse.encode())


        elif req == "logout" and self.loggedin and not cont:
            self.chatHandler.removeUser(self.user)
            self.chatHandler.removeConnection(self.connection)
            self.loggedin = False

            tid = time.time()
            now = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
            response = {"timestamp": now, "sender": "Server", "response": "logout", "content": "Suksessfull utlogging"}
            jsonresponse = json.dumps(response)
            self.connection.send(jsonresponse.encode())
            thread = self.chatHandler.getConnection()
            tid = time.time()
            thisTime = datetime.datetime.fromtimestamp(tid).strftime("%H:%M:%S")
            response = {"timestamp": thisTime, "sender": "Server", "response": "info", "content": self.user+" logget av!"}
            jsonresponse = json.dumps(response)
            for i in thread:
                i.send(jsonresponse.encode())

        elif req == 'history':
            for i in self.chatHandler.getHistory():
                    print(i)
                    self.connection.send(i.encode())
                    time.sleep(0.01)

        elif req == "msg" and cont:
            thread = self.chatHandler.getConnection()
            tid = time.time()
            thisTime = datetime.datetime.fromtimestamp(tid).strftime("%H:%M:%S")
            response = {"timestamp": thisTime, "sender": self.user, "response": "message", "content": cont}
            history = {"timestamp": thisTime, "sender": self.user, "response": "history", "content": cont}
            jsonresponse = json.dumps(response)
            jsonhistory = json.dumps(history)
            self.chatHandler.addHistory(jsonhistory)
            for i in thread:
                i.send(jsonresponse.encode())

        elif req == "names" and not cont:
            users = self.chatHandler.getUsers()
            userstring= json.dumps(users)
            tid = time.time()
            now = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
            response = {"timestamp": now, "sender": "Server", "response": "names", "content": userstring}
            jsonresponse = json.dumps(response)
            self.connection.send(jsonresponse.encode())

        elif req == "help" and not cont:
            tid = time.time()
            now = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
            response = {"timestamp": now, "sender": "Server", "response": "help", "content": "hjelpetekst"}
            jsonresponse = json.dumps(response)
            self.connection.send(jsonresponse.encode())

        else:
            tid = time.time()
            now = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
            response = {"timestamp": now, "sender": "Server", "response": "error", "content": "Noe ble feil. Prøv igjen eller skriv 'help' om du trenger hjelp."}
            jsonresponse = json.dumps(response)
            self.connection.send(jsonresponse.encode())

