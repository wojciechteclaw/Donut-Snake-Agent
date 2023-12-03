import time

import torch.cuda
from src.agent.agent import Agent
from src.environment.environment import Environment


def create_environments(number_of_env,
                        board_x_size,
                        board_y_size,
                        device,
                        is_penetration_active,
                        publish_environment,
                        is_multi_env):
    envs = []
    for _ in range(number_of_env if is_multi_env else 1):
        env = Environment(size_x=board_x_size,
                          size_y=board_y_size,
                          device=device,
                          is_penetration_active=is_penetration_active,
                          publish_environment=publish_environment)
        env.reset()
        envs.append(env)
    return envs

def train_single_step(agent, environment, device, avarage_score):
    local_memory = []
    while True:
        state_0 = agent.get_state(environment)
        move = agent.get_action(state_0)
        reward, is_alive, score = environment.move_snake(move)
        if environment.publish_environment:
            environment.publish_environment({'number_of_games': agent.number_of_games})
        new_state = agent.get_state(environment)
        action_object = agent.get_action_object(move).to(device)
        local_memory.append((state_0, action_object, reward, new_state, is_alive))
        if not is_alive:
            break
    if avarage_score >= 0:
        for item in local_memory:
            agent.remember(*item)

def train(**kwargs):
    scores = [0]
    number_of_board_expansions = 0
    board_x_size = kwargs.get('board_x_size', 10)
    board_y_size = kwargs.get('board_y_size', 10)
    is_penetration_active = kwargs.get('is_penetration_active', False)
    publish_environment = kwargs.get('publish_environment', False)
    increase_environment_size = kwargs.get('increase_environment_size', False)
    is_multi_env = kwargs.get('multi_env', False)
    number_of_env = kwargs.get('number_of_env', 10)
    device = kwargs.get('device', 'cpu')
    increase_step_games = kwargs.get('increase_step_games', 100)
    agent = Agent(**kwargs)
    envs = create_environments(number_of_env,
                               board_x_size,
                               board_y_size,
                               device,
                               is_penetration_active,
                               publish_environment,
                               is_multi_env)

    while True:
        for environment in envs:
            train_single_step(agent, environment, device, sum(scores[-100:])/(100 if len(scores) > 100 else len(scores) + 1))
        max_envs_score = 0
        for i, environment in enumerate(envs):
            max_envs_score = environment.score if environment.score > max_envs_score else max_envs_score
            if (agent.number_of_games % increase_step_games * (number_of_board_expansions + 1) == 0
                and agent.number_of_games != 0
                and increase_environment_size
                and number_of_board_expansions < max(board_x_size, board_y_size)):
                board_x_size = board_x_size + 1
                board_y_size = board_y_size + 1
                number_of_board_expansions += 1
                environment = Environment(size_x=board_x_size,
                                          size_y=board_y_size,
                                          device=device,
                                          is_penetration_active=is_penetration_active,
                                          publish_environment=publish_environment)
                envs[i] = environment
            environment.reset()
        agent.train()
        agent.increase_number_of_games()
        if max_envs_score > max(scores):
            agent.trainer.save(state_only=True)
        scores.append(max_envs_score)
        print('Game', agent.number_of_games,
              'Score', scores[-1],
              'Best Score:', max(scores),
              'Avarage Score:', round(sum(scores[-100:])/(100 if len(scores) > 100 else len(scores)), 2))

settings = {
    'batch_size': 2**11,
    'lr': 0.00025,
    'max_memory': 2**14,
    'gamma': 0.85,
    'epsilon': 0.005,
    'ending_epsilon': 0.001,
    'publish_environment': True,
    'number_of_games_to_end_epsilon': 500,
    # environment
    'board_x_size': 7,
    'board_y_size': 7,
    'is_penetration_active': False,
    # model
    'hidden_layer_size': 512,
    'load_model': False,
    'device': 'cuda' if torch.cuda.is_available() else 'cpu',
    'increase_environment_size': True,
    'multi_env': True,
    'number_of_env': 1,
    'mode': 'train',
    'increase_step_games': 500
}

if __name__ == '__main__':
    print("CUDA is available:", torch.cuda.is_available())
    train(**settings)