from dataclasses import dataclass
from collections import UserDict


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def get_neighbours(self) -> set["Position"]:
        return {
            Position(self.x + x, self.y + y)
            for x in [-1, 0, 1]
            for y in [-1, 0, 1]
            if (x, y) != (0, 0)
        }


class Grid(UserDict[Position, bool]):
    def __getitem__(self, position: Position) -> bool:
        return self.data.get(position, False)

    def get_alive_neighbours_count(self, position: Position) -> int:
        return sum(self[p] for p in position.get_neighbours())

    def will_survive(self, position: Position) -> bool:
        '''
            An alive cell with less or more neighbours
            will die by under/over population
        '''
        return self.get_alive_neighbours_count(position) in (2, 3)

    def will_be_born(self, position: Position) -> bool:
        return self.get_alive_neighbours_count(position) == 3

    def next_cell_state(self, position: Position) -> bool:
        if self[position]:
            return self.will_survive(position)
        else:
            return self.will_be_born(position)

    def next_grid(self) -> "Grid":
        to_analyze = set(self.keys())
        for cell in self.keys():
            if self[cell]:
                to_analyze |= cell.get_neighbours()

        return Grid({
            cell: self.next_cell_state(cell)
            for cell in to_analyze
        })