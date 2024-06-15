"""we generate a large number of RAs of a single type and estimate
the proportion of associative algebras
""" 
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ras.relalg
sys.modules['relalg'] = ras.relalg
from ras.randomRA import nextRA

def sample(count, num_divs, quiet=True):
    associative_count = 0

    for _ in range(count):
        ra = nextRA(associativity=False, num_units=1, num_divs=num_divs)
        if ra.associative:
            associative_count += 1
        elif not quiet:
            print(ra)
            print(ra.non_associative_reason, '\n')

    return associative_count

limit = 60
ys = []
for i in range(1, limit+1):
    print(i)
    associative_count = sample(100, i)
    ys.append(associative_count)

xs = range(1, limit+1)
print(ys)
plt.plot(xs, ys)
plt.show()