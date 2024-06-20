import abc
import time
import random

from game.models import GameState

class AbelardePlayer(metaclass=abc.ABCMeta):

    def make_move(self, game_state: GameState) -> GameState:
        if self.mark is game_state.current_mark:
            if move := self.get_move(game_state): # getting the move is delegated to an abstract method - template method pattern
                return move.after_state
            raise InvalidMove("No more possible moves")
        else:
            raise InvalidMove("It is the other player's turn.")
    
    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state. """

class HeloisePlayer(metaclass=abc.ABCMeta):

    def make_move(self, game_state : GameState) -> GameState:
        pass


