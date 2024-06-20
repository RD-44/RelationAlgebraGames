import pickle
import sys
from game.models import Character, GameState, Network
import ras.relalg
sys.modules['relalg'] = ras.relalg

from game.engine import Game

with open("dumps/monk.pickle","rb") as f:
    ra = pickle.load(f)

game_state = GameState(network=Network(ra, []), current_player=Character.ABELARDE)



# USE THIS AS BASIS FOR UNIT TESTS
moves = game_state.possible_moves
for move in moves:
    print(move.after_state.need)

g2 = moves[0].after_state

g2 = g2.possible_moves[0].after_state

moves = g2.possible_moves

for move in moves:
    print(move.after_state.possible_moves)

winner = Game(ra).play()
