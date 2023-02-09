from cProfile import run
import random
import numpy

class Agent():
    def __init__(self, state=[], action_space=[]) -> None:
        self.state = state
        self.score = 0
        self.max_score = 0
        self.num_games = 0
        self.action_space = action_space

    def getAction(self) -> int:
        return random.choice(self.action_space)

    def test(self, game_controller):
        self.state = game_controller._board
        self.action_space = game_controller._action_space
        while True:
            action = self.getAction()
            board, score, is_end = game_controller.run(action)
            self.state = board

            if is_end:
                self.num_games += 1
                game_controller.restart()
            
            self.score = score
            if score > self.max_score:
                self.max_score = score

            print('[State]: test, [Games]: %s, [Score]: %s, [Max Score]: %s, [Action]: %s' % (self.num_games, self.score, self.max_score, action))
