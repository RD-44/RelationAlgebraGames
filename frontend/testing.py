import pickle
import sys
from game.models import Character
from game.player import MiniMaxPlayer, RandomPlayer
import ras.relalg

from console.players import ConsolePlayer
from console.renderers import ConsoleRenderer

sys.modules['relalg'] = ras.relalg

from game.engine import RepresentationGame

with open("dumps/mckenzie.pickle", "rb") as f:
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

p1, p2 = MiniMaxPlayer(Character.ABELARDE), RandomPlayer(Character.HELOISE)
renderer = ConsoleRenderer()
winner = RepresentationGame(p1, p2, ra, renderer).play()
