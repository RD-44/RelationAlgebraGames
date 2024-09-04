import random
import itertools as it
from ras.relalg import RA

def peircean(triple, converse): # returns a set of all peircean transforms of a given triple
    a, b, c = triple
    return set([
        (a, b, c),
        (b, c, a),
        (c, a, b),
        (converse[b], converse[a], converse[c]),
        (converse[a], converse[c], converse[b]),
        (converse[c], converse[b], converse[a])
        ])

def generate(num_units, num_divs): # random NA generator
    num_atoms = num_units + num_divs 
    num_converse_pairs = random.randint(0, num_divs//2)
    num_symmetric = num_divs - 2*num_converse_pairs

    isunit = lambda x : 0 <= x < num_units # predicate to check if number corresponds to unit
    diversity = lambda i : i + num_units

    # these dictionaries store start and end of each diversity atom. If d = e_0 ; d ; e_1 then starts[d] = e_0
    start = {i : i for i in range(num_units)} # initially we only know that for each unit, its start and end is the same unit
    end = {i : i for i in range(num_units)} 
    converse = {i : i for i in range(num_units)}
    # choose random start and end for diversity atons
    for i in range(0, 2*num_converse_pairs-1, 2): 
        start[diversity(i)] = random.randint(0, num_units-1)
        end[diversity(i)] = random.randint(0, num_units-1)
        start[diversity(i+1)] = end[diversity(i)]
        end[diversity(i+1)] = start[diversity(i)]
        converse[diversity(i)] = diversity(i+1)
        converse[diversity(i+1)] = diversity(i)
    for i in range(2*num_converse_pairs, num_divs): # must have same start and end for self-converse atoms
        start[diversity(i)] = random.randint(0, num_units-1)
        end[diversity(i)] = start[diversity(i)]
        converse[diversity(i)] = diversity(i)
        
    legal = set() # stores peircean sets of triples that must be consistent
    
    for a, b, c in it.product(range(num_atoms), repeat=3): # iterate through all triples
        if start[a] != end[c] or end[b] != start[c] or end[a] != start[b]:
            continue
        if isunit(a):
            if start[b] == a and b == converse[c]: 
                legal.add(frozenset(peircean((a, b, c), converse)))
        elif not isunit(b) and not isunit(c): # adds options for not illegal triples that don't involve units
            if random.choice([True, False]):
                legal.add(frozenset(peircean((a, b, c), converse)))
    
    return RA(num_symmetric, num_units, converse, legal)

def nextRA(associativity=True, num_units=random.randint(1, 3), num_divs=random.randint(1, 5)):
    ra = generate(num_units, num_divs)
    while associativity and not ra.is_associative:
        ra = generate(num_units, num_divs)
    return ra