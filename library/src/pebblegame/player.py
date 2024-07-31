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

from pebblegame.models import AbelardeState, Character, GameState, HeloiseState, Move
from pebblegame.player import Player

class ConsolePlayer(Player):
    def get_move(self, game_state: GameState) -> Move | None:
        # while not game_state.game_over:
        #     try:
        #         index = int(input(f"{self.character.value}'s move: "))
        #     except ValueError:
        #         print("Please enter an index corresponding to the move.")
        #     else:
        #         try:
        #             return game_state.possible_moves[index]
        #         except IndexError:
        #             print("Not a valid move.")
        # return None
        n = len(game_state.network.adj)
        if game_state.current_player is Character.ABELARDE:
            print(f"Nodes go from 0 to {n-1}")
            x = int(input("Enter node x: "))
            y = int(input("Enter node y: "))
            z = int(input("Enter node z (must not be same as x or y): "))
            print("Atoms:", game_state.network.ra.tochar)
            a = int(input("Enter atom a: "))
            b = int(input("Enter atom b: "))
            incoming = [-1 for _ in range(n)]
            incoming[x] = a
            incoming[y] = game_state.network.ra.converse[b]
            return Move(
                    character=Character.ABELARDE,
                    before_state=game_state,
                    after_state=HeloiseState(game_state.network.add(z, incoming), x, y, z)
                )
        else:
            col = []
            print("Atoms:", game_state.network.ra.tochar)
            for i in range(n):
                if i == game_state.z:
                    if game_state.network.ra.num_units > 1:
                        print(f"Units go from 0 to {game_state.network.ra.num_units}")
                        col.append(int(input(f"Unit labelling edge {i}->{game_state.z}: ")))
                    else:
                        col.append(0)
                else:
                    col.append(int(input(f"Atom labelling edge {i}->{game_state.z}: ")))
            a, b = game_state.network.adj[game_state.x][game_state.z], game_state.network.adj[game_state.z][game_state.y]
            next_network = game_state.network.add(game_state.z, col)
            return Move(
                    character=Character.HELOISE,
                    before_state=game_state,
                    after_state=AbelardeState(next_network, a == next_network.adj[game_state.x][game_state.z] and b == next_network.adj[game_state.z][game_state.y])
                )