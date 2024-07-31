import time
from turtle import delay
from pebblegame.exceptions import InvalidPlayer
from pebblegame.models import AbelardeState, Network, Character
from ras.relalg import RA
from pebblegame.player import MiniMaxPlayer
import numpy as np

from pebblegame.player import ConsolePlayer

class PebbleGameAI:

    def __init__(self, ra : RA, n : int) -> None:
        self.ra = ra
        self.n = n
        self.rounds = 0
        self.game_state = AbelardeState(Network(ra, n))
        print(self.game_state.current_player)
        self.heloise_player = MiniMaxPlayer(Character.HELOISE, delay_seconds=0)
        self.last_move_number = -1 
    
    def reset(self) -> None:
        self.game_state = AbelardeState(Network(self.ra, self.n))
        self.rounds = 0

    def play_abelarde_step(self, action) -> tuple[int, int, int]:
        self.game_state.network.display()
        self.rounds += 1
        if not self.game_state.current_player is Character.ABELARDE :
            raise InvalidPlayer("Player is not Abelarde.")
        self.game_state.network.display()
        #time.sleep(1)
        move_number = np.argmax(action)
        if move_number == self.last_move_number: # discourage playing the same move played in the last round
            return -50, True, self.rounds
        self.last_move_number = move_number
        
        self.game_state = self.game_state.possible_moves[move_number].after_state
        reward = 0
        if self.game_state.game_over:
            # if game is over after abelarde's turn, he loses due to invalid move
            reward = -50
        else:
            #print(f"Abelarde picked {(self.game_state.x, self.game_state.y, self.game_state.z, self.game_state.network.adj[self.game_state.x][self.game_state.z], self.game_state.network.adj[self.game_state.z][self.game_state.y])}")
            self.game_state.network.display()
            self.game_state = self.heloise_player.get_move(self.game_state).after_state
            self.game_state.network.display()
            #time.sleep(1)
            if self.game_state.game_over: # here abelarde wins
                print("A won.")
                reward = 30
            else:
                reward = -20
        return reward, self.game_state.game_over, self.rounds
        
        
    # def play_heloise_step(self, action) -> tuple[int, int, int]:
    #     if self.game_state.current_player is not Character.ABELARDE :
    #         raise InvalidPlayer("Player is not Abelarde.")
    #     self.game_state = self.game_state.possible_moves[np.argmax(action)].after_state
    #     reward = 0
    #     if self.game_state.game_over:
    #         if self.game_state.winner is Character.HELOISE:
    #             reward = 10
    #         else:
    #             reward = -10
    #     else:
    #         reward = 5
    #     return reward, self.game_state.game_over, self.rounds

