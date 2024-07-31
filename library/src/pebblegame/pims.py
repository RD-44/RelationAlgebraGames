import pickle
from ras.relalg import RA
from pebblegame.models import Network
import numpy as np
import itertools as it

def consistent(ra : RA, adj : np.ndarray) -> bool:
    for i in range(len(adj)):
        for i, j, k in it.product(range(len(adj)), repeat=3):
            a, b, c = adj[i][j].item(), adj[j][k].item(), adj[i][k].item()
            if c not in ra.table[a][b] : return False
        return True

def construct_networks(ra : RA, n : int) -> list[np.ndarray]:
    # computes every possible CONSISTENT size n network using the given RA
    labellings = it.product(range(ra.num_atoms), repeat=(n*(n+1))//2)
    networks = []
    for labelling in labellings:
        arr = list(labelling)
        #print(arr)
        adj = np.zeros((n, n), dtype=int)
        k = 0
        valid = True
        for i in range(n):
            if arr[k] >= ra.num_units :
                valid = False
                break
            for j in range(i, n):
                adj[i][j] = arr[k]
                adj[j][i] = ra.converse[adj[i][j]]
                k += 1
        if valid and consistent(ra, adj): networks.append(adj)
    return networks

def is_match(adj, test, x, y, z, a, b):
    n = len(adj)
    if test[x][z] != a or test[z][y] != b : return False
    for i, j in it.product(range(n), repeat=2):
        if i != z and j != z and test[i][j] != adj[i][j]:
            # in this case the test network does not agree with adj off of z, so discard
            return False
    return True

def good_network(networks : np.ndarray, i : int, ra : RA, n : int) -> bool:
    adj = networks[i]
    for x, y, z in it.product(range(n), repeat=3):
        if z == x or z == y : continue
        for a, b in it.product(range(ra.num_atoms), repeat=2):
            if adj[x][y] not in ra.table[a][b] : continue
            if adj[x][z] == a and adj[z][y] == b : continue
            found = False
            for j in range(len(networks)):
                if is_match(adj, networks[j], x, y, z, a, b):
                    found = True
                    break
            if not found : return False
    return True

def find_basis(ra : RA, n : int):
    # finds an n-dimensional basis for the given RA if one exists
    networks = construct_networks(ra, n)
    i = 0
    while i < len(networks):
        if good_network(networks, i, ra, n):
            print("YES")
            i += 1
        else:
            print("NO")
            networks.pop(i)
            i = 0
    if len(networks) == 0:
        print("NO BASIS")
    else:
        print("BASIS FOUND")
        print(networks)
        

with open("library/tests/test_ras/ra1.pickle", "rb") as f:
    ra = pickle.load(f)

find_basis(ra, 5)

# TODO: need to check triangle addition property of the networks. Consider converting the networks to some string format which means you can make the networks into a set of strings
# maybe even generate tuples in construct_networks itself, although this will be complicated. 
# figure out the triangle addition property, email robin if you have to, Gl man you are amazing
# some random ideas that came to mind:

"""
- What about making this n-dim basis finder as optimised as possible?
- Any stages of the process that can be parallelised?
- Any chance machine learning can be used to speed up a certain stage?
This is a fun optimisation problem, use Leetcode skills
"""

    






    
    