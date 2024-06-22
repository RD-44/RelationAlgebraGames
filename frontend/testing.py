import pickle
import sys
from game.models import Character, GameState, Network
import ras.relalg
sys.modules['relalg'] = ras.relalg

from game.engine import RepresentationGame

with open("dumps/ra5.pickle","rb") as f:
    ra = pickle.load(f)

#  USE THIS AS BASIS FOR UNIT TESTS
# moves = game_state.possible_moves

# g2 = moves[0].after_state

# g2 = g2.possible_moves[0].after_state

# moves = g2.possible_moves

# h = moves[0].after_state

# print(len(h.possible_moves))
# for move in h.possible_moves:
#     print(move.after_state.network.adj)

winner = RepresentationGame(ra).play()
