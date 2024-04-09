from abc import ABC, abstractmethod

class State(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_click(self, position):
        pass

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass