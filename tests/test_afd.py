import unittest
from DFA import DFA

class TestAFD(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)

        self.machine = DFA([], [], [], [], [], None)

    def test_ABC(self):
        result = self.machine.run_machine('ABC')
        self.assertTrue(result)

    def test_ABB(self):
        result = self.machine.run_machine('ABB')
        self.assertFalse(result)

    def test_ABAA(self):
        result = self.machine.run_machine('ABAA')
        self.assertFalse(result)

    def test_ABBC(self):
        result = self.machine.run_machine('ABBC')
        self.assertFalse(result)

if __name__ == 'main':
    unittest.main()
