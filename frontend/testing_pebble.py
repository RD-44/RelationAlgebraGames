import pickle
import sys
from pebblegame.models import Character
from pebblegame.player import DQNPlayer, MiniMaxPlayer, RandomPlayer
import ras.relalg
sys.modules['relalg'] = ras.relalg
from pebblegameconsole.players import ConsolePlayer
from pebblegameconsole.renderers import ConsoleRenderer
from pebblegame.engine import PebbleGame
import math

with open("library/tests/test_ras/ra4.pickle", "rb") as f:
    ra = pickle.load(f)

p1, p2 = DQNPlayer(Character.ABELARDE, ra, 5), ConsolePlayer(Character.HELOISE)
renderer = ConsoleRenderer()
winner = PebbleGame(p1, p2, ra, 5, renderer).play()

