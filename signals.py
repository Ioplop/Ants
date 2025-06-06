# Defines classes for signaling using "pheromones"
from __future__ import annotations

class Signal:
    def __init__(self, id: str, intensity: float, decay: float = 1.0):
        self.id = id
        self.intensity = intensity
        self.decay = decay
    
    def decrease(self, dt: float) -> bool:
        """Decrease signal intensity based on its decay.
        Returns wether or not the signal reached zero.
        If signal intensity is 0, returns True

        Args:
            dt (float): Amount of time to apply signal decay

        Returns:
            bool: True if signal intensity reaches 0
        """
        self.intensity -= self.decay * dt
        if self.intensity <= 0:
            self.intensity = 0
            return True
        return False
    
    def increase(self, signal: Signal):
        """
        Increases signal intensity by the amount of another singal.

        Args:
            signal (Signal): Another signal to add to this one.
        """
        if self.id != signal.id:
            raise Exception(f"Tried to add two signals that don't share ids: {self.id} + {signal.id}")
        self.decay = (signal.decay * signal.intensity + self.decay * self.intensity) / (signal.intensity + self.intensity)
        self.intensity += signal.intensity