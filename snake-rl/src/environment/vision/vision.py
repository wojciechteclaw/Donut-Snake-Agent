import numpy as np

from src.environment.enums.direction import Direction
from src.environment.enums.field import Field
from src.environment.enums.raycasting_direction import RaycastingDirection
from src.environment.snake.block import Block
from src.environment.snake.snake import Snake
from collections import deque


class Vision:

    def __init__(self, snake: Snake, board: np.ndarray):
        self.snake = snake
        self.is_penetration_active = snake.is_penetration_active
        self.board = board
        self._max_distance = max(self.snake.size_x, self.snake.size_y)
        self._x_max_distance = self.snake.size_x
        self._y_max_distance = self.snake.size_y
        self._diag_max_distance = min(self._x_max_distance, self._y_max_distance)
        self.__raycasting_directions = deque([RaycastingDirection.NORTH, RaycastingDirection.NORTH_EAST,
                                       RaycastingDirection.EAST, RaycastingDirection.SOUTH_EAST,
                                       RaycastingDirection.SOUTH, RaycastingDirection.SOUTH_WEST,
                                       RaycastingDirection.WEST, RaycastingDirection.NORTH_WEST])

    def _rotate_from_direction(self):
        direction_value = self.snake.direction.value
        raycasting_directions = self.__raycasting_directions.copy()
        raycasting_directions.rotate(-direction_value * 2)
        return raycasting_directions

    def _get_direction_normalization_factor(self, direction:RaycastingDirection):
        x, y = direction.value
        if x != 0 and y != 0:
            return self._diag_max_distance
        elif x != 0:
            return self._x_max_distance
        else:
            return self._y_max_distance

    def _detect_obstacle_in_direction(self, direction:RaycastingDirection):
        x, y = self.snake.head.position
        x_step, y_step = direction.value
        normalization_factor = self._get_direction_normalization_factor(direction)
        number_of_steps_in_direction = 0
        intersecting_categories = [Field.APPLE.value, Field.SNAKE_BODY.value, Field.WALL.value]
        while True:
            if self.board[y][x] in intersecting_categories:
                distance = number_of_steps_in_direction / normalization_factor
                return distance, self.board[y][x]
            # boundary check and increment
            if (self.snake.size_x > x + x_step >= 0 and self.snake.size_y > y + y_step >= 0):
                x = x + x_step
                y = y + y_step
                number_of_steps_in_direction += 1
            else:
                break
        return number_of_steps_in_direction / normalization_factor, Field.WALL.value

    def _detect_obstacle_in_direction_with_wall_transparency(self, direction:RaycastingDirection):
        x, y = self.snake.head.position
        x_step, y_step = direction.value
        normalization_factor = self._get_direction_normalization_factor(direction)
        number_of_steps_in_direction = 0
        intersecting_categories = [Field.APPLE.value, Field.SNAKE_BODY.value]
        while number_of_steps_in_direction < normalization_factor:
            if self.board[y][x] in intersecting_categories:
                distance = number_of_steps_in_direction / normalization_factor
                return distance, self.board[y][x]
            else:
                x = (x + x_step) % self._x_max_distance
                y = (y + y_step) % self._y_max_distance
                number_of_steps_in_direction += 1
        return 1., Field.WALL.value

    def get_food_direction_vector(self, food:Block):
        x, y = self._get_food_direction(food)
        indicators = np.zeros(10)
        # binary indicators
        indicators[0] = x > 0
        indicators[1] = x == 0
        indicators[2] = x < 0
        indicators[3] = y > 0
        indicators[4] = y == 0
        indicators[5] = y < 0
        # distance indicators
        indicators[6] = x * indicators[0]
        indicators[7] = np.abs(x) * indicators[2]
        indicators[8] = y * indicators[3]
        indicators[9] = np.abs(y) * indicators[5]
        return indicators

    def _get_food_direction(self, food: Block):
        x, y = self.snake.head - food
        direction = self.snake.direction
        match direction:
            case Direction.UP:
                return np.array([x / self._x_max_distance, y / self._y_max_distance])
            case Direction.RIGHT:
                return np.array([-y / self._y_max_distance, x / self._x_max_distance])
            case Direction.DOWN:
                return np.array([-x / self._x_max_distance, -y / self._y_max_distance])
            case Direction.LEFT:
                return np.array([y / self._y_max_distance, -x / self._x_max_distance])

    def look(self):
        raycasting_directions = self._rotate_from_direction()
        distances, targets = [], []
        detection_function = self._detect_obstacle_in_direction_with_wall_transparency if self.is_penetration_active else self._detect_obstacle_in_direction
        for direction in raycasting_directions:
            distance, target = detection_function(direction)
            distances.append(distance), targets.append(target)
        return distances, targets


