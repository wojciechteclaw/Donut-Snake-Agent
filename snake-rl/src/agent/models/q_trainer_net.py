import os

import torch
import torch.nn as nn



class QTrainerNet(nn.Module):

    def __init__(self, model, lr, gamma, load, model_name='q_learning_net_'):
        super().__init__()
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        self.model_name = model_name
        self.load_model(load)

    def load_model(self, load_model):
        if load_model:
            self.load()

    def train(self, state, action, reward, next_state, is_alive):
        if action.dim() == 1:
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            is_alive = torch.unsqueeze(is_alive, 0)
        pred = self.model(state)
        target = pred.clone()
        for item_index in range(len(is_alive)):
            Q_new = reward[item_index]
            if is_alive[item_index]:
                Q_new = reward[item_index] + self.gamma * torch.max(self.model(next_state[item_index]))
            target[item_index][torch.argmax(action[item_index]).item()] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()

    def save(self):
        folder_path = self.__get_desired_directory()
        self.__create_directory(folder_path)
        path = os.path.join(folder_path, self.model_name + ".pth")
        torch.save(self.model.state_dict(), path)

    def load(self):
        folder_path = self.__get_desired_directory()
        path = os.path.join(folder_path, self.model_name + ".pth")
        if os.path.exists(path):
            print(f'Loading model: {self.model_name} state dictionary')
            self.model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
        else:
            print('there is no model to load')

    def __get_desired_directory(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        desired_directory = os.path.join(script_dir, '../..', 'models')
        return os.path.normpath(desired_directory)

    def __create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
