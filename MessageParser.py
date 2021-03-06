__author__ = 'Anna'

import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
            'login': self.parse_login,
            'logout': self.parse_logout,
            'names': self.parse_names,
            'help': self.parse_help
	    # More key:values pairs are needed
        }

    def parse(self, payload):
        decodedPayload = payload.decode()
        payload = json.loads(decodedPayload) # decode the JSON object
        # JSON object on form: { 'timestamp': <timestampt>, 'sender': <username>, 'response': <response>, 'content': <content>, }
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return 'Not valid server response'
            # Response not valid

    def parse_error(self, payload):
        timestamp = payload['timestamp']
        content = payload['content']
        return timestamp+'  '+'Error: '+content

    def parse_info(self, payload):
        timestamp = payload['timestamp']
        content = payload['content']
        return timestamp+'  '+content

    def parse_message(self, payload):
        sender = payload['sender']
        timestamp = payload['timestamp']
        content = payload['content']
        return timestamp+'  '+sender+': '+content

    def parse_history(self, payload):
        # history = json.load(payload['content'])
        # history_msg = ''
        # history_list= []
        # for user in history:
        #     history_list.append([user, history[user]]) # [[timestap  user, content],[timestamp  user, content]...]
        # history_list.sort()
        # for user in history_list:
        #     history_msg += user+': '+history[user]+'\n'
        # return history_msg
        sender = payload['sender']
        timestamp = payload['timestamp']
        content = payload['content']
        return timestamp+'  '+sender+': '+content

    def parse_login(self, payload):
        timestamp = payload['timestamp']
        content = payload['content']
        return timestamp+'  '+content


    def parse_logout(self, payload):
        timestamp = payload['timestamp']
        content = payload['content']
        return timestamp+'  '+content


    def parse_names(self, payload):
        timestamp = payload['timestamp']
        content = payload['content']
        return timestamp+'  '+content

    def parse_help(self, payload):
        timestamp = payload['timestamp']
        content = payload['content']
        return timestamp+'  '+content
    # Include more methods for handling the different responses...
