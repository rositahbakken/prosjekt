__author__ = 'Anna'

import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
	    # More key:values pairs are needed
        }

    def parse(self, payload):
        payload = json.loads(payload) # decode the JSON object
        # JSON object on form: { 'timestamp': <timestampt>, 'sender': <username>, 'response': <response>, 'content': <content>, }
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            pass
            # Response not valid

    def parse_error(self, payload):
        pass
    def parse_info(self, payload):
        pass

    # Include more methods for handling the different responses...
