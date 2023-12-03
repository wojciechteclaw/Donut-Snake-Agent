from unittest import mock
import pytest
import random
from src.environment.enums.direction import Direction
from src.environment.enums.actions import Action
from src.environment.snake.block import Block
from src.environment.snake.snake import Snake


@pytest.mark.parametrize("width, height", [
                            (5, 5),
                            (10, 10),
                            (30, 30)]
                         )
def test_randomPlacementOfSnake(width, height):
    snake = Snake(width, height)
    assert snake.body[0].x < width
    assert snake.body[0].y < height
    assert snake.body[0].x >= 0
    assert snake.body[0].y >= 0

def test_insertBody():
    with mock.patch.object(random, 'randint', return_value=5):
        s = Snake(10, 10)
    s.insert_body(Block(4, 5))
    assert s.head.x == 4
    assert s.head.y == 5

def test_isSelfClash():
    with mock.patch.object(random, 'randint', return_value=5):
        s = Snake(10, 10)
    s.insert_body(Block(4, 5))
    s.insert_body(Block(4, 4))
    assert s.is_self_clash(Block(5, 4)) == False
    assert s.is_self_clash(Block(5, 5)) == True

@pytest.mark.parametrize("direction, expected", [(Direction.UP, Block(5, 6)),
                                                 (Direction.DOWN, Block(5, 4)),
                                                 (Direction.LEFT, Block(4, 5)),
                                                 (Direction.RIGHT, Block(6, 5))]
                         )
def test_move(direction, expected):
    with mock.patch.object(random, 'randint', return_value=5):
        s = Snake(10, 10)
    s.modify_snake(direction)
    assert s.head == expected

@pytest.mark.parametrize("x_y_coord, direction, expected", [(0, Direction.DOWN, Block(0, 9)),
                                                            (0, Direction.LEFT, Block(9, 0)),
                                                            (9, Direction.UP, Block(9, 0)),
                                                            (9, Direction.RIGHT, Block(0, 9))]
                         )
def test_moveWithWallPenetration(x_y_coord, direction, expected):
    s = Snake(10, 10, is_penetration_active=True)
    s.head.x = x_y_coord
    s.head.y = x_y_coord
    s.modify_snake(direction)
    assert s.head == expected


@pytest.mark.parametrize("action, direction, expected", [
                            # left
                            (Action.STRAIGHT, Direction.LEFT, Direction.LEFT),
                            (Action.LEFT, Direction.LEFT, Direction.DOWN),
                            (Action.RIGHT, Direction.LEFT, Direction.UP),
                            # up
                            (Action.STRAIGHT, Direction.UP, Direction.UP),
                            (Action.LEFT, Direction.UP, Direction.LEFT),
                            (Action.RIGHT, Direction.UP, Direction.RIGHT),
                            # right
                            (Action.STRAIGHT, Direction.RIGHT, Direction.RIGHT),
                            (Action.LEFT, Direction.RIGHT, Direction.UP),
                            (Action.RIGHT, Direction.RIGHT, Direction.DOWN),
                            # down
                            (Action.STRAIGHT, Direction.DOWN, Direction.DOWN),
                            (Action.LEFT, Direction.DOWN, Direction.RIGHT),
                            (Action.RIGHT, Direction.DOWN, Direction.LEFT)]
                         )
def test_getDirectionFromAction(action, direction, expected):
    with mock.patch.object(random, 'randint', return_value=5):
        s = Snake(10, 10)
        s.direction = direction
    s.get_direction_from_action(action)

@pytest.mark.parametrize("x_y_coord, direction, expected", [(0, Direction.DOWN, False),
                                                            (0, Direction.LEFT, False),
                                                            (9, Direction.UP, False),
                                                            (9, Direction.RIGHT, False),
                                                            (0, Direction.UP, True),
                                                            (0, Direction.RIGHT, True),
                                                            (9, Direction.DOWN, True),
                                                            (9, Direction.LEFT, True)]
                         )
def test_isMoveInBoundries(x_y_coord, direction, expected):
    s = Snake(10, 10, is_penetration_active=False)
    s.head.x = x_y_coord
    s.head.y = x_y_coord
    s.modify_snake(direction)
    assert s.is_move_in_boundries(s.head) == expected

@pytest.mark.parametrize("x_y_coord, direction, expected", [(0, Direction.DOWN, False),
                                                            (0, Direction.LEFT, False),
                                                            (9, Direction.UP, False),
                                                            (9, Direction.RIGHT, False)]
                         )
def test_aliveStatus(x_y_coord, direction, expected):
    s = Snake(10, 10, is_penetration_active=False)
    s.head.x = x_y_coord
    s.head.y = x_y_coord
    s.modify_snake(direction)
    assert s.alive == expected

def test_reset():
    s = Snake(10, 10)
    s.reset()
    s.body = [Block(5, 5), Block(5, 4), Block(5, 3), Block(5, 2)]
    s.alive = False
    assert s.head.x == 5
    assert s.head.y == 5
    with mock.patch.object(random, 'randint', return_value=5):
        s.reset()
    assert s.head.x == 5
    assert s.head.y == 5
    assert s.alive == True
    assert s.direction == Direction.RIGHT
    assert len(s.body) == 1

def test_appendFood():
    with mock.patch.object(random, 'randint', return_value=5):
        s = Snake(10, 10)
    s.direction = Direction.RIGHT
    s.move(1)
    assert s.head.x == 6
    assert s.head.y == 5
    s.previous_tail_brick = Block(5, 5)
    s.append_food()
    assert len(s.body) == 2
    assert s.previous_tail_brick == None