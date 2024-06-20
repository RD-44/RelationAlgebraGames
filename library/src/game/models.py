import enum
import networkx as nx
from ras.relalg import RA
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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

class Network:
    def __init__(self, ra : RA, adj=[]) -> None:
        self.adj = adj
        self.ra = ra

    def add(self, incoming : list[int]):
        n = len(incoming)-1
        outgoing = [self.ra.converse[a] for a in incoming]
        self.adj.append(outgoing)
        for i in range(n):
            self.adj[i].append(incoming[i])
    
    def __str__(self):
        df = pd.DataFrame(self.adj)
        df.replace(to_replace=self.ra.tochar, inplace=True)
        return str(df)
    
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
    need : tuple[int, int, int, int] | None 

    @cached_property
    def winner(self) -> Character | None:
        if len(self.possible_moves) == 0:
            return self.current_player.other

    @cached_property
    def possible_moves(self) -> list[Move]:
        moves = []
        if self.current_player is Character.ABELARDE:
            for x in range(len(self.network.adj)):
                for y in range(len(self.network.adj)):
                    a = self.network.adj[x][y]
                    for b in range(self.network.ra.num_atoms):
                        for c in range(self.network.ra.num_atoms):
                            if a in self.network.ra.table[b][c]: # if a <= b;c
                                valid = True
                                for z in range(len(self.network.adj[x])):
                                    if self.network.adj[x][z] == b and self.network.adj[z][y] == c:
                                        valid = False # this means such a labelling exists, so not a valid move for abalarde
                                        break
                                if valid : moves.append(
                                    Move(
                                        character = Character.ABELARDE,
                                        before_state=self,
                                        after_state=GameState(self.network, self.current_player, (x, y, b, c))
                                    )
                                )
            return moves
        else:
            pass







