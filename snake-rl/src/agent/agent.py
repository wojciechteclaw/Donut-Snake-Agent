from collections import deque
from random import random, randint, sample
import numpy as np
import torch

from src.agent.models.q_learning_net import QLearningNet
from src.agent.models.q_trainer_net import QTrainerNet
from src.environment.enums.field import Field
from src.environment.environment import Environment


class Agent:

    def __init__(self, **kwargs):
        self._number_of_games = 0
        self.max_memory = kwargs.get('max_memory', 2**14)
        self.batch_size = kwargs.get('batch_size', 1024)
        self.mode = kwargs.get('mode', 'train')
        self.lr = kwargs.get('lr', 0.001)
        self.hidden_layers = kwargs.get('hidden_layer_size', 128)
        # randomness factor
        self._starting_epsilon = kwargs.get('epsilon', 0.0)
        self._ending_epsilon = kwargs.get('ending_epsilon', 0.01 if self.mode == 'train' else 0.0)
        self._number_of_games_to_end_epsilon = kwargs.get('number_of_games_to_end_epsilon', 1000)
        self._eplison_decreasing_factor = (self._ending_epsilon - self._starting_epsilon) / self._number_of_games_to_end_epsilon
        self._epsilon = self._starting_epsilon
        self._gamma = kwargs.get('gamma', 0.85)
        self.publish_environment = kwargs.get('publish_environment', False)
        self.memory = deque(maxlen=self.max_memory)
        self.device = kwargs.get('device', 'cpu')

        load_model = kwargs.get('load_model', False)
        model_name = kwargs.get('model_name', 'q_learning_net')

        self.model = QLearningNet(input_size=30,
                                  hidden_size=self.hidden_layers,
                                  output_size=3).to(self.device)
        self.trainer = QTrainerNet(self.model,
                                   lr=self.lr,
                                   gamma=self._gamma,
                                   load=load_model,
                                   model_name =model_name).to(self.device)

    @property
    def number_of_games(self):
        return self._number_of_games

    def increase_number_of_games(self):
        self._number_of_games += 1

    def get_batch(self):
        if len(self.memory) > self.batch_size:
            return sample(self.memory, self.batch_size)
        return self.memory

    def remember(self,
                 state: torch.Tensor,
                 action: torch.Tensor,
                 reward: torch.Tensor,
                 next_state: torch.Tensor,
                 is_active: torch.Tensor):
        self.memory.append((state, action, reward, next_state, is_active))
        if len(self.memory) > self.max_memory:
            self.memory.popleft()

    def train_step(self,
                   state:torch.Tensor,
                   action:torch.Tensor,
                   reward:torch.Tensor,
                   next_state:torch.Tensor,
                   is_active:torch.Tensor):
        self.trainer.train(state, action, reward, next_state, is_active)

    def set_epsilon(self):
        self._epsilon = max(self._ending_epsilon, self._eplison_decreasing_factor * self._number_of_games)

    def get_action(self, state:torch.Tensor):
        if random() < self._epsilon:
            return randint(0, 2)
        return torch.argmax(self.model(torch.unsqueeze(state, 0))).item()

    def get_action_object(self, action:int):
        move = [0, 0, 0]
        move[action] = 1
        return torch.tensor(move, dtype=torch.float)

    def train(self):
        batch = self.get_batch()
        states, actions, rewards, next_states, is_active = zip(*batch)
        torch_state = torch.stack(states)
        torch_action = torch.stack(actions)
        torch_reward = torch.stack(rewards)
        torch_next_state = torch.stack(next_states)
        torch_is_active = torch.stack(is_active)
        self.train_step(torch_state, torch_action, torch_reward, torch_next_state, torch_is_active)

    def get_state(self, environment:Environment):
        distances, obstacles, food, direction = environment.observe()
        obstacles_with_food_only = np.where(obstacles == Field.APPLE.value, 1., 0.)
        state = np.concatenate([distances,
                                obstacles_with_food_only,
                                direction,
                                food])
        state_tensor = torch.tensor(state, dtype=torch.float).to(self.device)
        return state_tensor
