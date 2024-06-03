import random

class Elem:
    def __init__(self, i, base_size):
        if base_size == 0 or (base_size & (base_size - 1) != 0):
            raise Exception("Error - base_size must be power of 2.")
        self.i = i
        self.base_size = base_size
    
    def __str__(self) -> str:
        return str(self.i)
    
    def __mul__(self, other):
        return Elem(self.i & other.i)
    
    def __add__(self, other):
        return Elem(self.i | other.i)
    
    def __neg__(self):
        return Elem(self.base_size - 1 - self.i, self.base_size)
    
    def isaatom(self):
        return (self.i != 0 and (self.i & (self.i - 1) == 0))

class RA:

    def __init__(self, base_size, forbidden, converse) -> None:
        self.base_size = base_size

# think about how to represent forbidden triples. Also ask in the next meeting how to check for associativity

t1 = Elem(9, 16)
t2 = Elem(8, 32)

print(-t1)

print(t1.isaatom())
