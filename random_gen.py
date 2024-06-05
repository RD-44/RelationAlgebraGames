import random
import numpy as np

class Elem: # element of relation algebra
    def __init__(self, i, size):
        if size == 0 or (size & (size - 1) != 0):
            raise Exception("Error - size must be power of 2.")
        self.i = i
        self.size = size
    
    def __str__(self) -> str:
        return str(self.i)
    
    def __mul__(self, other): # boolean AND
        return Elem(self.i & other.i)
    
    def __add__(self, other): # boolean OR
        return Elem(self.i | other.i)
    
    def __neg__(self): # boolean negation
        return Elem(self.size - 1 - self.i, self.size)

    def __invert__(self): # converse (yet to implement)
        pass
    
    def __le__(self, other):  # a <= b iff a + b = b
        return self + other == other

    def isaatom(self): # atoms are represented by powers of 2
        return (self.i != 0 and (self.i & (self.i - 1) == 0))
    

    def __eq__(self, other):
        return self.i == other.i
    

class RA:

    def __init__(self, base_size, composition, converses) -> None:
        self.base_size = base_size
        self.converses = converses
        self.composition = composition

def randomRA():
    num_atoms = 3 #random.randint(2, 10)
    num_converse_pairs = random.randint(0, num_atoms//2)
    print("Atoms: ", num_atoms)
    print("Non-self converse atoms: ", num_converse_pairs*2)
    end = num_converse_pairs*2
    atoms = np.array([chr(97+i) for i in range(num_atoms)])
    np.random.shuffle(atoms)

    converse = {atoms[i] : atoms[i+1] for i in range(0, end, 2)} | {atoms[i+1] : atoms[i] for i in range(0, end, 2)} | {atoms[i]  : atoms[i]  for i in range(end, num_atoms)}
    composition = [[set() for _ in range(num_atoms)] for _ in range(num_atoms)] # composition table

    for i in range(num_atoms):
        for j in range(num_atoms):
            for k in range(num_atoms):
                if random.choice([True, False]):
                    composition[i][j].add(converse[atoms[k]])
                    composition[j][k].add(converse[atoms[i]])
                    composition[k][i].add(converse[atoms[j]])
                    
        
    for row in composition:
        print(*row, sep="\t")

    print(converse)

randomRA()

