import pandas as pd
from functools import cached_property, lru_cache

class RA:
    def __init__(self, num_symmetric : int, num_units : int, converse : dict[int], legal : set[frozenset[tuple[int, int, int]]]) -> None:
        self.num_symmetric = num_symmetric
        self.num_units = num_units
        self.converse = converse
        self.non_associative_reason = None
        self.num_atoms = len(converse)
        self.table = [[set() for _ in range(self.num_atoms)] for _ in range(self.num_atoms)]
        for l in legal:
            for triple in l:
                self.table[triple[0]][triple[1]].add(converse[triple[2]])   
        self.num_diversity = self.num_atoms - self.num_units
        self._create_symbols()
       
    @cached_property
    def is_associative(self) -> bool:
        for a in range(self.num_atoms): 
            for b in range(self.num_atoms):
                ab = self.table[a][b]
                for c in range(self.num_atoms):
                    lhs = set()
                    for x in ab: lhs.update(self.table[x][c])
                    bc = self.table[b][c]
                    rhs = set()
                    for x in bc: 
                        for r in self.table[a][x]:
                            if r not in lhs:
                                return False
                            rhs.add(r)
                    if len(lhs) != len(rhs):
                        return False
        return True

    def _create_symbols(self) -> None:
        # represent atoms with conventional textual symbols
        self.tochar = {}
        subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        for i in range (self.num_units):
            self.tochar[i] = 'e' + str(i).translate(subscript)
            i += 1
        if self.num_units == 1:
            self.tochar[0] = "1'"
        for i in range(self.num_diversity):
            if len(self.tochar) == self.num_atoms : break
            d = i + self.num_units
            if d not in self.tochar:
                self.tochar[d] = chr(i+97)
                if self.converse[d] != d:
                    self.tochar[self.converse[d]] = self.tochar[d]+'~'
            i += 1

    def supremum(self, atoms) -> str: # returns the sum of a set of atoms (supremum) as a string
        atoms = sorted(list(atoms))
        if len(atoms) == 0 : return '0'
        if len(atoms) == len(self.tochar): return '1'
        s = self.tochar[atoms[0]]
        for i in range(1, len(atoms)):
            s += f'+{self.tochar[atoms[i]]}'
        return s
    
    @lru_cache(maxsize=None)
    def _cached_str(self) -> str:
        formatted_table = [['0' for _ in range(self.num_atoms)] for _ in range(self.num_atoms)]
        for i in range(self.num_atoms):
            for j in range(self.num_atoms):
                formatted_table[i][j] = self.supremum(self.table[i][j])
        formatted_table = pd.DataFrame(formatted_table)
        formatted_table.rename(columns=self.tochar, index=self.tochar, inplace=True)
        formatted_table.columns.name = ';'
        return str(formatted_table)

    def __str__(self) -> str:
        return self._cached_str()

