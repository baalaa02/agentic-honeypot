# TODO: Implement conversation memory logic

class Conversation:
    def __init__(self):
        self.history = []

    def add_message(self, message: str):
        self.history.append(message)
