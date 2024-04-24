from typing import List, Self

class Space:
    # States: Has bomb, clicked, flagged
    def __init__(self, has_bomb: bool) -> None:
        """
        Initialize a space on the game board.
        has_bomb (bool): Does the space contain a mine?
        """
        self.has_bomb: bool = has_bomb
        self.around: int = 0 # Num of mines around this space
        self.clicked: bool = False # Space been clicked?
        self.flagged: bool = False # Space been flagged?
        self.neighbors: List[Self] = [] # List of neighboring spaces

    def __str__(self) -> str:
        """ Return a string representation of the Space. """
        return str(self.has_bomb)

    def get_num_around(self) ->int:
        """ Getter for num_around. """
        return self.around

    def get_has_bomb(self) ->bool:
        """ Getter for has_bomb. """
        return self.has_bomb

    def get_clicked(self) ->bool:
        """ Getter for get_clicked. """
        return self.clicked

    def get_flagged(self) ->bool:
        """ Getter for get_flagged. """
        return self.flagged

    def toggle_flag(self) -> None:
        """ Tottle the flagged state of the space. """
        if not self.clicked:
            self.flagged = not self.flagged

    def handle_click(self) -> None:
        """ Setter for clicked. """
        self.clicked = True

    def set_num_around(self) -> None:
        """ Setter for num_around. """
        num = 0
        for neighbor in self.neighbors:
            if neighbor.get_has_bomb():
                num += 1
                #print("Neighbor with Mine found")
        self.around = num
       #print(f"Setting num_around: {self.around} for Space")

    def set_neighbors(self, neighbors: int) -> None:
        """ Setter for neighbors. """
        self.neighbors = neighbors
        
    def get_neighbors(self) ->int:
        """ Getter for neighbors. """
        return self.neighbors
 