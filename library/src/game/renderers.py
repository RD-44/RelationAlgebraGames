import abc
from game.models import GameState

class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render(self, game_state : GameState) -> None:
        """Render given game state."""

