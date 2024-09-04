import pickle
from ras.relalg import RA, create_symbols
from ras.random_ra import peircean
import itertools as it


def create(num_units : int | None = None, num_divs : int | None = None) -> RA:
    if num_units is None : num_units = int(input("Enter number of units: "))
    if num_divs is None : num_divs = int(input("Enter number of diversity atoms: "))
    num_converse_pairs = int(input(f"Enter number of diversity atom converse pairs (must be in range [0, {num_divs//2}]): "))
    num_symmetric = num_divs - 2*num_converse_pairs
    num_atoms = num_units + num_divs 

    isunit = lambda x : 0 <= x < num_units # predicate to check if number corresponds to unit
    diversity = lambda i : i + num_units

    # these dictionaries store start and end of each diversity atom. If d = e_0 ; d : e_1 then starts[d] = e_0
    start = {i : i for i in range(num_units)} 
    end = {i : i for i in range(num_units)} 
    converse = {i : i for i in range(num_units)}

    # form converse table 
    for i in range(0, 2*num_converse_pairs-1, 2): 
        converse[diversity(i)] = diversity(i+1)
        converse[diversity(i+1)] = diversity(i)
    for i in range(2*num_converse_pairs, num_divs): # must have same start and end for self-converse atoms
        converse[diversity(i)] = diversity(i)

    tochar = create_symbols(num_units, num_divs, converse)
    toint = {k:v for v,k in tochar.items()}

    print("Atoms:", list(tochar.values()))

    # choose random start and end for diversity atons
    for i in range(0, 2*num_converse_pairs-1, 2): 
        start[diversity(i)] = toint(input(f"Enter start for {tochar[i]}")) if num_units > 1 else 0
        end[diversity(i)] = toint(input(f"Enter end for {tochar[i]}")) if num_units > 1 else 0
        start[diversity(i+1)] = end[diversity(i)]
        end[diversity(i+1)] = start[diversity(i)]
    for i in range(2*num_converse_pairs, num_divs): # must have same start and end for self-converse atoms
        start[diversity(i)] = toint(input(f"Enter start for {tochar[i]}")) if num_units > 1 else 0
        end[diversity(i)] = start[diversity(i)]

    legal = set() # stores peircean sets of triples that must be consistent
    options = set() # stores peircean sets of triples that we are free to forbid or allow

    for a, b, c in it.product(range(num_atoms), repeat=3): # iterate through all triples
        if start[a] != end[c] or end[b] != start[c] or end[a] != start[b]:
            continue
        if isunit(a): 
            if start[b] == a and b == converse[c]:
                legal.add(frozenset(peircean((a, b, c), converse)))
        elif not isunit(b) and not isunit(c): # adds options for not illegal triples that don't involve units
            options.add(frozenset(peircean((a, b, c), converse)))


    for l in options: 
        for triple in l:
            print(f"{tochar[triple[0]]};{tochar[triple[1]]} >= {tochar[converse[triple[2]]]}")

        if input("Yes or no") == "y": # randomly choose peircan sets of triples to make consistent
            legal.add(l)

    ra = RA(num_symmetric, num_units, converse, legal)

    print(f"<{num_units},{num_symmetric},{num_converse_pairs}>")
    print(ra)

    ans = input("Save ra? (y = yes, n = no) \n")
    if ans == 'y':
        name = input("Enter file name: ")
        with open(f"notrepresentable/{name}.pickle","wb") as f:
            pickle.dump(ra, f)
        with open(f"notrepresentable/{name}.txt","w") as f:
            f.write(str(ra))

    # options = list(options)
    # n = 1<<len(options)
    # choices = []
    # count = 0
    # for i in range(n):
    #     choice = set()
    #     for j in range(len(options)):
    #         if (i & 1):
    #             choice.add(options[j])
    #         i >>= 1
    #     choice.update(legal)
    #     choices.append(choice)
    #     ra = RA(num_symmetric, num_units, converse, choice)
    #     if ra.is_associative : 
    #         print(ra, '\n')
    #         for group in choice:
    #             triple = sorted(group)[0]
    #             print(f"{tochar[triple[0]]}{tochar[triple[1]]}{tochar[converse[triple[2]]]}")
    #         count += 1
    


create()