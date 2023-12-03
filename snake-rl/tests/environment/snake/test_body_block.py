from src.environment.snake.block import Block


def test_shouldReturnTrue_whenExecuted():
    x1 = Block(0, 0)
    x2 = Block(0, 0)
    comparison = x1 == x2
    assert comparison == True

def test_shouldReturnFalse_whenExecuted():
    x1 = Block(1, 0)
    x2 = Block(0, 0)
    comparison = x1 == x2
    assert comparison == False


def test_shouldReturnBodyBlockWithRandomCoordinates_whenExecuted():
    block = Block.get_random_block(10, 10)
    assert type(block).__name__ == 'Block'
    assert block.x < 10
    assert block.y < 10
    assert block.x >= 0
    assert block.y >= 0