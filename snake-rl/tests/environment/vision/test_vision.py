import random
from unittest import mock

import numpy as np
import pytest

from src.environment.enums.direction import Direction
from src.environment.enums.field import Field
from src.environment.enums.raycasting_direction import RaycastingDirection
from src.environment.snake.block import Block
from src.environment.snake.snake import Snake
from src.environment.vision.vision import Vision

@pytest.mark.parametrize("direction, expected_first, expected_last", [(Direction.UP, RaycastingDirection.NORTH, RaycastingDirection.NORTH_WEST),
                                                                      (Direction.RIGHT, RaycastingDirection.EAST, RaycastingDirection.NORTH_EAST),
                                                                      (Direction.DOWN, RaycastingDirection.SOUTH, RaycastingDirection.SOUTH_EAST),
                                                                      (Direction.LEFT, RaycastingDirection.WEST, RaycastingDirection.SOUTH_WEST)
                                                                      ])
def test_rotate_from_direction(direction, expected_first, expected_last):
    with mock.patch.object(random, 'randint', return_value=5):
        s = Snake(10, 10)
    s.direction = direction
    board = np.zeros((10, 10))
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    raycasting_directions = vision._rotate_from_direction()
    assert raycasting_directions[0] == expected_first
    assert raycasting_directions[-1] == expected_last

@pytest.mark.parametrize("direction, expected", [  (RaycastingDirection.NORTH, (2, Field.WALL.value)),
                                                 (RaycastingDirection.SOUTH, (2, Field.WALL.value)),
                                                 (RaycastingDirection.EAST, (2, Field.WALL.value)),
                                                 (RaycastingDirection.WEST, (2, Field.WALL.value)),
                                                 (RaycastingDirection.NORTH_EAST, (2, Field.WALL.value)),
                                                 (RaycastingDirection.SOUTH_EAST, (2, Field.WALL.value)),
                                                 (RaycastingDirection.SOUTH_WEST, (2, Field.WALL.value)),
                                                 (RaycastingDirection.NORTH_WEST, (2, Field.WALL.value))
                                               ])
def test_raycast_without_food(direction, expected):
    board_size = 5
    with mock.patch.object(random, 'randint', return_value=2):
        s = Snake(board_size, board_size)
    board = np.ones((board_size, board_size)) * Field.EMPTY.value
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    distance, targets = vision._detect_obstacle_in_direction(direction)
    assert distance == (expected[0] / board_size)
    assert targets == expected[1]

@pytest.mark.parametrize("direction, result", [(RaycastingDirection.NORTH, (2, Field.APPLE.value)),
                                                 (RaycastingDirection.NORTH_EAST, (2, Field.APPLE.value)),
                                                 (RaycastingDirection.SOUTH, (2, Field.APPLE.value)),
                                                 (RaycastingDirection.SOUTH_EAST, (2, Field.APPLE.value)),
                                                 (RaycastingDirection.EAST, (2, Field.APPLE.value)),
                                                 (RaycastingDirection.SOUTH_WEST, (2, Field.APPLE.value)),
                                                 (RaycastingDirection.WEST, (2, Field.APPLE.value)),
                                                 (RaycastingDirection.NORTH_WEST, (2, Field.APPLE.value))])
def test_raycaster_in_with_food(direction, result):
    board_size = 10
    with mock.patch.object(random, 'randint', return_value=5):
        s = Snake(board_size, board_size)
    board = np.ones((board_size, board_size)) * Field.EMPTY.value
    board[3][3] = Field.APPLE.value
    board[3][5] = Field.APPLE.value
    board[3][7] = Field.APPLE.value
    board[5][7] = Field.APPLE.value
    board[7][7] = Field.APPLE.value
    board[7][5] = Field.APPLE.value
    board[7][3] = Field.APPLE.value
    board[5][3] = Field.APPLE.value
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    function_result = vision._detect_obstacle_in_direction(direction)
    assert function_result == (result[0] / board_size, result[1])

@pytest.mark.parametrize("raycast_direction, board_size_x, board_size_y, board_position_x, board_position_y, expected", [
    (RaycastingDirection.NORTH, 5, 5, 4, 2, (0.4, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 5, 5, 4, 2, (0.0, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 5, 5, 3, 2, (0.2, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 10, 10, 0, 0, (0.9, Field.WALL.value)),
    (RaycastingDirection.EAST, 5, 5, 4, 2, (0.0, Field.WALL.value)),
    (RaycastingDirection.EAST, 5, 5, 3, 2, (0.2, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 10, 10, 9, 5, (0.0, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 10, 20, 8, 5, (0.1, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 15, 10, 8, 5, (0.5, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 5, 0, 0, (0.0, Field.WALL.value)),
    (RaycastingDirection.NORTH, 16, 10, 9, 5, (0.4, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 20, 9, 4, (0.2, Field.WALL.value)),
    (RaycastingDirection.EAST, 10, 30, 9, 29, (0.0, Field.WALL.value)),
    (RaycastingDirection.WEST, 20, 20, 19, 19, (0.95, Field.WALL.value)),
    (RaycastingDirection.WEST, 20, 10, 19, 9, (0.95, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 20, 20, 18, 19, (0.05, Field.WALL.value)),
    (RaycastingDirection.SOUTH_WEST, 20, 10, 18, 9, (0.9, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 5, 5, 4, 2, (0.0, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 5, 5, 3, 2, (0.2, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 10, 5, 0, 0, (0.8, Field.WALL.value)),
    (RaycastingDirection.EAST, 5, 5, 4, 2, (0.0, Field.WALL.value)),
    (RaycastingDirection.EAST, 5, 5, 3, 2, (0.2, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 10, 10, 9, 5, (0.0, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 10, 10, 8, 5, (0.1, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 10, 8, 5, (0.5, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 10, 0, 0, (0.0, Field.WALL.value)),
    (RaycastingDirection.NORTH, 10, 10, 9, 5, (0.4, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 10, 9, 4, (0.4, Field.WALL.value)),
    (RaycastingDirection.EAST, 10, 10, 9, 4, (0.0, Field.WALL.value)),
    (RaycastingDirection.WEST, 20, 20, 19, 19, (0.95, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 20, 20, 18, 19, (0.05, Field.WALL.value)),
    (RaycastingDirection.SOUTH_WEST, 20, 10, 18, 9, (0.9, Field.WALL.value))
])
def test_raycaster_in_boundary_conditions(raycast_direction, board_size_x, board_size_y, board_position_x, board_position_y, expected):
    s = Snake(board_size_x, board_size_y)
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    s.body = [Block(board_position_x, board_position_y)]
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    function_result = vision._detect_obstacle_in_direction(raycast_direction)
    assert function_result == expected

@pytest.mark.parametrize("""raycast_direction,
                            board_size_x,
                            board_size_y,
                            head_position_x,
                            head_position_y,
                            food_position_x,
                            food_position_y,
                            obstacle_type,
                            expected_distance""",[
                             (RaycastingDirection.NORTH, 5, 5, 4, 2, 4, 4, Field.APPLE.value, 0.4),
                             (RaycastingDirection.NORTH_EAST, 5, 5, 0, 0, 4, 4, Field.APPLE.value, 0.8),
                             (RaycastingDirection.NORTH_EAST, 5, 5, 0, 0, 4, 4, Field.SNAKE_BODY.value, 0.8),
                             (RaycastingDirection.NORTH_EAST, 5, 5, 3, 2, 4, 3, Field.WALL.value, 0.2),
                             (RaycastingDirection.EAST, 20, 20, 10, 5, 15, 5, Field.APPLE.value, 0.25),
                             (RaycastingDirection.SOUTH_EAST, 10, 10, 1, 4, 2, 3, Field.SNAKE_BODY.value, 0.1),
])
def test_raycaster_in_boundary_conditions_with_obstacles(raycast_direction,
                                                         board_size_x,
                                                         board_size_y,
                                                         head_position_x,
                                                         head_position_y,
                                                         food_position_x,
                                                         food_position_y,
                                                         obstacle_type,
                                                         expected_distance):
    s = Snake(board_size_x, board_size_y)
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    s.body = [Block(head_position_x, head_position_y)]
    board[food_position_y][food_position_x] = obstacle_type
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    function_result = vision._detect_obstacle_in_direction(raycast_direction)
    expected = (expected_distance, obstacle_type)
    assert function_result == expected


@pytest.mark.parametrize("""board_size_x, board_size_y, raycasting_direction, expected""", [
    (5, 5, RaycastingDirection.NORTH, 5),
    (5, 5, RaycastingDirection.NORTH_EAST, 5),
    (5, 5, RaycastingDirection.EAST, 5),
    (10, 5, RaycastingDirection.NORTH, 5),
    (10, 5, RaycastingDirection.NORTH_EAST, 5),
    (10, 5, RaycastingDirection.EAST, 10),
    (5, 10, RaycastingDirection.NORTH, 10),
    (5, 10, RaycastingDirection.NORTH_WEST, 5),
    (10, 5, RaycastingDirection.WEST, 10),
    (10, 5, RaycastingDirection.NORTH_WEST, 5),
    (5, 10, RaycastingDirection.WEST, 5),
])
def test__get_direction_normalization_factor(board_size_x, board_size_y, raycasting_direction, expected):
    s = Snake(board_size_x, board_size_y)
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    result = vision._get_direction_normalization_factor(raycasting_direction)
    assert result == expected

@pytest.mark.parametrize("""snake_direction, board_size_x, board_size_y, board_position_x, board_position_y, food_position_x, food_position_y, expected""", [
    (Direction.UP, 5, 5, 2, 2, 4, 4, [
        [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.UP, 5, 5, 1, 1, 4, 4, [
        [0.6, 0.6, 0.6, 0.2, 0.2, 0.2, 0.2, 0.2],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.RIGHT, 5, 5, 2, 2, 4, 4, [
        [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value]
    ]),
    (Direction.RIGHT, 5, 5, 1, 1, 4, 4, [
        [0.6, 0.2, 0.2, 0.2, 0.2, 0.2, 0.6, 0.6],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value]
    ]),
    (Direction.LEFT, 5, 5, 1, 1, 4, 4, [
        [0.2, 0.2, 0.6, 0.6, 0.6, 0.2, 0.2, 0.2],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.UP, 10, 5, 1, 1, 4, 4, [
        [0.6, 0.6, 0.8, 0.2, 0.2, 0.2, 0.1, 0.2],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.WALL.value,Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.UP, 5, 10, 1, 1, 4, 4, [
        [0.8, 0.6, 0.6, 0.2, 0.1, 0.2, 0.2, 0.2],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.RIGHT, 10, 5, 1, 1, 4, 4, [
        [0.8, 0.2, 0.2, 0.2, 0.1, 0.2, 0.6, 0.6],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value]
    ]),
    (Direction.RIGHT, 5, 10, 1, 1, 4, 4, [
        [0.6, 0.2, 0.1, 0.2, 0.2, 0.2, 0.8, 0.6],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value]
    ]),
    (Direction.DOWN, 10, 5, 1, 1, 4, 4, [
        [0.2, 0.2, 0.1, 0.2, 0.6, 0.6, 0.8, 0.2],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.DOWN, 5, 10, 1, 1, 4, 4, [
        [0.1, 0.2, 0.2, 0.2, 0.8, 0.6, 0.6, 0.2],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.LEFT, 10, 5, 1, 1, 4, 4, [
        [0.1, 0.2, 0.6, 0.6, 0.8, 0.2, 0.2, 0.2],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.LEFT, 5, 10, 1, 1, 4, 4, [
        [ 0.2, 0.2, 0.8, 0.6, 0.6, 0.2, 0.1, 0.2],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),

])
def test_look_without_food_without_penetration(snake_direction,
                                               board_size_x,
                                               board_size_y,
                                               board_position_x,
                                               board_position_y,
                                               food_position_x,
                                               food_position_y,
                                               expected):
    s = Snake(board_size_x, board_size_y)
    s.direction = snake_direction
    s.body = [Block(board_position_x, board_position_y)]
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    board[food_position_y][food_position_x] = Field.APPLE.value
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    result_distances, result_targets = vision.look()
    expected_distances, expected_targets = expected
    assert result_targets == expected_targets
    assert result_distances == expected_distances


@pytest.mark.parametrize("""snake_direction, board_size_x, board_size_y, board_position_x, board_position_y, food_position_x, food_position_y, expected""", [
    (Direction.UP, 5, 5, 2, 2, 4, 4, [
        [1.0, 0.4, 1.0, 1.0, 1.0, 0.6, 1.0, 1.0],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.UP, 5, 5, 1, 1, 4, 4, [
        [1.0, 0.6, 1.0, 1.0, 1.0, 0.4, 1.0, 1.0],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.RIGHT, 5, 5, 2, 2, 4, 4, [
        [1.0, 1.0, 1.0, 0.6, 1.0, 1.0, 1.0, 0.4],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value]
    ]),
    (Direction.RIGHT, 5, 5, 1, 1, 4, 4, [
        [1.0, 1.0, 1.0, 0.4, 1.0, 1.0, 1.0, 0.6],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value]
    ]),
    (Direction.DOWN, 5, 5, 2, 2, 4, 4, [
        [1.0, 0.6, 1.0, 1.0, 1.0, 0.4, 1.0, 1.0],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.APPLE.value,Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.DOWN, 5, 5, 1, 1, 4, 4, [
        [1.0, 0.4, 1.0, 1.0, 1.0, 0.6, 1.0, 1.0],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value]
    ]),

    (Direction.LEFT, 5, 5, 2, 2, 4, 4, [
        [1.0, 1.0, 1.0, 0.4, 1.0, 1.0, 1.0, 0.6],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value]
    ]),
    (Direction.LEFT, 5, 5, 1, 1, 4, 4, [
        [1.0, 1.0, 1.0, 0.6, 1.0, 1.0, 1.0, 0.4],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value]
    ]),
    (Direction.UP, 10, 5, 2, 2, 4, 4, [
        [1.0, 0.4, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.UP, 5, 10, 1, 1, 4, 4, [
        [1.0, 0.6, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value,
         Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),

])
def test_look_with_food_without_penetration(snake_direction,
                                               board_size_x,
                                               board_size_y,
                                               board_position_x,
                                               board_position_y,
                                               food_position_x,
                                               food_position_y,
                                               expected):
    s = Snake(board_size_x, board_size_y, is_penetration_active=True)
    s.direction = snake_direction
    s.body = [Block(board_position_x, board_position_y)]
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    board[food_position_y][food_position_x] = Field.APPLE.value
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    result_distances, result_targets = vision.look()
    expected_distances, expected_targets = expected
    assert result_targets == expected_targets
    assert result_distances == expected_distances



@pytest.mark.parametrize("direction, board_size_x, board_size_y, snake_head_x, snake_head_y, food_x, food_y, expected_x, expected_y", [
    (Direction.UP, 10, 10, 1, 1, 5, 8, 0.4, 0.7),
    (Direction.RIGHT, 10, 10, 1, 1, 5, 8, -0.7, 0.4),
    (Direction.DOWN, 10, 10, 1, 1, 5, 8, -0.4, -0.7),
    (Direction.LEFT, 10, 10, 1, 1, 5, 8, 0.7, -0.4),
    (Direction.UP, 20, 10, 1, 1, 5, 8, 0.2, 0.7),
    (Direction.RIGHT, 20, 10, 1, 1, 5, 8, -0.7, 0.2),
    (Direction.DOWN, 20, 10, 1, 1, 5, 8, -0.2, -0.7),
    (Direction.LEFT, 20, 10, 1, 1, 5, 8, 0.7, -0.2),
    (Direction.UP, 10, 20, 1, 1, 5, 8, 0.4, 0.35),
    (Direction.RIGHT, 10, 20, 1, 1, 5, 8, -0.35, 0.4),
    (Direction.DOWN, 10, 20, 1, 1, 5, 8, -0.4, -0.35),
    (Direction.LEFT, 10, 20, 1, 1, 5, 8, 0.35, -0.4),
    ])
def test__get_food_distance(direction, board_size_x, board_size_y, snake_head_x, snake_head_y, food_x, food_y, expected_x, expected_y):
    snake = Snake(board_size_x, board_size_y)
    snake.body = [Block(snake_head_x, snake_head_y)]
    snake.direction = direction
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    board[food_y][food_x] = Field.APPLE.value
    food = Block(food_x, food_y)
    vision = Vision(snake, board)
    dx, dy = vision._get_food_distance(food)
    assert dx == expected_x
    assert dy == expected_y

@pytest.mark.parametrize("board_size_x, board_size_y, dir_x, dir_y, penetration_active, expected", [
    (10, 10, 0.4, 0.4, False, [1, 0, 0, 1, 0, 0, 0.4, 0, 0.4, 0]),
    (10, 10, 0.4, 0.0, False, [1, 0, 0, 0, 1, 0, 0.4, 0, 0, 0]),
    (10, 10, 0.25, -0.75, False, [1, 0, 0, 0, 0, 1, 0.25, 0, 0, 0.75]),
    (10, 10, 0, 0.22, False, [0, 1, 0, 1, 0, 0, 0, 0, 0.22, 0]),
    (10, 10, 0, 0, False, [0, 1, 0, 0, 1, 0, 0, 0, 0, 0]),
    (10, 10, 0, -.8, False, [0, 1, 0, 0, 0, 1, 0, 0, 0, 0.8]),
    (10, 10, -0.55, 0.4, False, [0, 0, 1, 1, 0, 0, 0, 0.55, 0.4, 0]),
    (10, 10, -0.85, 0, False, [0, 0, 1, 0, 1, 0, 0, 0.85, 0, 0]),
    (10, 10, -0.85, -0.85, False, [0, 0, 1, 0, 0, 1, 0, 0.85, 0, 0.85]),
    (10, 10, 0.4, 0.4, True, [1, 0, 0, 1, 0, 0, 0.4, 0.6, 0.4, 0.6]),
    (10, 10, 0.4, 0.0, True, [1, 0, 0, 0, 1, 0, 0.4, 0.6, 0, 0]),
    (10, 10, 0.25, -0.75, True, [1, 0, 0, 0, 0, 1, 0.25, 0.75, 0.25, 0.75]),
    (10, 10, 0, 0.22, True, [0, 1, 0, 1, 0, 0, 0, 0, 0.22, 0.78]),
    (10, 10, 0, 0, True, [0, 1, 0, 0, 1, 0, 0, 0, 0, 0]),
    (10, 10, 0, -.8, True, [0, 1, 0, 0, 0, 1, 0, 0, 0.2, 0.8]),
    (10, 10, -0.55, 0.4, True, [0, 0, 1, 1, 0, 0, 0.45, 0.55, 0.4, 0.6]),
    (10, 10, -0.85, 0, True, [0, 0, 1, 0, 1, 0, 0.15, 0.85, 0, 0]),
    (10, 10, -0.85, -0.85, True, [0, 0, 1, 0, 0, 1, 0.15, 0.85, 0.15, 0.85]),
    (10, 10, 0.4, -0.8, False, [1, 0, 0, 0, 0, 1, 0.4, 0, 0.0, 0.8]),
    (10, 10, 0.4, -0.8, True, [1, 0, 0, 0, 0, 1, 0.4, 0.6, 0.2, 0.8]),

])
def test_get_food_direction_vector(board_size_x, board_size_y, penetration_active, dir_x, dir_y, expected):
    snake = Snake(board_size_x, board_size_y, is_penetration_active=penetration_active)
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    vision = Vision(snake, board)
    with mock.patch.object(Vision, '_get_food_distance', return_value=(dir_x, dir_y)):
        function_result = vision.get_food_direction_vector(Block(0, 0))
    assert np.array_equal(function_result.round(4), np.array(expected))

@pytest.mark.parametrize("board_size_x, board_size_y, snake_head_x, snake_head_y, food_x, food_y, raycasting_directions, expected", [
    (10, 10, 1, 1, 3, 1,
     [RaycastingDirection.NORTH, RaycastingDirection.SOUTH, RaycastingDirection.EAST, RaycastingDirection.WEST],
     [(1, Field.WALL.value), (1, Field.WALL.value), (0.2, Field.APPLE.value), (0.8, Field.APPLE.value)]
     ),
    (5, 10, 1, 1, 3, 1,
     [RaycastingDirection.NORTH, RaycastingDirection.SOUTH, RaycastingDirection.EAST, RaycastingDirection.WEST],
     [(1, Field.WALL.value), (1, Field.WALL.value), (0.4, Field.APPLE.value), (0.6, Field.APPLE.value)]
     ),
    (10, 5, 1, 1, 3, 1,
     [RaycastingDirection.NORTH, RaycastingDirection.SOUTH, RaycastingDirection.EAST, RaycastingDirection.WEST],
     [(1, Field.WALL.value), (1, Field.WALL.value), (0.2, Field.APPLE.value), (0.8, Field.APPLE.value)]
     ),
    (10, 10, 1, 1, 0, 0,
     [RaycastingDirection.NORTH_WEST, RaycastingDirection.SOUTH_EAST, RaycastingDirection.NORTH_EAST, RaycastingDirection.SOUTH_WEST],
     [(1, Field.WALL.value), (1, Field.WALL.value), (0.9, Field.APPLE.value), (0.1, Field.APPLE.value)]
     ),
    (5, 10, 1, 1, 0, 0,
     [RaycastingDirection.NORTH_WEST, RaycastingDirection.SOUTH_EAST, RaycastingDirection.NORTH_EAST, RaycastingDirection.SOUTH_WEST],
     [(1, Field.WALL.value), (1, Field.WALL.value), (1.0, Field.WALL.value), (0.2, Field.APPLE.value)]
     ),
    (8, 5, 3, 2, 0, 2,
     [RaycastingDirection.NORTH, RaycastingDirection.SOUTH, RaycastingDirection.EAST, RaycastingDirection.WEST],
     [(1, Field.WALL.value), (1, Field.WALL.value), (0.625, Field.APPLE.value), (0.375, Field.APPLE.value)]
     ),
    (12, 9, 9, 2, 5, 1,
     [RaycastingDirection.NORTH_EAST],
     [(8/9, Field.APPLE.value)]
     ),
])

def test__detect_obstacle_in_direction_with_wall_transparency(board_size_x, board_size_y, snake_head_x, snake_head_y, food_x, food_y, raycasting_directions, expected):
    snake = Snake(board_size_x, board_size_y)
    snake.body = [Block(snake_head_x, snake_head_y)]
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    board[food_y][food_x] = Field.APPLE.value
    board = snake.project_snake_on_board(board)
    vision = Vision(snake, board)
    for i, raycasting_direction in enumerate(raycasting_directions):
        function_result = vision._detect_obstacle_in_direction_with_wall_transparency(raycasting_direction)
        assert function_result ==  expected[i]