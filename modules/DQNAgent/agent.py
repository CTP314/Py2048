from time import sleep
import torch
import random
import numpy as np
import torch.nn as nn
from modules.DQNAgent.network import DeepQNetwork
from collections import deque
import pandas as pd

class DQNAgent():
    def __init__(self, mode, checkpointspath):
        self.mode = mode
        self.checkpointspath = checkpointspath
        
        self.input_size = 16
        self.num_actions = 4
        self.save_interval = 5000
        self.replay_memory_record = deque()
        self.init_epsilon = 0.1
        self.end_epsilon = 1e-4
        self.epsilon = self.init_epsilon
        self.batch_size = 32
        self.replay_memory_size = 1e4
        self.discount_factor = 0.99
        self.pos_save_prob = 0.1
        self.num_observes = 3200
        self.num_explores = 1e5
        self.input_data = None
        self.num_iters = 0
        self.num_games = 0
        self.score = 0
        self.max_score = 0
        self.use_cuda = torch.cuda.is_available()
        self.FloatTensor = torch.cuda.FloatTensor if self.use_cuda else torch.FloatTensor

        self.dqn_model = DeepQNetwork(self.input_size, self.num_actions)
        self.dqn_model = self.dqn_model.cuda() if self.use_cuda else self.dqn_model
        self.optimizer = torch.optim.Adam(self.dqn_model.parameters(), lr=1e-4)
        self.loss_func = nn.MSELoss()

        self.train_scores = []
        self.avg_score = 0

    def process(self, board):
        X = np.array(board).flatten()
        X[X == 0] = 1
        X = 1 / (np.log2(X) + 1)
        return X

    def train(self, game_controller):
        action = np.array([0] * self.num_actions)
        action[0] = 1
        last_score = 0
        board, score, is_dead = game_controller.run(action)
        self.input_data = self.process(board)

        while True:
            valid_actions = game_controller.get_valid_actions()
            action = [0] * 4
            if random.random() <= self.epsilon:
                a = random.choice(valid_actions)
                action[a] = 1
            else:
                self.dqn_model.eval()
                input_data = torch.from_numpy(self.input_data).type(self.FloatTensor)
                with torch.no_grad():
                    preds = self.dqn_model(input_data).cpu().data.numpy()
                # print(f'network result{valid_actions}')
                a = valid_actions[np.argmax(preds[valid_actions])]
                action[a] = 1
                self.dqn_model.train()
            
            last_score = score
            board, score, is_dead = game_controller.run(action)
            input_data_prev = self.input_data.copy()
            self.input_data = self.process(board)

            if is_dead:
                self.avg_score += score
                self.train_scores.append(score)
                self.num_games += 1
                reward = -1
                last_score = 0
                score = 0
                game_controller.restart()
            else:
                reward = (score - last_score) / (2 ** 8)
            
            self.score = score
            if score > self.max_score:
                self.max_score = score
            if is_dead or random.random() <= self.pos_save_prob:
                self.replay_memory_record.append([[input_data_prev], [self.input_data], action, np.array([int(is_dead)]), np.array([reward])])
            if len(self.replay_memory_record) > self.replay_memory_size:
                self.replay_memory_record.popleft()

            loss = torch.Tensor([0]).type(self.FloatTensor)
            if self.num_iters > self.num_observes:
                self.optimizer.zero_grad()
                minibatch = random.sample(self.replay_memory_record, self.batch_size)
                states, states1, actions, is_deads, rewards = zip(*minibatch)
                
                states = torch.from_numpy(np.concatenate(states)).type(self.FloatTensor)
                states1 = torch.from_numpy(np.concatenate(states1)).type(self.FloatTensor)
                actions = torch.from_numpy(np.concatenate(actions)).type(self.FloatTensor).view(self.batch_size, -1)
                is_deads = torch.from_numpy(np.concatenate(is_deads)).type(self.FloatTensor)
                rewards = torch.from_numpy(np.concatenate(rewards)).type(self.FloatTensor)
                with torch.no_grad():
                    targets = rewards + self.discount_factor * self.dqn_model(states1).max(-1)[0] * (1 - is_deads)
                    targets = targets.detach()
                preds = torch.sum(self.dqn_model(states) * actions, dim=1)
                loss = self.loss_func(preds, targets)
                loss.backward()
                self.optimizer.step()

            self.num_iters += 1
            if self.epsilon > self.end_epsilon and self.num_iters > self.num_observes:
                self.epsilon -= (self.init_epsilon - self.end_epsilon) / self.num_explores

            if self.num_iters % self.save_interval == 0:
                self.save(self.checkpointspath)
            
            if self.num_games % 50 == 0 and not is_dead:
                print('-----------------------')
                for i in range(4):
                    for j in range(4):
                        print(board[i][j], end=' ')
                    print('') 
                sleep(0.5)
            
            if is_dead and self.num_games % 50 == 0:
                print(f'[State]: train, [Games]: {self.num_games}, [Avg Score]: {self.avg_score / 50}, [Max Score]: {self.max_score}, [Loss]: %.3f'%(loss.item())) 
                self.avg_score = 0
                df = pd.DataFrame({'score': self.train_scores})
                df.to_csv('result.csv', index=False)

    def save(self, checkpointspath):
        print(f'Saving checkpoints into {checkpointspath}...')
        torch.save(self.dqn_model.state_dict(), checkpointspath)