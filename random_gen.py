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
    
    def __le__(self, other):
        return self + other == other

    def isaatom(self):
        return (self.i != 0 and (self.i & (self.i - 1) == 0))

    def __eq__(self, other):
        return self.i == other.i
    

class RA:

    def __init__(self, base_size, forbidden, converses) -> None:
        self.base_size = base_size
        self.converses = converses
        self.forbidden = forbidden

    
    


def randomRA():
    num_atoms = random.randint(2, 10)
    num_converse_pairs = random.randint(0, num_atoms//2)
    print("Atoms: ", num_atoms)
    print("Non-self converse atoms: ", num_converse_pairs*2)
    end = num_converse_pairs*2
    converses = {i : i+1 for i in range(0, end, 2)} | {i+1:i for i in range(0, end, 2)} | {i : i for i in range(end, num_atoms)}




    assert(len(converses)==num_atoms)
    print(converses)

randomRA()
    
print(~3)
# think about how to represent forbidden triples. Also ask in the next meeting how to check for associativity
