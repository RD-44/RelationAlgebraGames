from randRA import nextRA
import unittest

class TestRandom(unittest.TestCase):

    def test_ra(self):
        ra = nextRA(associativity=True)
        self.assertEqual(ra.num_atoms, len(ra.converse))
        self.assertEqual(ra.num_atoms, len(ra.table))
        self.assertEqual(ra.num_atoms, len(ra.formatted_table))
        self.assertTrue(ra.associative)
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