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

        # Loop that listens for messages from the client
        while True:
            self.received_string = self.connection.recv(4096)
            self.received_string = self.received_string.decode()
            self.checkPayload()

            # TODO: Add handling of received payload from client

    def checkPayload(self):
        req = None
        cont = None
        loggedin = False

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

        if req == "login" and cont and not loggedin:
            self.user = cont
            if self.user not in self.chatHandler.getUsers():
                self.chatHandler.addUser(self.user)
                #self.chatHandler.addConnection(self.chatHandler)
                tid = time.time()
                now = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                response = {"timestamp": now, "sender": "Server", "response": "login", "content": "Suksessfull innlogging."}
                jsonresponse = json.dumps(response)
                self.connection.send(jsonresponse.encode())
            else:
                tid = time.time()
                now = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
                response = {"timestamp": now, "sender": "Server", "response": "login", "content": "Brukernavnet er opptatt, vennligst velg et annet."}
                jsonresponse = json.dumps(response)
                self.connection.send(jsonresponse.encode())
                for i in self.chatHandler.getHistory():
                    self.connection.send(i.encode())
                print(user+" logget på!")
                self.loggedin = True ##flytta for-løkka hit, men litt usikker. derde hadde den i eks på github

        elif req == "logout" and loggedin and not cont:
            self.chatHandler.removeUser()
            self.chatHandler.removeConnection(self.chatHandler)
            self.loggedin = False
            user = ''
            tid = time.time()
            now = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
            response = {"timestamp": now, "sender": "Server", "response": "logout", "content": "Suksessfull utlogging"}
            jsonresponse = json.dumps(response)
            self.connection.send(jsonresponse.encode())
            print(self.chatHandler.getUsers()+" logged out!")

        elif req == 'history':
            tid = time.time()
            thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
            history = self.chatHandler.getHistory()
            response = {"timestamp": thisTime, "sender": "Server", "response": "history", "content": cont}
            jsonresponse = json.dumps(response)
            self.connection.send(jsonresponse.encode())

        elif req == "msg" and cont:
            tid = time.time()
            thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
            ob = {"timestamp": thisTime, "sender": "Server", "response": "message", "content": cont}
            jsonresponse = json.dumps(ob)
            self.chatHandler.addMessage(jsonresponse)
            thread = self.chatHandler.getConnection()
            tid = time.time()
            thisTime = datetime.datetime.fromtimestamp(tid).strftime("%H:%M:%S")
            response = {"timestamp": thisTime, "sender": self.user, "response": "message", "content": cont}
            jsonresponse = json.dumps(response)
            for i in thread:
                i.send(jsonresponse.encode())
            self.chatHandler.addHistory(cont)


        elif req == "names" and not cont:
            users = self.chatHandler.getUsers()
            tid = time.time()
            now = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')
            response = {"timestamp": now, "sender": "Server", "response": "names", "content": users}
            jsonresponse = json.dumps(response)
            self.connection.send(jsonresponse.encode())

        elif req == "help" and not cont:
            print("hjelpetext")

        else:
            print("Noe ble feil. Prøv igjen eller skriv 'help' om du trenger hjelp.")

