import torch
from time import sleep
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
                              publish_environment=publish_environment,
                              publish_address=kwargs.get('publish_address', 'http://localhost:5001')
                              )
    environment.reset()
    while True:
        if publish_environment:
            environment.publish_environment({'number_of_games': agent.number_of_games})
        state_0 = agent.get_state(environment)
        move = agent.get_action(state_0)
        _, is_alive, _ = environment.move_snake(move)
        sleep(time_delay)
        if not is_alive:
            sleep(2.5)
            score = environment.score
            environment.reset()
            agent.increase_number_of_games()
            if score > best_score:
                best_score = score
            print('Game', agent.number_of_games, 'Score', score, 'Best Score:', best_score)


settings = {
    'publish_environment': True,
    # environment
    'board_x_size': 10,
    'board_y_size': 14,
    'is_penetration_active': False,
    # model
    'hidden_layer_size': 512,
    'model_name': 'q_learning_net_without_wall_transparency',
    'load_model': True,
    'device': 'cpu',
    'step_delay': 0.10,
    'mode': 'play',
    'publish_address': 'http://snake-transmiter:5001'
}

if __name__ == '__main__':
    print("CUDA is available:", torch.cuda.is_available())
    play(**settings)
