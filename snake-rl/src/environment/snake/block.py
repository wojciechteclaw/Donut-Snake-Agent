import random


class Block:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, head: 'Block') -> bool:
        """Compares two body blocks and returns `True` if x1 == x2 and y1 == y2, otherwise returns `False`."""
        return self.x == head.x and self.y == head.y

    def __sub__(self, other: 'Block') -> tuple[int, int]:
        """Subtracts two body blocks and returns a tuple of x and y coordinates."""
        return other.x - self.x, other.y - self.y

    @property
    def position(self) -> tuple[int, int]:
        """Returns the position of the body block as a tuple of x and y coordinates."""
        return self.x, self.y

    @staticmethod
    def get_random_block(max_x: int, max_y: int) -> 'Block':
        """Returns a random BodyBlock within the given range.
        ----------
        Parameters
        ----------
        max_x : int
            The maximum x coordinate.
        max_y : int
            The maximum y coordinate.
        """
        x = random.randint(0, max_x - 1)
        y = random.randint(0, max_y - 1)
        return Block(x, y)
