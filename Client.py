__author__ = 'macsita'

import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import time

class Client:
    """
    This is the chat client class
    """
    #hallohallo

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        self.run()
        message_receiver = MessageReceiver(self, self.connection)
        message_receiver.start()
        string = json.dumps({'request':'login', 'content':'anna'})
        self.connection.send(string.encode())
        while True:
            time.sleep(1)
            string = json.dumps({'request':'msg', 'content':'test'})
            string = string.encode()
            self.connection.send(string)


        # TODO: Finish init process with necessary code

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

    def disconnect(self):
        self.connection.close()
        print('Disconnected')
        # TODO: Handle disconnection

    def receive_message(self, message):
        msg_parser = MessageParser()
        print_message = msg_parser.parse(message)
        return print_message
        # TODO: Handle incoming message


    def send_payload(self, data):
        # TODO: Handle sending of a payload
        pass

    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
