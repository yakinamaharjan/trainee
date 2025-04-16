import argparse
import torch
import cv2
from src.tetris import Tetris

LOG_FILE = 'logs/testing.log'

def get_args():
    parser = argparse.ArgumentParser("""Implementation of Deep Q Network to play Tetris""")

    parser.add_argument("--width", type=int, default=10, help="The common width for all images")
    parser.add_argument("--height", type=int, default=20, help="The common height for all images")
    parser.add_argument("--block_size", type=int, default=30, help="Size of a block")
    parser.add_argument("--fps", type=int, default=300, help="frames per second")
    parser.add_argument("--saved_path", type=str, default="trained_models")
    parser.add_argument("--filename", type=str, default="tetris_4")
    parser.add_argument("--modelno", type=str, default="4")
    parser.add_argument("--output", type=str, default="output.mp4")

    args = parser.parse_args()
    return args

def test(opt):
    if torch.cuda.is_available():
        torch.cuda.manual_seed(123)
    else:
        torch.manual_seed(123)
    if torch.cuda.is_available():
        model = torch.load("{}/{}".format(opt.saved_path, opt.filename))
    else:
        model = torch.load("{}/{}".format(opt.saved_path, opt.filename), map_location=lambda storage, loc: storage, weights_only=False)

    model.eval()
    env = Tetris(width=opt.width, height=opt.height, block_size=opt.block_size)
    env.reset()
    if torch.cuda.is_available():
        model.cuda()
    out = cv2.VideoWriter(opt.output, cv2.VideoWriter_fourcc(*"MJPG"), opt.fps,
                          (int(1.5*opt.width*opt.block_size), opt.height*opt.block_size))
    while True:
        next_steps = env.get_next_states()
        next_actions, next_states = zip(*next_steps.items())
        next_states = torch.stack(next_states)
        if torch.cuda.is_available():
            next_states = next_states.cuda()
        predictions = model(next_states)[:, 0]
        index = torch.argmax(predictions).item()
        action = next_actions[index]
        _, done = env.step(action, render=True, video=out)

        if done:
            log_message = f"Model {opt.modelno} \nTest run score: {env.score} \nTest run Lines cleared: {env.cleared_lines}"
            
            with open(LOG_FILE, 'a') as file:
                file.write(log_message + '\n\n')
            out.release()

            break

if __name__ == "__main__":
    opt = get_args()
    test(opt)