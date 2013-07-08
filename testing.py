import regex
import unittest

class TestRegex(unittest.TestCase):
    def test_star(self):
        p = 'ba*'
        nfa = regex.compile(p)
        self.assertEqual(nfa.match('ba'), True)
        self.assertEqual(nfa.match('b'), True)
        self.assertEqual(nfa.match('baa'), True)
    
    def test_plus(self):
        p = 'ba+'
        nfa = regex.compile(p)
        self.assertEqual(nfa.match('ba'), True)
        self.assertEqual(nfa.match('b'), False)

    def test_qmark(self):
        p = 'ba?'
        nfa = regex.compile(p)
        self.assertEqual(nfa.match('b'), True)
        self.assertEqual(nfa.match('ba'), True)
        self.assertEqual(nfa.match('baa'), False)

if __name__ == '__main__':
    unittest.main()
