from ras.relalg import RA
from game.models import Network

class Game:
    def __init__(self, ra : RA) -> None:
        self.turn = True
        self.ra = ra
        self.network = Network(ra=ra, adj=[])
        self.rounds = 0
    
    def _output_atoms(self, atoms=None): # prints out atoms and numbers corresponding to them
        if atoms is None:
            for i in range(self.ra.num_atoms):
                print(f'{i} : {self.ra.tochar[i]}')
            return
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
    
    def _begin_round(self):
        self.rounds += 1
        print("--------------------------------")
        print(f'ROUND {self.rounds}\n')
    
    def _first_round(self):
        self._begin_round()
        print("Atoms: ")
        self._output_atoms()
        c = int(input("Abelarde, choose an atom: "))
        if c < self.ra.num_units:
            print("\nHeloise moves (forced)")
            self.network = self.network.add([c])
        elif self.ra.num_units == 1:
            print("\nHeloise moves (forced)")
            self.network = self.network.add([0])
            self.network = self.network.add([c, 0])
        else:
            allowed_units = self.ra.table[c][self.ra.converse[c]] & set(range(self.ra.num_units))
            self._output_atoms(allowed_units)
            if len(allowed_units) > 1:
                x = int(input(f"Enter a unit to label edge 0 -> 0: "))
            else:
                x = allowed_units.pop()
                print(f"Heloise picks {self.ra.tochar[x]} (forced).")
            self.network = self.network.add([x])

            allowed_units = self.ra.table[self.ra.converse[c]][c] & set(range(self.ra.num_units))
            self._output_atoms(allowed_units)
            if len(allowed_units) > 1:
                x = int(input(f"Enter a unit to label edge 1 -> 1: "))
            else:
                x = allowed_units.pop()
                print(f"Heloise picks {self.ra.tochar[x]} (forced).")
            self.network = self.network.add([c, x])

    def _get_abelarde_moves(self):
        moves = {}
        for x in range(len(self.network.adj)):
            for y in range(len(self.network.adj)):
                c = self.network.adj[x][y]
                pairs = []
                for i in range(self.ra.num_atoms):
                    for j in range(self.ra.num_atoms):
                        if c in self.ra.table[i][j]:
                            valid = True
                            for z in range(len(self.network.adj[x])):
                                if self.network.adj[x][z] == i and self.network.adj[z][y] == j:
                                    valid = False
                                    break
                            if valid : pairs.append((i, j))
                if len(pairs) > 0 : moves[(x, y)] = pairs
        return moves

    def _abelarde(self):
        moves = self._get_abelarde_moves()
        if len(moves)==0:
            print("Representation found. Heloise wins.")
            return None
        
        x = int(input("Abelarde, pick node x: "))
        y = int(input("Abelarde, pick node y: "))
        c = self.network.adj[x][y]
        print(f'\nN({x}, {y}) = {self.ra.tochar[c]}')

        if (x, y) not in moves:
            print("Abelarde made a bad move. Heloise wins.")
            return None

        pairs = moves[(x, y)]

        i = 0
        if len(pairs) == 0:
            print("Abelarde cannot make any good moves using nodes x and y. Next round.")
            return None
        elif len(pairs) == 1:
            print("Only one move is possible here: ")
            self._output_pairs(pairs)
        else:
            print(f"Possible pairs (a', b') such that a';b' >= {self.ra.tochar[c]}:")
            self._output_pairs(pairs)
            i = int(input(f"Abelarde, pick a pair: "))
        a, b = pairs[i]
        return x, y, a, b
    
    def _heloise(self, x, y, a, b):
        incoming = [-1 for _ in range(len(self.network.adj) + 1)]
        incoming[x] = a
        incoming[y] = self.ra.converse[b]

        if self.ra.num_units == 1:
            incoming[-1] = 0
        else:
            allowed_units = set()
            atoms = self.ra.table[self.ra.converse[a]][a] & self.ra.table[b][self.ra.converse[b]]
            for i in range(self.ra.num_units):
                if i in atoms:
                    allowed_units.add(i)
            self._output_atoms(allowed_units)
            if len(allowed_units) == 0:
                print("Heloise cannot label the self loop with a valid unit. Abelarde wins.")
                return True
            if len(allowed_units) > 1:
                x = int(input(f"Heloise, pick a unit: "))
            else:
                x = allowed_units.pop()
                print(f"Heloise picks {self.ra.tochar[x]} (forced).")
            incoming[-1] = x

        for i in range(len(incoming)):
            if incoming[i] != -1: continue
            print(f"\nLabelling edge: {i} -> {len(self.network.adj)}")

            allowed = set(range(self.ra.num_atoms))
            for j in range(len(self.network.adj)):
                if j != i and incoming[j]!=-1:
                    allowed &= self.ra.table[self.network.adj[i][j]][incoming[j]] # limits Heloise's moves by removing atoms that would create forbidden triples

            for k in range(self.ra.num_units):
                if k in allowed : allowed.remove(k)

            print("Allowed atoms:")
            self._output_atoms(allowed)
            if len(allowed) == 0:
                print("Heloise cannot label this edge with a valid atom. Abelarde wins.")
                return True
            if len(allowed) == 1:
                print("Only one possible atom to label this edge: ", end='')
                incoming[i] = allowed.pop()
                print(self.ra.tochar[incoming[i]])
            else:
                incoming[i] = int(input("Heloise, enter an atom: "))

        self.network = self.network.add(incoming)
        return False

    def play(self):
        print("Game has begun on the following relation algebra: \n", self.ra)
        self._first_round()
        self.network.display()
        while True: 
            self._begin_round()
            # Abelarde's turn
            picked = self._abelarde()
            if picked is None: 
                return 'Heloise'
            x, y, a, b = picked
            # Heloise's turn
            result = self._heloise(x, y, a, b)
            if result == True : return 'Abelarde'
            self.network.display()