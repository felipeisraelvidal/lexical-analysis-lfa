import unittest
from DFA import DFA

class TestAFD(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)

        self.machine = DFA()

    def test_ABC(self):
        self.assertTrue(True)

    def test_ABB(self):
        self.assertTrue(True)

    def test_ABAA(self):
        self.assertTrue(True)

if __name__ == 'main':
    unittest.main()
