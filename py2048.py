import os
import argparse
from modules.DQNAgent.agent import DQNAgent
from modules.gameapis.controller import GameController

def parseArgs():
    parser = argparse.ArgumentParser(description='Use dqn to play 2048')
    parser.add_argument('--mode', dest='mode', default='train', type=str)
    # parser.add_argument('--resume', dest='resume', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parseArgs()
    mode = args.mode.lower()
    assert mode in ['train', 'test']

    if not os.path.exists('checkpoints'):
        os.mkdir('checkpoints')
    checkpointspath = 'checkpoints/dqn.pth'
    agent = DQNAgent(mode=mode, checkpointspath=checkpointspath)
    
    game_controller = GameController()

    if mode == 'train':
        agent.train(game_controller)
