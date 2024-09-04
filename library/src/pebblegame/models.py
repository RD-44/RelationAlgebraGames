import enum
import networkx as nx
from ras.relalg import RA
import matplotlib.pyplot as plt
import numpy as np
import itertools as it
from dataclasses import dataclass
from functools import cached_property
from pebblegame.exceptions import InvalidNetwork
import abc 


""" TODO: have a map from (n, ra) to the set of actions.
would need to define hashes for the ra class."""
# stores set of actions for a given network size, for both abelarde and heloise
abelardeCache = {}
heloiseCache = {}

class Character(str, enum.Enum):
    ABELARDE = "Abelarde"
    HELOISE = "Heloise"

    @property
    def other(self) -> "Character":
        return Character.ABELARDE if self is Character.HELOISE else Character.HELOISE
    
@dataclass(frozen=True)
class Move:
    character : Character
    before_state: "GameState"
    after_state: "GameState"

class Network:
    
    def __init__(self, ra : RA, n : int, adj=None) -> None:
        self.ra = ra
        self.adj = np.zeros((n, n), dtype=int) if adj is None else adj

    def add(self, node : int, incoming : list[int]) -> "Network":
        if len(incoming) != (n:=len(self.adj)): 
            raise InvalidNetwork("Length of incoming list is not", n)
        nextadj = np.array(self.adj)
        for i in range(n):
            nextadj[i][node] = incoming[i]
            nextadj[node][i] = self.ra.converse[incoming[i]] if incoming[i] >= 0 else -1
        return Network(self.ra, n, nextadj)
    
    @cached_property
    def consistent(self) -> bool:
        for i in range(len(self.adj)):
            if self.adj[i][i] >= self.ra.num_units : return False
        for i, j, k in it.product(range(len(self.adj)), repeat=3):
            a, b, c = self.adj[i][j], self.adj[j][k], self.adj[i][k]
            if a == -1 or b == -1 or c == -1 : continue
            if c not in self.ra.table[a][b] : return False
        return True
    
    def display(self, done=False):
        plt.figure(1)
        n = len(self.adj)
        plt.clf()
        G = nx.from_numpy_array(self.adj, create_using=nx.MultiDiGraph)
        for i, j in it.product(G.nodes(), repeat=2): 
            if self.adj[i][j] == 0: G.add_edge(i, j)
        edge_labels_nonsymmetric = {(u, v) : f'{self.ra.tochar[self.adj[u][v]]}' for u, v in G.edges() if self.adj[u][v] != -1 and self.ra.converse[self.adj[u][v]] != self.adj[u][v]}
        edge_labels_symmetric = {(u, v) : f'{self.ra.tochar[self.adj[u][v]]}' for u, v in G.edges() if self.adj[u][v] != -1 and self.ra.converse[self.adj[u][v]] == self.adj[u][v] and u >= v}
        # circular layout does not display identity atoms for n = 2, this is a workaround
        pos = nx.circular_layout(G) if n != 2 else nx.spring_layout(G) 
        nx.draw(G, pos, with_labels=True, node_size=700, font_weight='bold')
        # label symmetric atoms only once on an edge
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_nonsymmetric, font_color='black', label_pos=0.8)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_symmetric, font_color='black')
        plt.draw()
        plt.pause(0.01)
        if done: plt.show(block=True)


@dataclass(frozen=True)
class GameState(metaclass=abc.ABCMeta):
    network : Network

    @abc.abstractmethod
    def possible_moves(self) -> list[Move]:
        """Return possible moves"""

    @abc.abstractmethod
    def current_player(self) -> Character:
        """Return current player"""
    
    @cached_property
    def done(self) -> int:
        return 1 if self.winner is not None else 0

    @cached_property
    def winner(self) -> Character | None:
        if not self.legal_moves:
            return self.current_player.other
        return None

    @cached_property
    def legal_moves(self) -> list[Move]:
        moves = []
        for move in self.possible_moves:
            if not move.after_state.done:
                moves.append(move)
        return moves

@dataclass(frozen=True)
class AbelardeState(GameState):

    valid : bool = True

    def _post_init__(self) -> None:
        pass
    
    @cached_property
    def winner(self) -> Character | None:
        if not self.network.consistent or not self.valid:
            return self.current_player

    @cached_property
    def current_player(self) -> Character:
        return Character.ABELARDE

    @cached_property
    def possible_moves(self) -> list[Move]:
        n = len(self.network.adj)
        moves = []
        if n not in abelardeCache:
            abelardeCache[n] = []
            for x, y, z in it.product(range(n), repeat=3):
                if y == z or x == z : continue
                for a, b in it.product(range(self.network.ra.num_atoms), repeat=2):
                    abelardeCache[n].append((x, y, z, a, b))

        for x, y, z, a, b in abelardeCache[n]:
            incoming = [-1 for _ in range(n)]
            incoming[x] = a
            incoming[y] = self.network.ra.converse[b]
            moves.append(
                Move(
                    character=Character.ABELARDE,
                    before_state=self,
                    after_state=HeloiseState(self.network.add(z, incoming), x, y, z)
                )
            )
        return moves

@dataclass(frozen=True)
class HeloiseState(GameState):
    
    x : int
    y : int
    z : int

    @cached_property
    def winner(self) -> Character | None:
        if not self.network.consistent:
            return self.current_player
    
    @cached_property
    def current_player(self) -> Character:
        return Character.HELOISE

    @cached_property
    def done(self) -> bool:
        return self.winner is not None

    @cached_property
    def possible_moves(self) -> list[Move]:
        n = len(self.network.adj)
        moves = []
        if n not in heloiseCache:
            permutations = it.product(range(self.network.ra.num_atoms), repeat = n-1)
            heloiseCache[n] = []
            for perm in permutations:
                for i in range(self.network.ra.num_units):
                    arr = list(perm)
                    arr.append(i)
                    heloiseCache[n].append(arr)
        
        a, b = self.network.adj[self.x][self.z], self.network.adj[self.z][self.y]
        for incoming in heloiseCache[n]:
            col = incoming.copy()
            col[-1], col[self.z] = col[self.z], col[-1] # bring identity atom to the label connecting z to itself
            next_network = self.network.add(self.z, col)
            moves.append(
                Move(
                    character=Character.HELOISE,
                    before_state=self,
                    after_state=AbelardeState(next_network, a == next_network.adj[self.x][self.z] and b == next_network.adj[self.z][self.y])
                )
            )
        return moves





