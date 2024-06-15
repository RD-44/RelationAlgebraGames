from relalg import RA
from randomRA import nextRA
import pickle

while True:
    ra = nextRA(num_units=1, num_divs=2, associativity=False)
    print(ra)
    print("Associative:", ra.associative)
    ans = input("Save ra? (y = yes, n = no, q = quit) \n")
    if ans == 'y':
        name = input("Enter file name: ")
        with open(f"dumps/{name}.pickle","wb") as f:
            pickle.dump(ra, f)
        with open(f"dumps/{name}.txt","w") as f:
            f.write(str(ra))
    elif ans == 'n':
        print('\n')
        continue
    else:
        break
