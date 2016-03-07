__author__ = 'Anna'

from threading import Thread
import json

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """

        # Flag to run thread as a deamon
        Thread.__init__(self)
        self.daemon = True
        self.client = client
        self.connection = connection

        # TODO: Finish initialization of MessageReceiver

    def run(self):
        Thread(target= self.receiveMessage()).start()
        # TODO: Make MessageReceiver receive and handle payloads

    def receiveMessage(self):
        while True:
            from_server = self.connection.recv(4096)
            if not from_server:
                break
            print_message = self.client.receive_message(from_server)
            print(print_message)
