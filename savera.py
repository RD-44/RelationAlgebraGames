from relalg import RA
from randRA import nextRA
import pickle

ra = nextRA()

print(ra)
ans = input("Save ra? (y = yes, n = no) \n")
if ans == 'y':
    name = input("Enter file name: ")
    with open(f"dumps/{name}.pickle","wb") as f:
        pickle.dump(ra, f)
    with open(f"dumps/{name}.txt","w") as f:
        f.write(str(ra))
else:
    print("Bye.")
