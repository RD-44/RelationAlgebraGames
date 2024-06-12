from relalg import RA
from randRA import nextRA
import pickle
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
    
class Network:
    def __init__(self, ra : RA) -> None:
        self.adj = []
        self.ra = ra

    def add(self, incoming : list[int]):
        outgoing = [self.ra.converse[a] for a in incoming]
        self.adj.append(outgoing)
        for i in range(len(incoming)-1):
            self.adj[i].append(incoming[i])
    
    def __str__(self):
        df = pd.DataFrame(self.adj)
        df.replace(to_replace=self.ra.tochar, inplace=True)
        return str(df)
    
    def print(self):
        n = len(self.adj)
        plt.clf()
        G = nx.from_numpy_array(np.matrix(self.adj), parallel_edges=True, create_using=nx.MultiDiGraph)
        for node in G.nodes(): G.add_edge(node, node)
        edges = {(u, v) : f'{self.ra.tochar[self.adj[u][v]]}' for u, v in G.edges()}
        # Draw the graph with node labels and edge weights
        pos = nx.spring_layout(G)  # Position nodes using spring layout
        nx.draw(G, pos, with_labels=True, node_size=700, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edges, font_color='black')
        for node in G.nodes():
            x, y = pos[node]
            plt.text(x, y + 0.1, f'{self.ra.tochar[self.adj[node][node]]}', fontsize=8, ha='center', va='center')
        plt.show(block=False)

class Game:
    def __init__(self, ra : RA) -> None:
        self.turn = True
        self.ra = ra
        self.network = Network(ra)
    
    def _output_atoms(self, atoms=None): # prints out atoms and numbers corresponding to them
        if atoms is None:
            for i in range(self.ra.num_atoms):
                print(f'{i} : {self.ra.tochar[i]}')
        else:
            atoms = sorted(list(atoms))
            for i in range(len(atoms)):
                x = atoms[i]
                print(f'{x} : {self.ra.tochar[x]}')

    def _output_units(self):
        for i in range(self.ra.num_units):
            print(f'{i} : {self.ra.tochar[i]}')
    
    def _output_pairs(self, pairs):
        for i in range(len(pairs)):
            print(f'{i} : ({self.ra.tochar[pairs[i][0]]}, {self.ra.tochar[pairs[i][1]]})')
    
    def start(self):
        print("Game has begun on the following relation algebra: ")
        print(self.ra, '\n')
        print("Atoms: ")
        self._output_atoms()
        c = int(input("Abalarde, choose an atom: "))

        if c < self.ra.num_units:
            print("\nHeloise moves (forced)")
            self.network.add([c])
        else:
            if self.ra.num_units == 1:
                print("Heloise moves (forced)")
                self.network.add([0])
                self.network.add([c, 0])
            else:
                x = int(input(f"Enter a unit to label edge (0, 0): "))
                self.network.add([x])
                x = int(input(f"Enter a unit to label edge (1, 1): "))
                self.network.add([c, x])
        self.network.print()

        rounds = 1

        while True: 
            # Abalarde's turn
            print(f"ROUND {rounds}")
            x = int(input("Abalarde, pick node x: "))
            y = int(input("Abalarde, pick node y: "))
            c = self.network.adj[x][y]
            print(f'\nN({x}, {y}) = {self.ra.tochar[c]}')
            pairs = []
            for i in range(self.ra.num_atoms):
                for j in range(self.ra.num_atoms):
                    if c in self.ra.table[i][j]:
                        valid = True
                        for z in range(len(self.network.adj[x])):
                            if self.network.adj[x][z] == i and self.network.adj[z][y] == j:
                                valid = False
                        if valid : pairs.append((i, j))

            i = 0
            if len(pairs) == 0:
                print("Abalarde cannot make any good moves using nodes x and y. Next round.")
                continue
            elif len(pairs) == 1:
                print("Only one move is possible here: ")
                self._output_pairs(pairs)
                print('\n')
            else:
                print(f"Possible pairs (a', b') such that a';b' >= {self.ra.tochar[c]}:")
                self._output_pairs(pairs)
                i = int(input(f"Abalarde, pick a pair: "))

            # Heloise's turn
            a, b = pairs[i]
            incoming = [-1 for _ in range(len(self.network.adj) + 1)]
            incoming[x] = a
            incoming[y] = self.ra.converse[b]
            incoming[-1] = int(input("Heloise, pick a unit: ")) if self.ra.num_units > 1 else 0

            for i in range(len(incoming)):
                if incoming[i] != -1: continue
                print(f"\n Labelling edge: ({i}, {len(self.network.adj)})")
                allowed = set()
                started = False
                for j in range(len(self.network.adj)):
                    if j != i and incoming[j]!=-1:
                        if started:
                            allowed &= self.ra.table[self.network.adj[i][j]][incoming[j]]
                        else:
                            allowed = self.ra.table[self.network.adj[i][j]][incoming[j]]
                            started = True
                for k in range(self.ra.num_units):
                    if k in allowed : allowed.remove(k)

                print("Allowed atoms:")
                self._output_atoms(allowed)
                if len(allowed) == 0:
                    print("Heloise cannot label this edge with a valid atom. Abalarde wins.")
                    return
                if len(allowed) == 1:
                    print("Only one possible atom to label this edge: ", end='')
                    incoming[i] = allowed.pop()
                    print(self.ra.tochar[incoming[i]])
                else:
                    incoming[i] = int(input("Heloise, enter an atom: "))

            self.network.add(incoming)
            self.network.print()
            rounds += 1
            print("--------------------------------")
        
with open("dumps/monk.pickle","rb") as f:
    ra = pickle.load(f)
    
game = Game(ra)
game.start()