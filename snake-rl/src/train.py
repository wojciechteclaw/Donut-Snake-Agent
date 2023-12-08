import torch.cuda
from src.agent.agent import Agent
from src.environment.environment import Environment


def train_single_step(agent, environment, device):
    while True:
        if environment.is_publish_enabled:
            environment.publish_environment({'number_of_games': agent.number_of_games})
        state_0 = agent.get_state(environment)
        move = agent.get_action(state_0)
        reward, is_alive, score = environment.move_snake(move)
        new_state = agent.get_state(environment) if is_alive else state_0
        action_object = agent.get_action_object(move).to(device)
        agent.remember(state_0, action_object, reward, new_state, is_alive)
        if not is_alive:
            break


def train(**kwargs):
    scores = [0]
    number_of_board_expansions = 0
    board_x_size = kwargs.get('board_x_size', 10)
    board_y_size = kwargs.get('board_y_size', 10)
    is_penetration_active = kwargs.get('is_penetration_active', False)
    publish_environment = kwargs.get('publish_environment', False)
    increase_environment_size = kwargs.get('increase_environment_size', False)
    device = kwargs.get('device', 'cpu')
    increase_step_games = kwargs.get('increase_step_games', 100)
    agent = Agent(**kwargs)
    environment = Environment(size_x=board_x_size,
                              size_y=board_y_size,
                              device=device,
                              is_penetration_active=is_penetration_active,
                              publish_environment=publish_environment)
    environment.reset()

    while True:
        train_single_step(agent, environment, device)
        if (agent.number_of_games % increase_step_games * (number_of_board_expansions + 1) == 0 and
                agent.number_of_games != 0 and
                increase_environment_size and
                number_of_board_expansions < max(board_x_size, board_y_size)):
            board_x_size = board_x_size + 1
            board_y_size = board_y_size + 1
            number_of_board_expansions += 1
            environment = Environment(size_x=board_x_size,
                                      size_y=board_y_size,
                                      device=device,
                                      is_penetration_active=is_penetration_active,
                                      publish_environment=publish_environment)

        agent.train()
        agent.increase_number_of_games()
        if environment.score > max(scores):
            agent.trainer.save()
        scores.append(environment.score)
        print('Game', agent.number_of_games,
              'Score', scores[-1],
              'Best Score:', max(scores),
              'Avarage Score:', round(sum(scores[-100:])/(100 if len(scores) > 100 else len(scores)), 2))
        environment.reset()


settings = {
    'batch_size': 2**11,
    'lr': 0.00075,
    'max_memory': 2**14,
    'gamma': 0.85,
    'epsilon': 0.05,
    'desire_epsilon': 0.01,
    'publish_environment': False,
    'number_of_games_to_end_epsilon': 500,
    # environment
    'board_x_size': 6,
    'board_y_size': 6,
    'is_penetration_active': True,
    # model
    'hidden_layer_size': 512,
    'model_name': 'q_learning_net_with_wall_transparency_trololol',
    'load_model': True,
    'device': 'cuda' if torch.cuda.is_available() else 'cpu',
    'increase_environment_size': True,
    'mode': 'train',
    'increase_step_games': 100
}

if __name__ == '__main__':
    print("CUDA is available:", torch.cuda.is_available())
    train(**settings)
