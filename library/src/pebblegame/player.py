import abc
import time
import random
from typing import TYPE_CHECKING
import numpy as np
from pebblegame.models import GameState, Move, Character
from ras.relalg import RA
from pebblegame.exceptions import InvalidMove
    


class Player(metaclass=abc.ABCMeta):
    def __init__(self, character: Character) -> None:
        self.character = character

    def make_move(self, game_state: GameState) -> GameState:
        if move := self.get_move(game_state):
            return move.after_state
        raise InvalidMove("No more possible moves")

    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state. """


class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, character: Character, delay_seconds: float = 0.25) -> None:
        super().__init__(character)
        self.delay_seconds = delay_seconds

    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Return computer's move"""


class RandomPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        try:
            return random.choice(game_state.possible_moves)
        except IndexError:
            return None


class MiniMaxPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        from pebblegame.minimax import find_best_move
        return find_best_move(game_state)

class DQNPlayer(ComputerPlayer):
    """Player that learns using deep q learning
    may need to reward differently based on player
    consider having a reward attribute"""
    
    def __init__(self, character: Character, ra : RA, n : int, delay_seconds: float = 0.25) -> None:
        from pebblegame.dqn.agents import AbelardeAgent
        super().__init__(character, delay_seconds)
        self.agent = AbelardeAgent(ra, n)

    def get_computer_move(self, game_state: GameState) -> Move | None:
        return game_state.possible_moves[np.argmax(self.agent.get_action(np.ravel(game_state.network.adj), True))]
