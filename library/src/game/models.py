import enum
from game.validators import validate_network, validate_game_state
import networkx as nx
from ras.relalg import RA
import matplotlib.pyplot as plt
import numpy as np
import itertools as it
from dataclasses import dataclass
from functools import cached_property

class Character(str, enum.Enum):
    ABELARDE = "A"
    HELOISE = "H"

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
    adj : list[list[int]]
    
    def _post_init__(self) -> None:
        validate_network(self)

    def add(self, incoming : list[int]) -> "Network":
        nextadj = self.adj.copy()
        n = len(incoming)-1
        outgoing = [self.ra.converse[a] for a in incoming]
        nextadj.append(outgoing)
        for i in range(n):
            nextadj[i].append(incoming[i])
        return Network(self.ra, nextadj)
    
    def display(self):
        n = len(self.adj)
        plt.clf()
        G = nx.from_numpy_array(np.triu(np.matrix(self.adj)), parallel_edges=True, create_using=nx.MultiDiGraph)
        for node in G.nodes(): G.add_edge(node, node)
        edge_labels = {(u, v) : f'{self.ra.tochar[self.adj[u][v]]}' for u, v in G.edges()}
        pos = nx.circular_layout(G) if n != 2 else nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=700, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', label_pos=0.2)
        plt.show(block=False)

@dataclass(frozen=True)
class GameState:
    network : Network
    current_player : Character
    need : tuple[int, int, int, int] | int | None = None

    def __post_init__(self) -> None:
        validate_game_state(self)

    @cached_property
    def winner(self) -> Character | None:
        if len(self.possible_moves) == 0:
            return self.current_player.other

    @cached_property
    def possible_moves(self) -> list[Move]:
        if self.current_player is Character.ABELARDE:
            return self._possible_abelarde_moves
        return self._possible_heloise_moves

    @cached_property
    def _possible_abelarde_moves(self) -> list[Move]:
        moves = []
        if len(self.network.adj) == 0:
            for a in range(self.network.ra.num_atoms):
                moves.append(
                    Move(
                        character=Character.ABELARDE,
                        before_state = self,
                        after_state=GameState(self.network, self.current_player.other, a)
                    )
                )
        else:
            for x, y in it.product(range(len(self.network.adj)), repeat=2):
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
                                    after_state=GameState(self.network, self.current_player.other, (x, y, b, c))
                                )
                            )
        return moves
    
    @cached_property
    def _possible_heloise_moves(self) -> list[Move]:
        ra = self.network.ra
        if len(self.network.adj) == 0:
            if self.need < ra.num_units:
                return [
                    Move(
                        character=Character.HELOISE,
                        before_state=self,
                        after_state=GameState(self.network.add([self.need]), self.current_player.other)
                    )
                ]
            elif ra.num_units == 1:
                return [
                    Move(
                        character=Character.HELOISE,
                        before_state=self,
                        after_state=GameState(self.network.add([0]).add([self.need, 0]), self.current_player.other)
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
                                after_state=GameState(self.network.add([x]).add([self.need, y]))
                            )
                        )
                return moves
        else:
            raise NotImplementedError()









