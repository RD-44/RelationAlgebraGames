import abc
from game.models import AbelardeState, HeloiseState

class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def renderabelarde(self, game_state : AbelardeState) -> None:
        """Render given game state."""

    def renderheloise(self, game_state : HeloiseState) -> None:
        """Render given game state."""


