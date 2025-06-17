from __future__ import annotations
from enum import IntEnum
from dataclasses import dataclass
from functools import cached_property
import warnings

# Defines positional classes

class Direction(IntEnum):
    """
    Simple direction enumerator to handle directions in a simpler and readable way
    """
    # The direction codes were picked by starting up and turning counter clockwise.
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    
class DirectionError(Exception):
    pass

@dataclass(frozen=True)
class Position:
    x : int
    y : int
    
    # A 2d vector that works with int numbers and usually represents a position on a grid
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        warnings.warn(f"Warning: Tried to compare Position to {type(other)}")
        return NotImplemented
    
    def __add__(self, other: Position) -> Position:
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        raise TypeError(f"Cannot add Position to {type(other)}")
    
    def __sub__(self, other: Position) -> Position:
        if isinstance(other, Position):
            return Position(self.x - other.x, self.y - other.y)
        raise TypeError(f"Cannot subtract {type(other)} from Position")
    
    def __mul__(self, other: int) -> Position:
        if isinstance(other, int):
            return Position(self.x * other, self.y * other)
        elif isinstance(other, float):
            return Position(round(self.x * other), round(self.y * other))
        raise TypeError(f"Cannot multiply Position with {type(other)}")

    def __truediv__(self, other: int) -> Position:
        if isinstance(other, int) or isinstance(other, float):
            return Position(self.x / other, self.y/other)
        return TypeError(f"Cannot divide Position by {type(other)}")
    
    def __rmul__(self, other: int) -> Position:
        return self * other
    
    def __mod__(self, other: Position) -> Position:
        # This one is used for cycling positions around a world.
        if isinstance(other, Position):
            return Position(self.x % other.x, self.y % other.y)
        raise TypeError(f"Cannot mod Position with {type(other)}")
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"Position({self.x}, {self.y})"
    
    def move_dir(self, direction: Direction, distance: int = 1) -> Position:
        """
        Returns a displaced position in a specific direction and by a specific amount

        Args:
            direction (Direction): Direction in which to displace the position.
            distance (int, optional): Distance to displace. Defaults to 1.

        Raises:
            DirectionError: Direction invalid

        Returns:
            Position: Displaced position
        """
        
        # In grids, the y axis is inverted. (0 is upmost, and we go down from there)
        try:
            return self + DIRECTION_VECTORS[direction] * distance
        except KeyError:
            raise DirectionError(f"Cannot move position in direction \"{direction}\" because it's not a valid direction.")

    def move(self, x: int = 0, y: int = 0) -> Position:
        """Moves a vector by x and y coors.
        Helps to avoid instancing positions for single operations where it's not needed.

        Args:
            x (int, optional): Displacement in x axis. Defaults to 0.
            y (int, optional): Displacement in y axis. Defaults to 0.

        Raises:
            TypeError: X or Y are not ints

        Returns:
            Position: Displaced position
        """
        if isinstance(x, int) and isinstance(y, int):
            return Position(self.x + x, self.y + y)
        raise TypeError(f"Tried moving a position by {type(x)} and {type(y)} but a position can only be moved by ints.")
    
    def distance_to(self, other: Position) -> int:
        if isinstance(other, Position):
            return max(abs(self.x - other.x), abs(self.y - other.y))
        raise TypeError(f"Cannot calculate distance between Position and {type(other)}")

DIRECTION_VECTORS = {
    Direction.UP:    Position(0, -1),
    Direction.LEFT:  Position(-1, 0),
    Direction.DOWN:  Position(0, 1),
    Direction.RIGHT: Position(1, 0),
}

@dataclass(frozen=True)
class Vector:
    x : float
    y : float
    
    # A 2d vector that works with int numbers and usually represents a position on a grid
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        warnings.warn(f"Warning: Tried to compare  {type(self)} to {type(other)}")
        return NotImplemented
    
    def __add__(self, other: Vector) -> Vector:
        if isinstance(other, Vector) or isinstance(other, Position):
            return Position(self.x + (float)other.x, self.y + (float)other.y)
        raise TypeError(f"Cannot add  {type(self)} to {type(other)}")
    
    def __sub__(self, other: Vector) -> Vector:
        if isinstance(other, Vector) or isinstance(other, Position):
            return Position(self.x - (float)other.x, self.y - (float)other.y)
        raise TypeError(f"Cannot subtract {type(other)} from {type(self)}")
    
    def __mul__(self, other: float) -> Vector:
        if isinstance(other, float) or isinstance(other, int):
            return Vector(self.x * other, self.y * other)
        raise TypeError(f"Cannot multiply  {type(self)} with {type(other)}")

    def __truediv__(self, other: float) -> Vector:
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x / other, self.y/other)
        return TypeError(f"Cannot divide  {type(self)} by {type(other)}")
    
    def __rmul__(self, other: float) -> Vector:
        return self * other
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"Position({self.x}, {self.y})"
    
    def sqr_magnitude(self) -> float:
        return self.x*self.x + self.y*self.y
    
    @cached_property
    def magnitude(self) -> float:
        return self.sqr_magnitude()**0.5
    
    def move_dir(self, direction: Direction, distance: int = 1) -> Position:
        """
        Returns a displaced position in a specific direction and by a specific amount

        Args:
            direction (Direction): Direction in which to displace the position.
            distance (int, optional): Distance to displace. Defaults to 1.

        Raises:
            DirectionError: Direction invalid

        Returns:
            Position: Displaced position
        """
        
        # In grids, the y axis is inverted. (0 is upmost, and we go down from there)
        try:
            return self + DIRECTION_VECTORS[direction] * distance
        except KeyError:
            raise DirectionError(f"Cannot move position in direction \"{direction}\" because it's not a valid direction.")

    def move(self, x: int = 0, y: int = 0) -> Position:
        """Moves a vector by x and y coors.
        Helps to avoid instancing positions for single operations where it's not needed.

        Args:
            x (int, optional): Displacement in x axis. Defaults to 0.
            y (int, optional): Displacement in y axis. Defaults to 0.

        Raises:
            TypeError: X or Y are not ints

        Returns:
            Position: Displaced position
        """
        if isinstance(x, int) and isinstance(y, int):
            return Position(self.x + x, self.y + y)
        raise TypeError(f"Tried moving a position by {type(x)} and {type(y)} but a position can only be moved by ints.")
    
    def distance_to(self, other: Position) -> int:
        if isinstance(other, Position):
            return max(abs(self.x - other.x), abs(self.y - other.y))
        raise TypeError(f"Cannot calculate distance between Position and {type(other)}")