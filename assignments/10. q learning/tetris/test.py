import argparse
import torch
import cv2
from src.tetris import Tetris

def get_args():
    parser = argparse.ArgumentParser("""Implementation of Deep Q Network to play Tetris""")

    parser.add_argument("--width", type=int, default=10, help="The common width for all images")
    parser.add_argument("--height", type=int, default=20, help="The common height for all images")
    parser.add_argument("--block_size", type=int, default=30, help="Size of a block")
    parser.add_argument("--modelno", type=str)
    parser.add_argument("--rendering", type=bool, default=False)
    parser.add_argument("--runs", type=int, default=3)

    args = parser.parse_args()
    return args

def test(opt):
    filename = "tetris_" + opt.modelno
    if torch.cuda.is_available():
        torch.cuda.manual_seed(123)
    else:
        torch.manual_seed(123)
    if torch.cuda.is_available():
        model = torch.load("{}/{}".format('trained_models', filename))
    else:
        model = torch.load("{}/{}".format('trained_models', filename), map_location=lambda storage, loc: storage, weights_only=False)

    model.eval()
    env = Tetris(width=opt.width, height=opt.height, block_size=opt.block_size)
    env.reset()
    if torch.cuda.is_available():
        model.cuda()

    while True:
        next_steps = env.get_next_states()
        next_actions, next_states = zip(*next_steps.items())
        next_states = torch.stack(next_states)
        if torch.cuda.is_available():
            next_states = next_states.cuda()
        predictions = model(next_states)[:, 0]
        index = torch.argmax(predictions).item()
        action = next_actions[index]
        _, done = env.step(action, render=opt.rendering, video=out)

        if done:
            out.release()
            return env.score, env.cleared_lines

if __name__ == "__main__":
    opt = get_args()
    LOG_FILE = 'logs/testing.log'

    with open(LOG_FILE, 'a') as file:
        file.write('Model ' + opt.modelno + '\n')
    
    total_score = 0
    total_lines = 0

    for i in range(1, (opt.runs + 1)):
        score, lines = test(opt)
        total_score += score
        total_lines += lines
        
        log_message = f"Score: {score}, Lines cleared: {lines}"
        with open(LOG_FILE, 'a') as file:
            file.write('Test Run ' + str(i) + ': ' + log_message + '\n')
    
    with open(LOG_FILE, 'a') as file:
        file.write('Average: Score: ' + str(round(total_score/3, 2)) + ', Lines cleared: ' + str(round(total_lines/3, 2)) +'\n\n')