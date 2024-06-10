import random
import numpy as np
import itertools as it
import matplotlib.pyplot as plt
import pandas as pd
    
def format(num_units, diversity, legal, converse): # creates nicely formatted composition and converse table
    num_atoms = num_units + len(diversity)
    table = [['0' for _ in range(num_atoms)] for _ in range(num_atoms)]

    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    tochar = {}
    i = 0
    for e in range (num_units):
        tochar[e] = 'e' + str(i).translate(SUB)
        i += 1

    if num_units == 1:
        tochar[0] = "1'"

    i = 0
    for d in diversity:
        tochar[d] = 'x' + str(i).translate(SUB)
        i += 1

    triples = []
    for l in legal:
        for triple in l:
            triples.append(triple)

    triples.sort(key = lambda triple : (triple[0], triple[1], converse[triple[2]]))

    for triple in triples:
        table[triple[0]][triple[1]] = table[triple[0]][triple[1]] + '+' + tochar[converse[triple[2]]] if table[triple[0]][triple[1]]!='0' else tochar[converse[triple[2]]] 
        if table[triple[0]][triple[1]].count('+') == num_atoms - 1:
            table[triple[0]][triple[1]] = '1'

    composition_table = pd.DataFrame(table)
    composition_table.rename(columns=tochar, index=tochar, inplace=True)
    composition_table = composition_table.reindex(sorted(composition_table.columns), axis=1)
    composition_table.sort_index(inplace=True)
    composition_table.columns.name = ';'

    converse_table = pd.DataFrame([tochar[converse[x]] for x in converse], index=[tochar[x] for x in range(num_atoms)], columns=['a︶'])
    converse_table.columns.name= 'a'

    return composition_table, converse_table

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
    
def generateRA():
    num_units = 1 #random.randint(1, 2) # number of atoms below the identity 
    num_divs = 2 # number of diversity atoms
    num_atoms = num_units + num_divs 

    atoms = [i for i in range(num_atoms)] # number the atoms
    random_unit = lambda : random.randint(0, num_units-1)
    isunit = lambda x : 0 <= x < num_units # predicate to check if number corresponds to unit
    diversity = [i+num_units for i in range(num_divs)]

    # these dictionaries store start and end of each diversity atom. If d = e_0 ; d : e_1 then starts[d] = e_0
    start = {i : i for i in range(num_units)} 
    end = {i : i for i in range(num_units)} 
    need_converse = False
    nextStart = None
    nextEnd = None
    prev = None
    converse = {i : i for i in range(num_units)} # map of converses

    for i in range(num_divs): # Generate start, end and converse for each diversity atom
        if need_converse:
            start[diversity[i]] = nextStart
            end[diversity[i]] = nextEnd
            converse[prev] = diversity[i]
            converse[diversity[i]] = prev
            need_converse = False
        elif i == num_divs - 1: # if reached last diversity atom and don't need to be in a converse pair, make it self-converse
            start[diversity[i]] = random_unit()
            end[diversity[i]] = start[diversity[i]]
            converse[diversity[i]] = diversity[i]
        else:
            start[diversity[i]] = random_unit()
            end[diversity[i]] = random_unit()
            # If start != end, atom must not be self-converse. If not, can do whatever we want.
            if (start[diversity[i]] != end[diversity[i]]) or random.choice([True, False]): 
                nextStart = end[diversity[i]]
                nextEnd = start[diversity[i]]
                need_converse = True
                prev = diversity[i]
            else: 
                converse[diversity[i]] = diversity[i]

    illegal = set() # stores at least one triple from each forbidden peircean set
    legal = set() # stores peircean sets of triples that must be consistent
    options = set() # stores peircean sets of triples that we are free to forbid or allow
    
    for a, b, c in it.product(atoms, repeat=3): # iterate through all triples
        if start[a] != end[c] or end[b] != start[c] or end[a] != start[b]:
            illegal.add((a, b, c))
        elif isunit(a): 
            if start[b] != a or b != converse[c]:
                illegal.add((a, b, c))
            else:
                legal.add(frozenset(peircean((a, b, c), converse)))
        elif not isunit(b) and not isunit(c): # adds options for not illegal triples that don'tinvolving units
            options.add(frozenset(peircean((a, b, c), converse)))
    
    for l in options: 
        if random.choice([True, False]): # randomly choose peircan sets of triples to make consistent
            legal.add(l)
    
    composition_table, converse_table = format(num_units, diversity, legal, converse) # produce composition table and converse table
    print("Composition: ")
    print(composition_table)
    print("\nConverse: ")
    print(converse_table)

    # print("Units: ", unit)
    # print("Diversity atoms: ", diversity)
    # print("Start: ", start)
    # print("End: ", end)

generateRA()

