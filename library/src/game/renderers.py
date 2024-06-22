import abc
from game.models import AbelardeState, GameState, HeloiseState

class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def renderAbelarde(self, game_state : AbelardeState) -> None:
        """Render given game state."""

    def renderHeloise(self, game_state : HeloiseState) -> None:
        """Render given game state."""


