import torch
import torch.nn as nn
import torch.nn.functional as F

class DeepQNetwork(nn.Module):
    def __init__(self, input_size, num_actions):
        super(DeepQNetwork, self).__init__()
        self.fc1 = nn.Linear(in_features=input_size, out_features=16 * 16)
        self.fc2 = nn.Linear(in_features=16*16, out_features=16)
        self.fc3 = nn.Linear(in_features=16, out_features=num_actions)
    
    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x, inplace=True)
        x = self.fc2(x)
        x = F.sigmoid(x)
        x = self.fc3(x)
        return x