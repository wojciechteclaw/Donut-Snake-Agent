import requests
import numpy as np
import json
import torch
from src.environment.snake.block import Block
from src.environment.enums.field import Field
from src.environment.snake.snake import Snake
from src.environment.vision.vision import Vision


class Environment:

    CLASH_REWARD = -2.5
    FOOD_REWARD = 1

    def __init__(self, size_x: int = 10,
                 size_y: int = 10,
                 device: torch.device = 'cpu',
                 is_penetration_active: bool = False,
                 publish_environment: bool = False,
                 publish_address: str = 'http://127.0.0.1:5001'):
        self.number_of_steps_without_food = 0
        self.number_of_turns_without_food = 0
        self.number_of_steps = 0
        self.size_x = size_x
        self.size_y = size_y
        self.score = 0
        self.device = device
        # step punish depends on a board size. The bigger the board the smaller the punishment
        # because it might be harder to reach the food. The assumption is that the snake can visit
        # each cell at least before being dead
        self.STEP_REWARD = -2.5 / (size_x * size_y)
        self.is_penetration_active = is_penetration_active
        self.snake = Snake(size_x=size_x,
                           size_y=size_y,
                           is_penetration_active=is_penetration_active)
        self.reward = 0
        self.PUBLISHER_ADDRESS = publish_address
        self.is_publish_enabled = publish_environment

    def reset(self) -> None:
        self.snake.reset()
        self.food = self.generate_food()
        self.score = 0
        self.reward = 0
        self.number_of_steps_without_food = 0
        self.number_of_steps = 0
        if self.is_publish_enabled:
            self.publish_environment()

    def generate_food(self) -> Block:
        board = self.__get_board_with_snake_items_only()
        empty_cells = np.argwhere(board == Field.EMPTY.value)
        np.random.shuffle(empty_cells)
        random_item = empty_cells[0]
        return Block(random_item[1], random_item[0])

    def __get_board_with_snake_items_only(self) -> np.ndarray:
        board = np.ones((self.size_y, self.size_x)) * Field.EMPTY.value
        board = self.snake.project_snake_on_board(board)
        return board

    def get_board(self) -> np.ndarray:
        board = self.__get_board_with_snake_items_only()
        board[self.food.y][self.food.x] = Field.APPLE.value
        return np.array(board)

    def check_food(self) -> bool:
        if self.snake.head == self.food:
            self.snake.append_food()
            return True
        return False

    def observe(self) -> tuple[np.array, np.array, np.array, np.array]:
        board = self.get_board()
        vision = Vision(self.snake, board)
        distance, target_type = vision.look()
        food = vision.get_food_direction_vector(self.food)
        snake_direction_vector = self.snake.get_direction_vector()
        return (np.array(distance),
                np.array(target_type),
                food,
                snake_direction_vector)

    def move_snake(self, action: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        self.snake.move(action)
        found_food = self.check_food()
        self.number_of_steps += 1
        self.number_of_steps_without_food += 1
        if found_food:
            self.food = self.generate_food()
            self.score += 1
            self.reward += self.FOOD_REWARD
            self.number_of_steps_without_food = 0
            self.number_of_turns_without_food = 0
        elif not self.snake.alive:
            self.reward += self.CLASH_REWARD
        if self.reward < self.CLASH_REWARD:
            self.snake.alive = False
        self.reward += self.STEP_REWARD

        return (torch.tensor(self.reward, dtype=torch.float).to(self.device),
                torch.tensor(self.snake.alive, dtype=torch.int).to(self.device),
                torch.tensor(self.score, dtype=torch.float).to(self.device))

    def publish_environment(self, extra: dict = {}) -> None:
        try:
            data = {
                'x_rows': self.size_x,
                'y_rows': self.size_y,
                'environment_object': self.get_board().tolist(),
                'is_donut': self.is_penetration_active,
                'score': self.score,
                'reward': self.reward,
                'is_alive': self.snake.alive,
                'number_of_steps': self.number_of_steps,
                'number_of_steps_without_food': self.number_of_steps_without_food
            }
            data.update(extra)
            dumped = json.dumps(data)
            requests.post(self.PUBLISHER_ADDRESS + '/publish-environment', data=dumped)
        except Exception as e:
            print(e)
