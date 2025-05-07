import argparse
import pygame

from snakeql import SnakeQAgent
from visualsnake import VisualSnake

def get_args():
    parser = argparse.ArgumentParser("""Snake""")
    parser.add_argument("--mode", type = int, default = 1, help="1 for training, 0 for demo")
    parser.add_argument("--ep", type = str, help="Model number to visualize (demo)")

    args = parser.parse_args()
    return args

def main():
    agent = SnakeQAgent()

    agent.train()
    pygame.quit()

def demo(episode):
    game = VisualSnake()
    game.run_game(episode)
    

if __name__ == "__main__":
    args = get_args()
    if args.mode:
        main()
    else:
        demo(episode=args.ep)