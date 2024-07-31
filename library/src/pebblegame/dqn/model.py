import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

HIDDEN_SIZE = 512

# TODO: ideas below
"""Interpret the network using a convolutional neural net, so the matrix structure is recognised"""

class Linear_QNet(nn.Module):

    def __init__(self, input_size : int, output_size : int) -> None:
        super().__init__()
        self.linear1 = nn.Linear(input_size, HIDDEN_SIZE)
        #self.linear2 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
        self.linear2 = nn.Linear(HIDDEN_SIZE, output_size)
        self.load()

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        #x = self.linear3(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './saved'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)
    
    def load(self, file_name='model.pth'):
        model_folder_path = './saved'
        if not os.path.exists(model_folder_path): return
        file_name = os.path.join(model_folder_path, file_name)
        self.load_state_dict(torch.load(file_name))
        
# Trains the given neural network 
class QTrainer():
    def __init__(self, model, lr, gamma) -> None:
        self.lr = lr
        self.model = model
        self.gamma = gamma
        self.optimiser = optim.SGD(model.parameters(), lr=lr, momentum=0.9)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            # want shape (1, x) for single sample
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            done = (done,)
        
        # predicted Q value with current state
        pred = self.model(state)

        # r + gamma * max of next_predicted Q value

        target = pred.clone()

        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            target[idx][torch.argmax(action).item()] = Q_new

        self.optimiser.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimiser.step()




        