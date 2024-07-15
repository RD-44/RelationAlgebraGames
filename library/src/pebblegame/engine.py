from pebblegame.player import Player
from ras.relalg import RA
from pebblegame.models import Network, AbelardeState
from dataclasses import dataclass
from pebblegame.renderers import Renderer
from pebblegame.validators import validate_game

@dataclass(frozen=True)
class PebbleGame:

    player1 : Player
    player2 : Player
    ra : RA
    n : int # number of nodes in network
    renderer : Renderer | None = None
    
    def __post_init__(self):
        validate_game(self)

    def play(self) -> None:
        game_state = AbelardeState(Network(self.ra))
        if self.renderer is not None : print("Game has begun on the following relation algebra: \n", self.ra, "\n ------------------\n")
        while True: 
            if self.renderer is not None : self.renderer.renderabelarde(game_state)
            if game_state.game_over: break
            game_state = self.player1.make_move(game_state)
            if self.renderer is not None : self.renderer.renderheloise(game_state)
            if game_state.game_over: break
            game_state = self.player2.make_move(game_state)
        return game_state.winner