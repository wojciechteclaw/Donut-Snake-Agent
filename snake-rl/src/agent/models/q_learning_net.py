import torch
import torch.nn as nn


class QLearningNet(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.net = nn.Sequential(
            nn.Linear(in_features=input_size, out_features=hidden_size),
            nn.ReLU(),
            nn.Linear(in_features=hidden_size, out_features=hidden_size * 2),
            nn.ReLU(),
            nn.Linear(in_features=hidden_size * 2, out_features=output_size),
        )

    def forward(self, x: torch.Tensor):
        return self.net(x)
