from abc import ABC, abstractmethod
from typing import Tuple, Any


class State(ABC):
    def __init__(self, game: Any) -> None:
        self.game: Any = game

    @abstractmethod
    def handle_click(self, position: Tuple[int, int]) -> None:
        pass

    @abstractmethod
    def enter(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass
