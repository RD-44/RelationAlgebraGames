import itertools as it
import pandas as pd

class RA:

    def __init__(self, num_symmetric, num_units, converse, legal) -> None:
        self.num_symmetric = num_symmetric
        self.num_units = num_units
        self.converse = converse
        self.associative = None
        self.num_atoms = len(converse)
        self.table = [[set() for _ in range(self.num_atoms)] for _ in range(self.num_atoms)]
        for l in legal:
            for triple in l:
                self.table[triple[0]][triple[1]].add(converse[triple[2]])   
        num_diversity = self.num_atoms - self.num_units

        self.tochar = {}
        subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        for i in range (num_units):
            self.tochar[i] = 'e' + str(i).translate(subscript)
            i += 1
        if num_units == 1:
            self.tochar[0] = "1'"
        for i in range(num_diversity):
            if len(self.tochar) == self.num_atoms : break
            d = i + num_units
            if d not in self.tochar:
                self.tochar[d] = chr(i+97)
                if converse[d] != d:
                    self.tochar[converse[d]] = self.tochar[d]+'~'
            i += 1

        self.formatted_table = [['0' for _ in range(self.num_atoms)] for _ in range(self.num_atoms)]
    
        for i in range(self.num_atoms):
            for j in range(self.num_atoms):
                self.formatted_table[i][j] = self.supremum(self.table[i][j])

        self.formatted_table = pd.DataFrame(self.formatted_table)
        self.formatted_table.rename(columns=self.tochar, index=self.tochar, inplace=True)
        self.formatted_table.columns.name = ';'

        for a, b, c in it.product(range(self.num_atoms), repeat=3): 
            ab = self.table[a][b]
            lhs = set()
            for x in ab:
                lhs.update(self.table[x][c])
            bc = self.table[b][c]
            rhs = set()
            for x in bc:
                rhs.update(self.table[a][x])
            if lhs != rhs:
                #print("Not Associative as", f"({self.tochar[a]};{self.tochar[b]});{self.tochar[c]} = {self.supremum(lhs)} but {self.tochar[a]};({self.tochar[b]};{self.tochar[c]}) = {self.supremum(rhs)}")
                self.associative = False
                return 
        self.associative = True

    def supremum(self, atoms): # returns the sum of a set of atoms (supremum) as a string
        atoms = sorted(list(atoms))
        if len(atoms) == 0 : return '0'
        if len(atoms) == len(self.tochar): return '1'
        s = self.tochar[atoms[0]]
        for i in range(1, len(atoms)):
            s += f'+{self.tochar[atoms[i]]}'
        return s

    def __str__(self) -> str:
        return str(self.formatted_table)
