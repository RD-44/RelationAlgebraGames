import pickle
import sys
from game.models import Character, GameState, Network
import ras.relalg
sys.modules['relalg'] = ras.relalg

from game.engine import Game

with open("dumps/monk.pickle","rb") as f:
    ra = pickle.load(f)

game_state = GameState(network=Network(ra, [[0]]), current_player=Character.ABELARDE, need=None)


# USE THIS AS BASIS FOR UNIT TESTS
moves = game_state.possible_moves
for move in moves:
    print(move.after_state.need)
    
game = Game(ra)
winner = game.play()
print("Winner:", winner)