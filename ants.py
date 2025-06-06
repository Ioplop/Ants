# Defines classes for ants, their world, their food, etc.
from __future__ import annotations
from typing import List, Dict
from signals import Signal
from utils import Position

class Cell:
    """
    Holds ants, food and signals
    """
    def __init__(self, pos: Position):
        # Position of this cell
        self.pos = pos
        # A cell can hold only a single ant at a time
        self.ant : Ant = None
        # A dict of all signals in the cell
        self.signals: Dict[str, Signal] = {}
        # How much food this cell holds.
        self.food : float = 0.0
    
    def grab_food(self, amount: float) -> float:
        """
        Returns as much food as possible, up to the amount of food contained in the cell.
        Removes the amount returned from the cell's food storage.

        Args:
            amount (float): Maximum food returned

        Returns:
            float: How much food is returned
        """
        if self.food >= amount:
            self.food -= amount
            return amount
        else:
            amount = self.food
            self.food = 0.0
            return amount
    
    def check_signal(self, key: str) -> float:
        """
        Returns the intensity of a specific signal in this cell.

        Args:
            key (str): Identifier for the signal to search for

        Returns:
            float: Intensity of the given signal
        """
        if key in self.signals:
            return self.signals[key].intensity
        else:
            return 0.0
    
    def add_signal(self, signal: Signal):
        """
        Increases signal intensity in the cell.

        Args:
            signal (Signal): Signal to increase
        """
        if signal.id in self.signals:
            self.signals[signal.id].increase(signal)
    
    
    
class World:
    """
    A class that holds and works with a grid of Cells.
    Cells are responsible for holding everything in the world: Ants, Food, Signals, Etc.
    """
    
    
class Ant:
    """
    AN ANT!
    """