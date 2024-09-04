import pickle
import sys
from ras import random_ra
from repgame.models import Character
from repgame.player import MiniMaxPlayer, RandomPlayer
import ras.relalg
sys.modules['relalg'] = ras.relalg
from repgameconsole.players import ConsolePlayer
from repgameconsole.renderers import ConsoleRenderer
from repgame.engine import RepresentationGame

with open("library/tests/test_ras/ra2.pickle", "rb") as f:
    ra = pickle.load(f)

# FOR TESTING:
from pebblegame.models import Network

#  USE THIS AS BASIS FOR UNIT TESTS
# moves = game_state.possible_moves

# g2 = moves[0].after_state

# g2 = g2.possible_moves[0].after_state

# moves = g2.possible_moves

# h = moves[0].after_state

# print(len(h.possible_moves))
# for move in h.possible_moves:
#     print(move.after_state.network.adj)

p1, p2 = MiniMaxPlayer(Character.ABELARDE), MiniMaxPlayer(Character.HELOISE)
renderer = ConsoleRenderer()
winner = RepresentationGame(p1, p2, ra, renderer).play()

# test = Network(ra, 4)
# print(consistent(test))
# test.display(True)