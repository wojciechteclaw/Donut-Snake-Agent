import numpy as np
from copy import copy
from src.environment.enums.actions import Action
from src.environment.enums.direction import Direction
from src.environment.enums.field import Field
from src.environment.snake.block import Block


class Snake:

    def __init__(self, size_x:int, size_y:int , is_penetration_active:bool = False):
        self.body:[Block] = []
        self._direction: Direction = Direction.RIGHT
        self.size_x = size_x
        self.size_y = size_y
        self.alive = True
        self.is_penetration_active = is_penetration_active
        self.get_random_head()
        self.previous_tail_brick = None
        self.previous_direction = None
        self.reset()

    def reset(self):
        self.body = []
        self._direction = Direction.RIGHT
        self.alive = True
        self.previous_tail_brick = None
        self.previous_direction = None
        self.get_random_head()

    def get_random_head(self):
        random_head = Block.get_random_block(self.size_x, self.size_y)
        self.body = [random_head]

    def append_food(self):
        self.body.append(self.previous_tail_brick)
        self.previous_tail_brick = None

    def insert_body(self, body:Block):
        self.body.insert(0, body)

    def move(self, action:int):
        action_object = Snake.get_action_from_number(action)
        direction = self.get_direction_from_action(action_object)
        self.modify_snake(direction)

    def modify_snake(self, direction:Direction):
        new_head = copy(self.head)
        self.previous_direction = self.direction
        self.direction = direction
        if self.is_penetration_active:
            new_head = self.__move_block_with_penetration(new_head, direction)
        else:
            new_head = self.__move_block_without_penetration(new_head, direction)
        is_valid = self.is_new_head_valid(new_head)
        if not is_valid:
            self.alive = False
        self.body.insert(0, new_head)
        self.previous_tail_brick = self.body[-1]
        self.body.pop()

    def __move_block_with_penetration(self, block:Block, direction:Direction):
        match direction:
            case Direction.UP:
                block.y = (block.y + 1) % self.size_y
            case Direction.DOWN:
                block.y = (block.y - 1) % self.size_y
            case Direction.LEFT:
                block.x = (block.x - 1) % self.size_x
            case Direction.RIGHT:
                block.x = (block.x + 1) % self.size_x
        return block

    def __move_block_without_penetration(self, block:Block, direction:Direction):
        match direction:
            case Direction.UP:
                block.y += 1
            case Direction.DOWN:
                block.y -= 1
            case Direction.LEFT:
                block.x -= 1
            case Direction.RIGHT:
                block.x += 1
        return block

    def is_new_head_valid(self, new_head:Block) -> bool:
        if not self.is_move_in_boundries(new_head):
            return False
        if self.is_self_clash(new_head):
            return False
        return True

    def is_self_clash(self, new_head: Block) -> bool:
        for body_block in self.body:
            if new_head == body_block:
                return True
        return False

    def get_direction_vector(self) -> np.ndarray:
        vector = np.zeros(4)
        vector[self.direction.value] = 1
        return vector

    def project_snake_on_board(self, board:np.ndarray):
        try:
            board[self.body[0].y][self.body[0].x] = Field.SNAKE_HEAD.value
            for block in self.body[1:]:
                board[block.y][block.x] = Field.SNAKE_BODY.value
        except:
            pass
        return np.array(board)

    @property
    def head(self) -> Block:
        return self.body[0]

    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, direction:Direction):
        self._direction = direction

    @staticmethod
    def get_action_from_number(action_number:int) -> Action:
        match action_number:
            case 0:
                return Action.LEFT
            case 1:
                return Action.STRAIGHT
            case 2:
                return Action.RIGHT
        return Action.INVALID

    @staticmethod
    def get_direction_from_number(direction_number:int) -> Direction:
        match direction_number:
            case 0:
                return Direction.UP
            case 1:
                return Direction.RIGHT
            case 2:
                return Direction.DOWN
            case 3:
                return Direction.LEFT
        return Direction.INVALID

    def get_direction_from_action(self, action:Action) -> Direction:
        new_direction_value = self.direction.value + action.value
        new_direction = Snake.get_direction_from_number(new_direction_value % 4)
        return new_direction

    def is_move_in_boundries(self, block:Block) -> bool:
        return -1 < block.x < self.size_x and -1 < block.y < self.size_y
