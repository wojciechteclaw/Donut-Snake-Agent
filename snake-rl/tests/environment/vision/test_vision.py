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
        s = Snake(10, 10, "http://localhost:5001")
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
    x_size = 5
    y_size = 5
    with mock.patch.object(random, 'randint', return_value=2):
        s = Snake(x_size, y_size, "http://localhost:5001")
    board = np.ones((x_size, y_size)) * Field.EMPTY.value
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    distance, targets = vision._detect_obstacle_in_direction(direction)
    assert distance == (expected[0] / (x_size - 1))
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
    x_size = 10
    y_size = 10
    with mock.patch.object(random, 'randint', return_value=5):
        s = Snake(x_size, y_size, "http://localhost:5001")
    board = np.ones((x_size, y_size)) * Field.EMPTY.value
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
    assert function_result == (result[0]/(x_size - 1), result[1])

@pytest.mark.parametrize("raycast_direction, board_size_x, board_size_y, board_position_x, board_position_y, expected", [
    (RaycastingDirection.NORTH, 5, 5, 4, 2, (2, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 5, 5, 4, 2, (0, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 5, 5, 3, 2, (1, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 10, 10, 0, 0, (9, Field.WALL.value)),
    (RaycastingDirection.EAST, 5, 5, 4, 2, (0, Field.WALL.value)),
    (RaycastingDirection.EAST, 5, 5, 3, 2, (1, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 10, 10, 9, 5, (0, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 10, 10, 8, 5, (1, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 10, 8, 5, (5, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 10, 0, 0, (0, Field.WALL.value)),
    (RaycastingDirection.NORTH, 10, 10, 9, 5, (4, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 10, 9, 4, (4, Field.WALL.value)),
    (RaycastingDirection.EAST, 10, 10, 9, 4, (0, Field.WALL.value)),
    (RaycastingDirection.WEST, 20, 20, 19, 19, (19, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 20, 20, 18, 19, (1, Field.WALL.value)),
    (RaycastingDirection.SOUTH_WEST, 20, 10, 18, 9, (9, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 5, 5, 4, 2, (0, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 5, 5, 3, 2, (1, Field.WALL.value)),
    (RaycastingDirection.NORTH_EAST, 10, 5, 0, 0, (4, Field.WALL.value)),
    (RaycastingDirection.EAST, 5, 5, 4, 2, (0, Field.WALL.value)),
    (RaycastingDirection.EAST, 5, 5, 3, 2, (1, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 10, 10, 9, 5, (0, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 10, 10, 8, 5, (1, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 10, 8, 5, (5, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 10, 0, 0, (0, Field.WALL.value)),
    (RaycastingDirection.NORTH, 10, 10, 9, 5, (4, Field.WALL.value)),
    (RaycastingDirection.SOUTH, 10, 10, 9, 4, (4, Field.WALL.value)),
    (RaycastingDirection.EAST, 10, 10, 9, 4, (0, Field.WALL.value)),
    (RaycastingDirection.WEST, 20, 20, 19, 19, (19, Field.WALL.value)),
    (RaycastingDirection.SOUTH_EAST, 20, 20, 18, 19, (1, Field.WALL.value)),
    (RaycastingDirection.SOUTH_WEST, 20, 10, 18, 9, (9, Field.WALL.value))
])
def test_raycaster_in_boundary_conditions(raycast_direction, board_size_x, board_size_y, board_position_x, board_position_y, expected):
    s = Snake(board_size_x, board_size_y, "http://localhost:5001")
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    s.body = [Block(board_position_x, board_position_y)]
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    function_result = vision._detect_obstacle_in_direction(raycast_direction)
    assert function_result == (expected[0]/(max(board_size_y, board_size_x) - 1), expected[1])

@pytest.mark.parametrize("""raycast_direction,
                            board_size_x,
                            board_size_y,
                            board_position_x,
                            board_position_y,
                            food_position_x,
                            food_position_y,
                            obstacle_type,
                            expected_distance""",[
                             (RaycastingDirection.NORTH, 5, 5, 4, 2, 4, 4, Field.APPLE.value, 2),
                             (RaycastingDirection.NORTH_EAST, 5, 5, 0, 0, 4, 4, Field.APPLE.value, 4),
                             (RaycastingDirection.NORTH_EAST, 5, 5, 0, 0, 4, 4, Field.SNAKE_BODY.value, 4),
                             (RaycastingDirection.NORTH_EAST, 5, 5, 3, 2, 4, 3, Field.WALL.value, 1),
                             (RaycastingDirection.EAST, 20, 20, 10, 5, 15, 5, Field.APPLE.value, 5),
                             (RaycastingDirection.SOUTH_EAST, 10, 10, 1, 4, 2, 3, Field.SNAKE_BODY.value, 1),
])
def test_raycaster_in_boundary_conditions_with_obstacles(raycast_direction,
                                                         board_size_x,
                                                         board_size_y,
                                                         board_position_x,
                                                         board_position_y,
                                                         food_position_x,
                                                         food_position_y,
                                                         obstacle_type,
                                                         expected_distance):
    s = Snake(board_size_x, board_size_y, "http://localhost:5001")
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    s.body = [Block(board_position_x, board_position_y)]
    board[food_position_y][food_position_x] = obstacle_type
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    function_result = vision._detect_obstacle_in_direction(raycast_direction)
    assert function_result == (expected_distance/(max(board_size_x, board_size_y) - 1), obstacle_type)

@pytest.mark.parametrize("""snake_direction,board_size_x,board_size_y,board_position_x,board_position_y,food_position_x,food_position_y,expected""", [
    (Direction.UP, 5, 5, 2, 2, 4, 4, [
        [2, 2, 2, 2, 2, 2, 2, 2],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.UP, 5, 5, 1, 1, 4, 4, [
        [3, 3, 3, 1, 1, 1, 1, 1],
        [Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),
    (Direction.RIGHT, 5, 5, 2, 2, 4, 4, [
        [2, 2, 2, 2, 2, 2, 2, 2],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value]
    ]),
    (Direction.RIGHT, 5, 5, 1, 1, 4, 4, [
        [3, 1, 1, 1, 1, 1, 3, 3],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value]
    ]),
    (Direction.LEFT, 5, 5, 1, 1, 4, 4, [
        [1, 1, 3, 3, 3, 1, 1, 1],
        [Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.APPLE.value, Field.WALL.value, Field.WALL.value, Field.WALL.value, Field.WALL.value]
    ]),
])
def test_look_without_food(snake_direction,
                           board_size_x,
                           board_size_y,
                           board_position_x,
                           board_position_y,
                           food_position_x,
                           food_position_y,
                           expected):
    s = Snake(board_size_x, board_size_y, "http://localhost:5001")
    s.direction = snake_direction
    s.body = [Block(board_position_x, board_position_y)]
    board = np.ones((board_size_y, board_size_x)) * Field.EMPTY.value
    board[food_position_y][food_position_x] = Field.APPLE.value
    board = s.project_snake_on_board(board)
    vision = Vision(s, board)
    result_distances, result_targets = vision.look()
    expected_distances, expected_targets = expected
    normalizer = max(board_size_x, board_size_y) - 1
    assert result_targets == expected_targets
    assert result_distances == [x / normalizer for x in expected_distances]
