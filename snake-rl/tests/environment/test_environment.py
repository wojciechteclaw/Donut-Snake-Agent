from unittest import mock
import random

import numpy as np
import pytest

from src.environment.enums.direction import Direction
from src.environment.enums.field import Field
from src.environment.environment import Environment
from src.environment.snake.block import Block
from src.environment.snake.snake import Snake


def test_board_reset():
    with mock.patch.object(random, 'randint', return_value=5):
        snake = Snake(10, 10)
    environment = Environment(10, 10)
    environment.reset()
    environment.snake = snake
    environment.food = Block(6, 5)
    environment.move_snake(1)
    assert environment.reward == (Environment.FOOD_REWARD + Environment.STEP_REWARD)
    assert environment.score == 1
    environment.food = Block(7, 5)
    environment.move_snake(1)
    assert environment.score == 2
    assert round(environment.reward, 3) == (Environment.FOOD_REWARD + Environment.STEP_REWARD) * 2
    environment.reset()
    assert environment.score == 0
    assert environment.reward == 0
    assert environment.number_of_steps_without_food == 0

def test_clash_reward():
    snake = Snake(10, 10)
    snake.body = [Block(9, 5), Block(8, 5), Block(7, 5), Block(6, 5)]
    snake.direction = Direction.RIGHT
    board = Environment(10, 10)
    board.reset()
    board.snake = snake
    board.move_snake(1)
    assert board.reward == Environment.CLASH_REWARD + Environment.STEP_REWARD
    assert board.snake.alive == False

def test_snake_body_clash_reward():
    snake = Snake(10, 10)
    snake.body = [Block(8, 6),
                  Block(8, 5),
                  Block(7, 5),
                  Block(6, 5),
                  Block(6, 6),
                  Block(7, 6)]
    snake.direction = Direction.LEFT
    board = Environment(10, 10)
    board.reset()
    board.snake = snake
    board.move_snake(1)
    assert round(board.reward, 3) == Environment.CLASH_REWARD + Environment.STEP_REWARD
    assert board.snake.alive == False

def test_check_food():
    with mock.patch.object(random, 'randint', return_value=5):
        snake = Snake(10, 10)
    board = Environment(10, 10)
    board.snake = snake
    assert board.snake.head == Block(5, 5)
    board.food = Block(6, 5)
    assert board.check_food() == False
    board.snake.move(1)
    assert board.snake.head == Block(6, 5)
    assert board.check_food() == True

@pytest.mark.parametrize("board_x_size, board_y_size", [
    (10, 10),
    (20, 20),
    (12, 11)
])
def test_generate_food(board_x_size, board_y_size):
    snake = Snake(board_x_size, board_y_size)
    environment = Environment(board_x_size, board_y_size)
    body = []
    board_items = board_x_size * board_y_size
    for y in range(board_y_size):
        for x in range(board_x_size):
            body.append(Block(x, y))
    random.shuffle(body)
    snake.body = body[:int(0.9 * board_items)]
    environment.snake = snake
    for i in range(board_items):
        food = environment.generate_food()
        assert food not in snake.body

@pytest.mark.parametrize("board_x_size, board_y_size, snake_head_x, snake_head_y, body_elements, expected_elements_other_than_empty", [
    (10, 10, 5, 5,
     [Block(4, 5), Block(3, 5), Block(2, 5), Block(1, 5)],
     [(5, 5), (4, 5), (3, 5), (2, 5), (1, 5)]),
    (12, 8, 6, 5,
     [Block(5, 7), Block(4, 7), Block(3, 7), Block(2, 7), Block(1, 7)],
     [(6,5), (5,7), (4, 7), (3, 7), (2, 7), (1, 7)]),
    (15, 10, 8, 8,
     [Block(7, 8), Block(6, 8), Block(5, 8), Block(4, 8)],
     [(8, 8), (7, 8), (6, 8), (5, 8), (4, 8)]),
])
def test__get_board_with_snake_items_only(board_x_size,
                   board_y_size,
                   snake_head_x,
                   snake_head_y,
                   body_elements,
                   expected_elements_other_than_empty):
    snake = Snake(board_x_size, board_y_size)
    environment = Environment(board_x_size, board_y_size)
    body = [Block(snake_head_x, snake_head_y)] + body_elements
    snake.body = body
    environment.snake = snake
    board = environment._Environment__get_board_with_snake_items_only()
    for x in range(board_x_size):
        for y in range(board_y_size):
            if (x, y) in expected_elements_other_than_empty:
                assert board[y][x] != Field.SNAKE_BODY.value or board[y][x] != Field.SNAKE_HEAD.value
            else:
                assert board[y][x] == Field.EMPTY.value

@pytest.mark.parametrize("board_x_size, board_y_size, snake_head_x, snake_head_y, body_elements, food", [
    (10, 10, 5, 5, [Block(4, 5), Block(3, 5), Block(2, 5), Block(1, 5)], Block(7, 7)),
    (12, 8, 6, 5, [Block(5, 7), Block(4, 7), Block(3, 7), Block(2, 7), Block(1, 7)], Block(7, 7)),
    (15, 10, 8, 8, [Block(7, 8), Block(6, 8), Block(5, 8), Block(4, 8)], Block(8, 9)),
])
def test_get_board(board_x_size, board_y_size, snake_head_x, snake_head_y, body_elements, food):
    snake = Snake(board_x_size, board_y_size)
    environment = Environment(board_x_size, board_y_size)
    body = [Block(snake_head_x, snake_head_y)] + body_elements
    snake.body = body
    environment.snake = snake
    environment.food = food
    resulting_board = environment.get_board()

    expected_board = np.ones((board_y_size, board_x_size)) * Field.EMPTY.value
    for i, block in enumerate(body):
        if i != 0:
            expected_board[block.y][block.x] = Field.SNAKE_BODY.value
        else:
            expected_board[block.y][block.x] = Field.SNAKE_HEAD.value
    expected_board[food.y][food.x] = Field.APPLE.value
    assert np.array_equal(resulting_board, expected_board)

@pytest.mark.parametrize("""board_x_size,
board_y_size,
snake_head_x,
snake_head_y,
element_x,
element_y,
element_type,
action,
direction,
number_of_steps_without_food,
expected_reward,
expected_alive_status,
expected_score""", [
    (10, 10, 5, 5, 6, 5, Field.APPLE, 1, Direction.RIGHT, 0, Environment.FOOD_REWARD, True, 1),
    (10, 10, 5, 5, 6, 5, Field.SNAKE_BODY, 1, Direction.RIGHT, 0, Environment.CLASH_REWARD, False, 0),
    (10, 5, 0, 0, 0, 1, Field.SNAKE_BODY, 1, Direction.UP, 0, Environment.CLASH_REWARD, False, 0),
    (6, 17, 0, 1, 0, 0, Field.SNAKE_BODY, 1, Direction.DOWN, 0, Environment.CLASH_REWARD, False, 0),
    (6, 6, 3, 3, 3, 2, Field.SNAKE_BODY, 2, Direction.RIGHT, 0, Environment.CLASH_REWARD, False, 0),
    (15, 12, 3, 3, 3, 2, Field.APPLE, 2, Direction.RIGHT, 0, Environment.FOOD_REWARD, True, 1),
    (10, 12, 5, 5, 8, 5, Field.APPLE, 1, Direction.RIGHT, 15, 0, True, 0),
    (10, 12, 0, 0, 8, 5, Field.APPLE, 1, Direction.LEFT, 250, Environment.CLASH_REWARD, False, 0),
    (10, 12, 9, 11, 8, 5, Field.APPLE, 0, Direction.RIGHT, 250, Environment.CLASH_REWARD, False, 0),
    (10, 12, 9, 0, 8, 5, Field.APPLE, 2, Direction.RIGHT, 37, Environment.CLASH_REWARD, False, 0),
    (10, 12, 0, 6, 8, 5, Field.APPLE, 0, Direction.UP, 0, Environment.CLASH_REWARD, False, 0),
])
def test_move_snake(board_x_size,
                    board_y_size,
                    snake_head_x,
                    snake_head_y,
                    element_x,
                    element_y,
                    element_type,
                    action,
                    direction,
                    number_of_steps_without_food,
                    expected_reward,
                    expected_alive_status,
                    expected_score):
    snake = Snake(board_x_size, board_y_size)
    environment = Environment(board_x_size, board_y_size)
    environment.reset()
    snake.body = [Block(snake_head_x, snake_head_y)]
    snake.direction = direction
    environment.snake = snake
    environment.number_of_steps_without_food = number_of_steps_without_food
    if element_type == Field.APPLE:
        environment.food = Block(element_x, element_y)
    elif element_type == Field.SNAKE_BODY:
        snake.body.append(Block(element_x, element_y))
    reward, is_alive, score = environment.move_snake(action)
    assert round(reward.item(), 3) == round(expected_reward + environment.STEP_REWARD, 3)
    assert is_alive.item() == expected_alive_status
    assert score.item() == expected_score


