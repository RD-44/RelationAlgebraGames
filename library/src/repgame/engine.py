from repgame.player import Player
from ras.relalg import RA
from repgame.models import Network, AbelardeState
from dataclasses import dataclass
from repgame.renderers import Renderer
from repgame.validators import validate_game

@dataclass(frozen=True)
class RepresentationGame:

    player1 : Player
    player2 : Player
    ra : RA
    renderer : Renderer | None = None
    
    def __post_init__(self):
        validate_game(self)

    def play(self) -> None:
        game_state = AbelardeState(Network(self.ra))
        if self.renderer is not None : print("Game has begun on the following relation algebra: \n", self.ra, "\n ------------------\n")
        round = 0
        while True: 
            if self.renderer is not None : self.renderer.renderabelarde(game_state)
            if game_state.game_over: break
            game_state = self.player1.make_move(game_state)
            if self.renderer is not None : self.renderer.renderheloise(game_state)
            if game_state.game_over: break
            game_state = self.player2.make_move(game_state)
            round += 1
        
        print(round)
            
        return game_state.winner