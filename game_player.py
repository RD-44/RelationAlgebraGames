from relalg import RA
from randRA import nextRA
import pickle
import pandas as pd
    
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

class Game:
    def __init__(self, ra : RA) -> None:
        self.turn = True
        self.ra = ra
        self.network = Network(ra)
    
    def _output_atoms(self): # prints out atoms and numbers corresponding to them
        for i in range(self.ra.num_atoms-1):
            print(f'{i} : {self.ra.tochar[i]}', end=', ')
        print(f'{self.ra.num_atoms-1} : {self.ra.tochar[self.ra.num_atoms-1]}')

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
        a = int(input("Abalarde, choose an atom: "))

        if a < self.ra.num_units:
            print("\nHeloise moves (forced)")
            self.network.add([a])
        else:
            if self.ra.num_units == 1:
                print("Heloise moves (forced)")
                self.network.add([0])
                self.network.add([a, 0])
            else:
                x = int(input(f"Enter a unit to label edge (0, 0): "))
                self.network.add([x])
                x = int(input(f"Enter a unit to label edge (1, 1): "))
                self.network.add([a, x])
        print(self.network)
        while True:
            print(f"Nodes: {[i for i in range(len(self.network.adj))]}")
            x = int(input("Abalarde, pick node x: "))
            y = int(input("Abalarde, pick node y: "))
            a = self.network.adj[x][y]
            print(f'\nN({x}, {y}) = {self.ra.tochar[a]}')
            pairs = []
            for i in range(self.ra.num_atoms):
                for j in range(self.ra.num_atoms):
                    if a in self.ra.table[i][j]:
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
                print("Possible pairs (a', b') such that a';b' >= {self.ra.tochar[a]}:")
                i = int(input(f"Abalarde, pick a pair: "))

            pair = pairs[i]

            incoming = [-1 for _ in range(len(self.network.adj) + 1)]

            incoming[x] = pair[0]
            incoming[y] = pair[1]
            incoming[-1] = 0

            self.network.add(incoming)
            print(self.network)
            break
        

with open("dumps/ra3.pickle","rb") as f:
    ra = pickle.load(f)

# print(ra)

# net = Network(ra)

# net.add([0])
# net.add([1, 0])
# net.add([2, 1, 0])

# print(net)

game = Game(ra)
game.start()