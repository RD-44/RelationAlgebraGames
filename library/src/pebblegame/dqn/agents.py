#TODO: Create Abelarde agent first and train against the minimax algorithm
# Once it's clear that the agent is evolving, do heloise.
from abc import ABC
import pickle
from pebblegame.dqn.aiengine import PebbleGameAI
from ras.relalg import RA
import sys
import ras
sys.modules['relalg'] = ras.relalg
import torch
import random
import numpy as np
from collections import deque
from pebblegame.models import AbelardeState, GameState, HeloiseState, Network
from pebblegame.dqn.model import Linear_QNet, QTrainer
from pebblegame.dqn.exceptions import UninitialisedAgent
from matplotlib import pyplot as plt

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class PostInitCaller(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.__post_init__()
        return obj

class Agent(metaclass=PostInitCaller):

    def __init__(self, ra : RA, n : int) -> None:
        self.ra = ra
        self.n = n
        self.n_games = 0 # number of games played
        self.epsilon = 0.4 # used to determine exploitation vs exploration
        self.gamma = 0.9 # discount factor
        self.memory = deque(maxlen=MAX_MEMORY)
        self.trainer = None # must be initialised in a subclass
    
    def __post_init__(self) -> None:
        if self.trainer is None:
            raise UninitialisedAgent("trainer is not initialised")

    def get_state(self, game : PebbleGameAI) -> np.ndarray:
        return np.ravel(game.game_state.network.adj) # flattens adjacency matrix to 1D array
        
    def remember(self, state, action, reward, next_state, done) -> None:
        self.memory.append((state, action, reward, next_state, done)) 
        # memory will auto popleft once MAX_MEMORY capacity is reached 

    def train_long_memory(self) -> None:
        mini_sample = self.memory if len(self.memory) <= BATCH_SIZE else random.sample(self.memory, BATCH_SIZE)
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(np.array(states), np.array(actions), np.array(rewards), np.array(next_states), np.array(dones))

    def train_short_memory(self, state, action, reward, next_state, done) -> None:
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def get_action(self, state, test=False) -> list[int]:
        final_move = np.zeros((self.num_moves,))
        self.epsilon = 0.1#1/(2 + 2*np.log(1+0.1*self.n_games))
        print(self.epsilon)
        if np.random.rand() < self.epsilon and not test:
            index = random.randint(0, self.num_moves-1)
            final_move[index] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

class AbelardeAgent(Agent):

    def __init__(self, ra : RA, n : int) -> None:
        super().__init__(ra, n)
        self.num_moves = n*((n-1)**2)*(ra.num_atoms**2)
        self.model = Linear_QNet(n*n, self.num_moves) 
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
class HeloiseAgent(Agent):

    def __init__(self, ra : RA, n : int) -> None:
        super().__init__(ra, n)
        self.model = Linear_QNet(n*n, ra.num_units*(ra.num_atoms**(n-1)))
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
        
def train(ra : RA, n : int):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    abelarde_agent = AbelardeAgent(ra, n)
    game = PebbleGameAI(ra, n)

    while True:
        # get old state 
        state_old = abelarde_agent.get_state(game)
        # get move based on current state
        action = abelarde_agent.get_action(state_old)
        # do the move and get new state
        reward, done, score = game.play_abelarde_step(action)
        state_new = abelarde_agent.get_state(game)
        abelarde_agent.train_short_memory(state_old, action, reward, state_new, done)
        abelarde_agent.remember(state_old, action, reward, state_new, done)

        if done:
            # experienced replay - train again on ALL previous moves to improve 
            game.reset()
            abelarde_agent.n_games += 1
            abelarde_agent.train_long_memory()

            if score > record:
                record = score
                # agent.model.save

            print('Game', abelarde_agent.n_games, 'Score', score, 'Record', record)

            plot_scores.append(score)
            total_score += score
            plot_mean_scores.append(total_score/abelarde_agent.n_games)

            if abelarde_agent.n_games % 10 == 0:
                abelarde_agent.model.save()

            plot(plot_scores, plot_mean_scores)

def plot(scores, mean_scores) -> None:
    plt.figure(2)
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    

if __name__ == '__main__':
    with open("library/tests/test_ras/ra4.pickle", "rb") as f:
        ra = pickle.load(f)
    train(ra, 4)