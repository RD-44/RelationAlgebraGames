import enum
from repgame.validators import validate_network, validate_heloise_state
import networkx as nx
from ras.relalg import RA
import matplotlib.pyplot as plt
import numpy as np
import itertools as it
from dataclasses import dataclass, field
from functools import cached_property
import abc 

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

@dataclass(frozen=True)
class Network:
    ra : RA
    adj : list[list[int]] = field(default_factory=lambda: [])
    
    def _post_init__(self) -> None:
        validate_network(self)

    def add(self, incoming : list[int]) -> "Network":
        nextadj = [row[:] for row in self.adj]
        outgoing = [self.ra.converse[a] for a in incoming]
        nextadj.append(outgoing)
        for i in range(len(incoming)-1):
            nextadj[i].append(incoming[i])
        return Network(self.ra, nextadj)
    
    def display(self, done=False):
        n = len(self.adj)
        plt.clf()
        G = nx.from_numpy_array(np.triu(np.matrix(self.adj)), parallel_edges=True, create_using=nx.MultiDiGraph)
        for node in G.nodes(): 
            if self.adj[node][node] == 0: G.add_edge(node, node)
        edge_labels = {(u, v) : f'{self.ra.tochar[self.adj[u][v]]}' for u, v in G.edges()}
        pos = nx.circular_layout(G) if n != 2 else nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=700, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', label_pos=0.2)
        if done : plt.show()
        else : plt.show(block=False)

def consistent(network : Network) -> bool:
    ra = network.ra
    if not network.adj[-1][-1] < ra.num_units : return False
    for i, j, k in it.product(range(len(network.adj)), repeat=3):
        a, b, c = network.adj[i][j], network.adj[j][k], network.adj[i][k]
        if c not in ra.table[a][b] : return False
    return True

@dataclass(frozen=True)
class GameState(metaclass=abc.ABCMeta):
    network : Network

    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None

    @cached_property
    def winner(self) -> Character | None:
        if len(self.possible_moves) == 0:
            return self.current_player.other

    @abc.abstractmethod
    def possible_moves(self) -> list[Move]:
        """Return possible moves"""

    @abc.abstractmethod 
    def current_player(self) -> Character:
        """Return current player"""

@dataclass(frozen=True)
class HeloiseState(GameState):
    need : tuple[int, int, int, int] | int 

    def __post_init__(self) -> None:
        validate_heloise_state(self)

    @cached_property
    def current_player(self) -> Character:
        return Character.HELOISE

    @cached_property
    def possible_moves(self) -> list[Move]:
        if len(self.network.adj) == 0: return self._first_round_moves
        ra = self.network.ra
        n = len(self.network.adj) + 1
        moves = []
        x, y, a, b = self.need     
        permutations = it.product(range(ra.num_atoms), repeat=n-2 if x != y else n-1) 
        for perm in permutations:
            incoming = list(perm)
            incoming.append(a)
            incoming[x], incoming[-1] = incoming[-1], incoming[x]
            if x != y:
                incoming.append(ra.converse[b])
                incoming[y], incoming[-1] = incoming[-1], incoming[y]
            potential_move = self.network.add(incoming)
            if consistent(potential_move):
                moves.append(
                    Move(
                        character=Character.HELOISE,
                        before_state=self,
                        after_state=AbelardeState(potential_move)
                    )
                )
        return moves

    @cached_property
    def _first_round_moves(self) -> list[Move]:
        ra = self.network.ra
        if self.need < ra.num_units:
            return [
                Move(
                    character=Character.HELOISE,
                    before_state=self,
                    after_state=AbelardeState(self.network.add([self.need]))
                )
            ]
        elif ra.num_units == 1:
            return [
                Move(
                    character=Character.HELOISE,
                    before_state=self,
                    after_state=AbelardeState(self.network.add([0]).add([self.need, 0]))
                )
            ]
        else:
            moves = []
            allowed_units_lr = ra.table[self.need][ra.converse[self.need]] & set(range(ra.num_units))
            allowed_units_rl = ra.table[ra.converse[self.need]][self.need] & set(range(ra.num_units))
            for x in allowed_units_lr:
                for y in allowed_units_rl:
                    moves.append(
                        Move(
                            character=Character.HELOISE,
                            before_state=self,
                            after_state=AbelardeState(self.network.add([x]).add([self.need, y]))
                        )
                    )
            return moves

@dataclass(frozen=True)       
class AbelardeState(GameState):

    def _post_init__(self) -> None:
        pass

    @cached_property
    def current_player(self) -> Character:
        return Character.ABELARDE

    @cached_property
    def possible_moves(self) -> list[Move]:
        if len(self.network.adj) == 0: return self._first_round_moves
        moves = []
        for x, y in it.product(range(len(self.network.adj)), repeat=2):
            if x > y : continue
            a = self.network.adj[x][y]
            for b, c in it.product(range(self.network.ra.num_atoms), repeat=2):
                if a in self.network.ra.table[b][c]: # if a <= b;c
                    for z in range(len(self.network.adj[x])):
                        # this means such a labelling exists, so not a valid move for abalarde
                        if self.network.adj[x][z] == b and self.network.adj[z][y] == c: break # 
                    else:
                        moves.append(
                            Move(
                                character = Character.ABELARDE,
                                before_state=self,
                                after_state=HeloiseState(self.network, (x, y, b, c))
                            )
                        )
        return moves

    @cached_property
    def _first_round_moves(self) -> list[Move]:
        return [
            Move(
                character=Character.ABELARDE,
                before_state = self,
                after_state=HeloiseState(self.network, atom)
            )
            for atom in range(self.network.ra.num_atoms)
        ]








