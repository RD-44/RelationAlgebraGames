from pebblegame.dqn.aiengine import PebbleGameAI
from ras.relalg import RA
import torch
import random
import numpy as np
from collections import deque
from pebblegame.dqn.model import DQN, DoubleQTrainer, QTrainer
from pebblegame.dqn.exceptions import UninitialisedAgent

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class PostInitCaller(type):
    # used to ensure that postinit is called in the Agent class
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.__post_init__()
        return obj

class Agent(metaclass=PostInitCaller):

    def __init__(self, ra : RA, n : int) -> None:
        self.ra = ra
        self.n = n
        self.epsilon = 0.5 # determines exploitation vs exploration
        self.gamma = 0.9 # discount factor
        self.memory = deque(maxlen=MAX_MEMORY) # replay buffer
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
        self.trainer.train_step(np.array([state]), np.array([action]), np.array([reward]), np.array([next_state]), np.array([done]))
    
    def get_action(self, state, test=False) -> int:
        self.epsilon = 1/(2 + 2*np.log(1+0.1*len(self.memory)))
        if np.random.rand() < self.epsilon and not test:
            return random.randint(0, self.num_moves-1)
        prediction = self.model(torch.tensor(state, dtype=torch.float))
        return torch.argmax(prediction).item()

class AbelardeAgent(Agent):

    def __init__(self, ra : RA, n : int, name : str) -> None:
        super().__init__(ra, n)
        self.num_moves = n*((n-1)**2)*(ra.num_atoms**2)
        # self.trainer = QTrainer(model=self.model, lr=LR, gamma=self.gamma)
        self.model = DQN(input_size=n*n, output_size=self.num_moves, name=name) 
        self.target_model = DQN(input_size=n*n, output_size=self.num_moves, name=name+'_target')
        for target_param, param in zip(self.model.parameters(), self.target_model.parameters()):
            target_param.data.copy_(param)
        self.trainer = DoubleQTrainer(model=self.model, target_model=self.target_model, lr=LR, gamma=self.gamma)
    
    def get_action(self, state, test=False) -> int:
        self.epsilon = 1/(2 + 2*np.log(1+0.1*len(self.memory)))
        if np.random.rand() < self.epsilon and not test:
            return random.randint(0, self.num_moves-1)
        prediction = self.target_model(torch.tensor(state, dtype=torch.float))
        return torch.argmax(prediction).item()

    def save(self) -> None:
        self.model.save()
        self.target_model.save()

    
class HeloiseAgent(Agent):

    def __init__(self, ra : RA, n : int, name : str) -> None:
        super().__init__(ra, n)
        self.num_moves = ra.num_units*(ra.num_atoms**(n-1))
        self.model = DQN(input_size=n*n, output_size=self.num_moves, name=name)
        self.trainer = QTrainer(model=self.model, lr=LR, gamma=self.gamma)
    
