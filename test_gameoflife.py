import pytest

from gameoflife import Position, Grid


# Any live cell with fewer than two live neighbours dies,
#   as if by underpopulation.
#
# Any live cell with two or three live neighbours lives
#   on to the next generation.
#
# Any live cell with more than three live neighbours dies,
#   as if by overpopulation.
#
# Any dead cell with exactly three live neighbours becomes a live cell,
#   as if by reproduction.

# {
# Inmutable(x, y) -> Bool
# }


def test_create_position() -> None:
    position = Position(3, 5)
    assert position.x == 3
    assert position.y == 5


def test_create_empty_grid() -> None:
    grid = Grid()
    assert len(grid) == 0


def test_get_cells() -> None:
    grid = Grid(
        {
            Position(0, 0): True,
            Position(0, 1): False,
        }
    )
    assert grid[Position(0, 0)] == True
    assert grid[Position(0, 1)] == False
    assert grid[Position(0, 2)] == False


def test_get_neighbours() -> None:
    position = Position(0, 0)
    assert position.get_neighbours() == {
        Position(-1, -1),
        Position(-1, 0),
        Position(-1, 1),
        Position(0, -1),
        Position(0, 1),
        Position(1, -1),
        Position(1, 0),
        Position(1, 1),
    }


def test_get_alive_neighbours_count() -> None:
    # Test data
    #   0 1 2
    # 0 T F F
    # 1 F T F
    # 2 F T F
    grid = Grid(
        {
            Position(0, 0): True,
            Position(0, 1): False,
            Position(1, 1): True,
            Position(2, 1): True,
        }
    )
    assert grid.get_alive_neighbours_count(Position(0, 0)) == 1
    assert grid.get_alive_neighbours_count(Position(0, 1)) == 2
    assert grid.get_alive_neighbours_count(Position(3, 3)) == 0


# Any live cell with two or three live neighbours lives
#   on to the next generation.
def test_will_survive():
    # Test data
    #   0 1 2
    # 0 T F F
    # 1 F T F
    # 2 F T F
    grid = Grid(
        {
            Position(0, 0): True,
            Position(0, 1): False,
            Position(1, 1): True,
            Position(2, 1): True,
        }
    )

    assert grid.will_survive(Position(0, 0)) == False
    assert grid.will_survive(Position(1, 1)) == True


# Any dead cell with exactly three live neighbours becomes a live cell,
#   as if by reproduction.
def test_will_be_born():
    # Test data
    #   0 1 2
    # 0 T F F
    # 1 F T T
    # 2 F T T
    grid = Grid(
        {
            Position(0, 0): True,
            Position(1, 1): True,
            Position(2, 1): True,
            Position(1, 2): True,
            Position(2, 2): True,
        }
    )

    assert grid.will_be_born(Position(0, 1)) == True
    assert grid.will_be_born(Position(0, 2)) == False
    assert grid.will_be_born(Position(1, 1)) == False
    assert grid.will_be_born(Position(42, 42)) == False


def test_next_cell_state():
    # Test data
    #   0 1 2
    # 0 T F F
    # 1 F T T
    # 2 F T T
    grid = Grid(
        {
            Position(0, 0): True,
            Position(1, 1): True,
            Position(2, 1): True,
            Position(1, 2): True,
            Position(2, 2): True,
        }
    )

    assert grid.next_cell_state(Position(0, 0)) == False
    assert grid.next_cell_state(Position(0, 1)) == True
    assert grid.next_cell_state(Position(1, 1)) == False
    assert grid.next_cell_state(Position(1, 0)) == True
    assert grid.next_cell_state(Position(2, 2)) == True
    assert grid.next_cell_state(Position(42, 42)) == False


def test_next_grid():
    # Test data
    #   0 1 2
    # 0 T F F
    # 1 F T T
    # 2 F T T

    # 0 T T F
    # 1 T F T
    # 2 F T T

    grid = Grid(
        {
            Position(0, 0): True,
            Position(1, 1): True,
            Position(2, 1): True,
            Position(1, 2): True,
            Position(2, 2): True,
        }
    )

    next_grid = grid.next_grid()

    assert next_grid[Position(0, 0)] == False
    assert next_grid[Position(0, 1)] == True
    assert next_grid[Position(1, 1)] == False
    assert next_grid[Position(1, 0)] == True
    assert next_grid[Position(2, 2)] == True
    assert next_grid[Position(42, 42)] == False
