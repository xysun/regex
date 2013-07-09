import regex
import unittest

# use basic.dat
class TestRegex(unittest.TestCase):
    def base(self, fname):
        with open(fname) as f:
            self.text = f.readlines()

        for line in self.text:
            [pattern, string] = line.split()
            print(pattern, string)
            nfa = regex.compile(pattern)
            self.assertEqual(nfa.match(string), True)
            print("pass")
    
    def test_basic(self):
        self.base('test_suite.dat')

if __name__ == '__main__':
    unittest.main()
