import sys
from game import Game

def main() -> None:
    """ Get command line arguments: size x, size y, mine count """
    if len(sys.argv) != 4:
        print("Usage: python3 main.py grid_width grid_height mine_count")
        sys.exit(1)
    try:
        grid_width = int(sys.argv[1])
        grid_height = int(sys.argv[2])
        mine_count = int(sys.argv[3])

        if grid_width <= 0 or grid_height <= 0 or mine_count <= 0:
            raise ValueError("Grid dimensions and mine count must be positive numbers > 0.")

    except ValueError as e:
        print("Invalid input:", e)
        sys.exit(1)

    size = (grid_width, grid_height)
    g = Game(size, mine_count) # Create a game with arguments
    g.run()

if __name__ == '__main__':
    main()