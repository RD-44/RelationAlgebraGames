import pickle
import sys
from game.models import AbelardeState, Character,Network
from game.player import MiniMaxPlayer, RandomPlayer
import ras.relalg
sys.modules['relalg'] = ras.relalg
from game.engine import RepresentationGame
import unittest

class TestGame(unittest.TestCase):

    def test_need_first_round(self):
        for i in range(1, 5):
            with open(f"library/tests/test_ras/ra{i}.pickle","rb") as f:
                ra = pickle.load(f)
                game_state = AbelardeState(Network(ra))
                game_state = game_state.possible_moves[0].after_state
                self.assertTrue(isinstance(game_state.need, int))
    
    def test_need_second_round(self):
        for i in range(1, 5):
            with open(f"library/tests/test_ras/ra{i}.pickle","rb") as f:
                ra = pickle.load(f)
                game_state = AbelardeState(Network(ra))
                game_state = game_state.possible_moves[0].after_state.possible_moves[0].after_state.possible_moves[0].after_state
                self.assertTrue(isinstance(game_state.need, tuple) and len(game_state.need) == 4)
        
    def test_num_abalarde_moves_first_round(self):
        for i in range(1, 5):
            with open(f"library/tests/test_ras/ra{i}.pickle","rb") as f:
                ra = pickle.load(f)
                game_state = AbelardeState(Network(ra))
                self.assertTrue(len(game_state.possible_moves)==ra.num_atoms, msg=f'Failed on ra{i}')
            

class TestMiniMax(unittest.TestCase):

    def test_both_minimax(self):
        for i in range(1, 4):
            with open(f"library/tests/test_ras/ra{i}.pickle","rb") as f:
                ra = pickle.load(f)
                game_state = AbelardeState(Network(ra))
                p1, p2 = MiniMaxPlayer(Character.ABELARDE, delay_seconds=0), MiniMaxPlayer(Character.HELOISE, 0)
                winner = RepresentationGame(p1, p2, ra).play()
                self.assertTrue(winner is Character.HELOISE, msg=f'Failed on ra{i}')

    def test_minimax_random(self):
        for i in range(1, 4):
            with open(f"library/tests/test_ras/ra{i}.pickle","rb") as f:
                    ra = pickle.load(f)
                    game_state = AbelardeState(Network(ra))
                    p1, p2 = RandomPlayer(Character.ABELARDE, delay_seconds=0), MiniMaxPlayer(Character.HELOISE, 0)
                    winner = RepresentationGame(p1, p2, ra).play()
                    self.assertTrue(winner is Character.HELOISE, msg=f'Failed on ra{i}')


if __name__ == '__main__':
    unittest.main()



#  USE THIS AS BASIS FOR UNIT TESTS
# moves = game_state.possible_moves

# g2 = moves[0].after_state

# g2 = g2.possible_moves[0].after_state

# moves = g2.possible_moves

# h = moves[0].after_state

# print(len(h.possible_moves))
# for move in h.possible_moves:
#     print(move.after_state.network.adj)

