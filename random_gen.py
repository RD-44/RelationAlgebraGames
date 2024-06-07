import random
import numpy as np
import itertools as it
import matplotlib.pyplot as plt
import pandas as pd

"""
 Are all the units self converse?
Must there be at least one self converse atom
Must (ei, a, a) be consistent, can i choose to forbid it


"""
    
def format(units, diversity_atoms, legal):
    num_atoms = len(units) + len(diversity_atoms)
    table = [['0' for _ in range(num_atoms)] for _ in range(num_atoms)]

    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    tochar = {}
    i = 0
    for e in units:
        tochar[e] = 'e' + str(i).translate(SUB)
        i += 1

    if len(units) == 1:
        e = units.pop()
        tochar[e] = "1'"
        units.add(e)

    i = 0
    for d in diversity_atoms:
        tochar[d] = 'x' + str(i).translate(SUB)
        i += 1

    for l in legal:
        for triple in l:
            table[triple[0]][triple[1]] = table[triple[0]][triple[1]] + '+' + tochar[triple[2]] if table[triple[0]][triple[1]]!='0' else tochar[triple[2]] 
            if table[triple[0]][triple[1]].count('+') == num_atoms - 1:
                table[triple[0]][triple[1]] = '1'

    df = pd.DataFrame(table)
    df = df.rename(columns=tochar, index=tochar)
    df = df.reindex(sorted(df.columns), axis=1)
    df.sort_index(inplace=True)

    return df

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
    num_atoms = 3 #random.randint(2, 5)
    num_converse_pairs = 0 # random.randint(0, num_atoms//2 if num_atoms % 2 != 0 else num_atoms//2 - 1)
    num_self_converse = num_atoms - 2*num_converse_pairs
    print("Atoms: ", num_atoms)
    print("Number of self converse atoms: ", num_self_converse)
    end = num_converse_pairs*2
    atoms = np.array([i for i in range(num_atoms)]) 

    np.random.shuffle(atoms)

    # random composition table
    conv = {atoms[i] : atoms[i+1] for i in range(0, end, 2)} | {atoms[i+1] : atoms[i] for i in range(0, end, 2)} | {atoms[i]  : atoms[i]  for i in range(end, num_atoms)}

    self_converse_atoms = atoms[end:]
    np.random.shuffle(self_converse_atoms)
    num_atoms_below_id = random.randint(1, num_self_converse)
    
    atoms_below_id = self_converse_atoms[:num_atoms_below_id]

    options = set()
    illegal = set()
    legal = set()
    units = set(atoms_below_id)
    diversity_atoms = set(atoms).difference(units)

    for e in atoms_below_id:
        for i in range(num_atoms):
            if (atoms[i] not in units) or (atoms[i] in units and atoms[i] == e) : legal.add(frozenset(peircean((e, atoms[i], atoms[i]), conv)))
            for j in range(i+1, num_atoms):
                illegal.add((e, atoms[i], atoms[j])) # ei;a * b = 0 if a != b
    
    permutations = set(it.product(atoms, repeat=3)) # cartesian product (set of atoms)^3

    while len(permutations) > 0: # group permutations into peircean groups
        curr = permutations.pop()
        group = frozenset(peircean(curr, conv))
        permutations = permutations.difference(group)
        if len(group.intersection(illegal)) == 0 and group not in legal:
            options.add(group)

    for g in options:
        if random.choice([True, False]):
            legal.add(g)

    df = format(units, diversity_atoms, legal)

    print(df)
    
randomRA()

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


