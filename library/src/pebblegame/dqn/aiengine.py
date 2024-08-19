import time
from turtle import delay
from pebblegame.exceptions import InvalidPlayer
from pebblegame.models import AbelardeState, Network, Character
from ras.relalg import RA
from pebblegame.player import MiniMaxPlayer
import numpy as np

class PebbleGameAI:

    def __init__(self, ra : RA, n : int) -> None:
        self.ra = ra
        self.n = n
        self.rounds = 0
        self.game_state = AbelardeState(Network(ra, n))
        self.num_games = 1
        self.last_action = -1 
    
    def reset(self) -> None:
        self.game_state = AbelardeState(Network(self.ra, self.n))
        self.rounds = 0
        self.num_games += 1

    def play_abelarde_step(self, action) -> tuple[int, int]:
        self.game_state.network.display()
        self.rounds += 1
        if not self.game_state.current_player is Character.ABELARDE :
            raise InvalidPlayer("Player is not Abelarde.")
        #time.sleep(1)
        if action == self.last_action: # discourage playing the same move played in the last round
            return -5, True
            # variance of last n moves
        self.last_action = action
        
        self.game_state = self.game_state.possible_moves[action].after_state
        reward = 0
        if self.game_state.done:
            # if game is over after abelarde's turn, he loses due to invalid move
            reward = -10
        return reward, self.game_state.done
    
    def play_abelarde_single(self, action) -> tuple[int, int]:
        self.game_state.network.display()
        self.rounds += 1
        if not self.game_state.current_player is Character.ABELARDE :
            raise InvalidPlayer("Player is not Abelarde.")
        self.game_state.network.display()
        # if move_number == self.last_move_number: # discourage playing the same move played in the last round
        #     return -5, True
        self.last_action = action
        
        self.game_state = self.game_state.possible_moves[action].after_state
        reward = 0
        if self.game_state.done:
            # if game is over after abelarde's turn, he loses due to invalid move
            reward = -100
        else:
            #print(f"Abelarde picked {(self.game_state.x, self.game_state.y, self.game_state.z, self.game_state.network.adj[self.game_state.x][self.game_state.z], self.game_state.network.adj[self.game_state.z][self.game_state.y])}")
            self.game_state = MiniMaxPlayer(Character.HELOISE).get_move(self.game_state).after_state
            self.game_state.network.display()
            if self.game_state.done: # here abelarde wins
                print("A won.")
                reward = 3
            else:
                reward = -self.rounds
        return reward, self.game_state.done
        
        
    def play_heloise_step(self, action) -> tuple[int, int, int]:
        self.game_state.network.display()
        if self.game_state.current_player is not Character.HELOISE :
            raise InvalidPlayer("Player is not Heloise.")
        self.game_state = self.game_state.possible_moves[action].after_state
        reward = 0
        if self.game_state.done: # game ends after heloise moves only if she plays wrong move
            reward = -10
        else:
            reward = 5
        return reward, self.game_state.done

