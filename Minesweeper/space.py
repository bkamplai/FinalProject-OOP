from typing import List, Self

class Space:
    # States: Not clicked, clicked, flagged
    def __init__(self, has_bomb: bool) -> None:
        self.has_bomb: bool = has_bomb
        self.around: int = 0
        self.clicked: bool = False
        self.flagged: bool = False
        self.neighbors: List[Self] = []

    def __str__(self) -> str:
        return str(self.has_bomb)

    def get_num_around(self) ->int:
        return self.around

    def get_has_bomb(self) ->bool:
        return self.has_bomb

    def get_clicked(self) ->bool:
        return self.clicked

    def get_flagged(self) ->bool:
        return self.flagged

    def toggle_flag(self) ->None:
        self.flagged = not self.flagged

    def handle_click(self) ->None:
        self.clicked = True

    def set_num_around(self) ->None:
        num = 0
        for neighbor in self.neighbors:
            if neighbor.get_has_bomb():
                num += 1
        self.around = num

    def set_neighbors(self, neighbors: int) ->None:
        self.neighbors = neighbors
        
    def get_neighbors(self) ->int:
        return self.neighbors
 