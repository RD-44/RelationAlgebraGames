from ras.random_ra import nextRA
import unittest

class TestRandom(unittest.TestCase):

    def test_ra_associative(self):
        ra = nextRA(associativity=True)
        self.assertTrue(ra.is_associative)
    
    def test_ra_structure(self):
        ra = nextRA()
        for atom in ra.converse:
            self.assertTrue(ra.converse[ra.converse[atom]] == atom)
        for i in range(ra.num_units):
            self.assertTrue(ra.converse[i] == i)
            for j in range(ra.num_units):
                if i == j:
                    self.assertTrue(ra.table[i][i] == set([i]))
                else:
                    self.assertTrue(ra.table[i][j] == set())
            for j in range(ra.num_units, ra.num_atoms):
                self.assertTrue((ra.table[i][j] == set()) != (ra.table[i][j] == set([j])))

    

if __name__ == '__main__':
    unittest.main()