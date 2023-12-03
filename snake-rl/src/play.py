import torch
import time
from src.agent.agent import Agent
from src.environment.environment import Environment

def play(**kwargs):
    best_score = 0
    board_x_size = kwargs.get('board_x_size', 10)
    board_y_size = kwargs.get('board_y_size', 10)
    time_delay = kwargs.get('step_delay', 0.25)
    is_penetration_active = kwargs.get('is_penetration_active', False)
    publish_environment = kwargs.get('publish_environment', False)
    device = kwargs.get('device', 'cpu')
    agent = Agent(**kwargs)
    environment = Environment(size_x=board_x_size,
                              size_y=board_y_size,
                              device=device,
                              is_penetration_active=is_penetration_active,
                              publish_environment=publish_environment)
    environment.reset()
    while True:
        state_0 = agent.get_state(environment)
        move = agent.get_action(state_0)
        _, is_alive, _ = environment.move_snake(move)
        time.sleep(time_delay)
        if publish_environment:
            environment.publish_environment({'number_of_games': agent.number_of_games})
        if not is_alive:
            time.sleep(2.5)
            score = environment.score
            environment.reset()
            agent.increase_number_of_games()
            if score > best_score:
                best_score = score
            print('Game', agent.number_of_games, 'Score', score, 'Best Score:', best_score)


settings = {
    'batch_size': 2**10,
    'max_memory': 2**12,
    'gamma': 0.85,
    'epsilon': 0.00,
    'publish_environment': True,
    'number_of_games_to_end_epsilon': 500,
    # environment
    'board_x_size': 14,
    'board_y_size': 14,
    'is_penetration_active': False,
    # model
    'hidden_layer_size': 512,
    'file_name': 'q_learning_net_v2_old_food_vectoring',
    'load_model': False,
    'device': 'cuda' if torch.cuda.is_available() else 'cpu',
    'step_delay': 0.05,
    'mode': 'play'
}

if __name__ == '__main__':
    print("CUDA is available:", torch.cuda.is_available())
    play(**settings)