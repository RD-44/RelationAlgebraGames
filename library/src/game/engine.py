from game.exceptions import InvalidMove
from game.player import Player
from ras.relalg import RA
from game.models import Character, GameState, Network, AbelardeState
from dataclasses import dataclass
from game.renderers import Renderer

@dataclass(frozen=True)
class RepresentationGame:

    player1 : Player
    player2 : Player
    renderer : Renderer
    ra : RA
    
    def __post_init__(self):
        pass

    def play(self) -> None:
        game_state = AbelardeState(Network(self.ra))
        print("Game has begun on the following relation algebra: \n", self.ra)
        while True: 
            self.renderer.renderAbelarde(game_state)
            if game_state.game_over: break
            game_state = self.player1.make_move(game_state)
            self.renderer.renderHeloise(game_state)
            if game_state.game_over: break
            game_state = self.player2.make_move(game_state)


    def get_current_player(self, game_state : GameState):
        if game_state.current_player is Character.ABELARDE:
            return self.player1
        return self.player2