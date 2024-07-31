import pickle
from re import L
import sys
from tkinter import N
from pebblegame.models import AbelardeState, HeloiseState, Character,Network
from pebblegame.pims import construct_networks
from pebblegame.player import MiniMaxPlayer, RandomPlayer
import ras.relalg
sys.modules['relalg'] = ras.relalg
from pebblegame.engine import PebbleGame
import unittest


class TestGame(unittest.TestCase):

    #TODO: implement creation and deletion methods

    def test_num_abelarde_moves(self):
        for i in range(1, 5):
            with open(f"library/tests/test_ras/ra{i}.pickle","rb") as f:
                ra = pickle.load(f)
                game_state = AbelardeState(Network(ra, 4))
                m, n = len(game_state.network.adj), ra.num_atoms
                self.assertEqual(len(game_state.possible_moves),m*((m-1)**2)*(n**2))

    def test_num_heloise_moves(self):
        for i in range(1, 5):
            with open(f"library/tests/test_ras/ra{i}.pickle","rb") as f:
                ra = pickle.load(f)
                for j in range(2, 4):
                    game_state = AbelardeState(Network(ra, j)).possible_moves[0].after_state
                    k, m, n = ra.num_units, len(game_state.network.adj), ra.num_atoms
                    self.assertEqual(len(game_state.possible_moves),k*(n**(m-1)))

    def test_heloise_self_loop(self):
        for i in range(1, 5):
            with open(f"library/tests/test_ras/ra{i}.pickle","rb") as f:
                ra = pickle.load(f)
                game_state = AbelardeState(Network(ra, 4)).possible_moves[0].after_state
                for move in game_state.possible_moves:
                    after = move.after_state
                    self.assertTrue(after.network.adj[game_state.z][game_state.z] < ra.num_units)

    def test_abelarde_edge_labelling(self):
        for i in range(1, 5):
            with open(f"library/tests/test_ras/ra{i}.pickle","rb") as f:
                ra = pickle.load(f)
                game_state = AbelardeState(Network(ra, 4)).possible_moves[0].after_state
                adj = game_state.network.adj
                for j in range(len(adj)):
                    if j != game_state.x and j != game_state.y:
                        self.assertEqual(adj[j][game_state.z], -1)
                        self.assertEqual(adj[game_state.z][j], -1)
                    else:
                        self.assertNotEqual(adj[j][game_state.z], -1)
                        self.assertNotEqual(adj[game_state.z][j], -1)
    
    def test_construct_networks(self):
        for i in range(1, 5):
            with open(f"library/tests/test_ras/ra{i}.pickle","rb") as f:
                ra = pickle.load(f)
            for j in range(2, 4):
                networks = construct_networks(ra, j)
                self.assertEqual((ra.num_atoms)**((j*(j+1))//2), len(networks))
                



                

    

    
    
