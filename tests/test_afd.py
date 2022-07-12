import unittest
from DFA import DFA

class TestAFD(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestAFD, self).__init__(*args, **kwargs)

        afd = DFA.read_machine_file('./resources/afd.xml')
        self.machine = DFA(afd[0], afd[1], afd[2], afd[3], afd[4], afd[5])

    def test_ABC(self):
        result = self.machine.run_machine('abc')
        self.assertTrue(result)

    def test_ABB(self):
        result = self.machine.run_machine('abb')
        self.assertFalse(result)

    def test_ABAA(self):
        result = self.machine.run_machine('abaa')
        self.assertFalse(result)

    def test_ABBC(self):
        result = self.machine.run_machine('abbc')
        self.assertFalse(result)

    def test_ABCABC(self):
        result = self.machine.run_machine('abcabc')
        self.assertTrue(result)

    def test_ABBCDA(self):
        result = self.machine.run_machine('abbcda')
        self.assertFalse(result)

if __name__ == 'main':
    unittest.main()
