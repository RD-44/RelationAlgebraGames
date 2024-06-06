import random
import numpy as np
import itertools as it
import matplotlib.pyplot as plt
import pandas as pd

"""
 Are all the units self converse?
Must there be at least one self converse atom
"""

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

def peircean(triple, conv): # returns a set of all peircean transforms of a given triple
    a, b, c = triple
    return set([
        (a, b, c),
        (b, conv[c], conv[a]),
        (conv[c], a, conv[b]),
        (conv[b], conv[a], conv[c]),
        (conv[a], c, b),
        (c, conv[b], a)
        ])
    
def randomRA():
    num_atoms = random.randint(2, 5)
    num_converse_pairs = random.randint(0, num_atoms//2 if num_atoms % 2 != 0 else num_atoms//2 - 1)
    num_self_converse = num_atoms - 2*num_converse_pairs
    print("Atoms: ", num_atoms)
    print("Number of self converse atoms: ", num_self_converse)
    end = num_converse_pairs*2
    atoms = np.array([i for i in range(num_atoms)]) #chr(97+i) 

    np.random.shuffle(atoms)
    conv = {atoms[i] : atoms[i+1] for i in range(0, end, 2)} | {atoms[i+1] : atoms[i] for i in range(0, end, 2)} | {atoms[i]  : atoms[i]  for i in range(end, num_atoms)}

    self_converse_atoms = atoms[end:]
    np.random.shuffle(self_converse_atoms)
    num_atoms_below_id = random.randint(1, num_self_converse)
    
    atoms_below_id = self_converse_atoms[:num_atoms_below_id]
    print(atoms_below_id)

    perms = set(it.product(atoms, repeat=3))

    groups = set()

    illegal = set()

    legal = set()

    for e in atoms_below_id:
        for i in range(num_atoms):
            legal.add(frozenset(peircean((e, atoms[i], atoms[i]), conv)))
            for j in range(i+1, num_atoms):
                illegal.add((e, atoms[i], atoms[j]))

    while len(perms) > 0:
        curr = perms.pop()
        group = frozenset(peircean(curr, conv))
        perms = perms.difference(group)
        if len(group.intersection(illegal)) == 0 and group not in legal:
            groups.add(group)

    for g in groups:
        if random.choice([True, False]):
            legal.add(g)


    table = [["" for _ in range(num_atoms)] for _ in range(num_atoms)]

    tochar = {}
    for i in range(num_atoms_below_id):
        tochar[atoms_below_id[i]] = 'e' + str(i)
    i = 0
    for j in range(num_atoms_below_id, num_self_converse):
        tochar[self_converse_atoms[j]] = 'x' + str(i)
        i += 1
    for j in range(end):
        tochar[atoms[j]] = 'x' + str(i)
        i += 1
    for l in legal:
        for triple in l:
            table[triple[0]][triple[1]] += '+' + tochar[triple[2]] if table[triple[0]][triple[1]] else tochar[triple[2]] 

    df = pd.DataFrame(table)
    df = df.rename(columns=tochar, index=tochar)
    df = df.reindex(sorted(df.columns), axis=1)
    df.sort_index(inplace=True)
        
    print(df)
    
randomRA()

