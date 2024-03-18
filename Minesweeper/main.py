import sys
from game import Game

def main():
    size = int(sys.argv[1]), int(sys.argv[2])
    mine_count = float(sys.argv[3])
    g = Game(size, mine_count)
    g.run()

if __name__ == '__main__':
    main()