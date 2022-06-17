from bs4 import BeautifulSoup

# LEITURA DO ARQUIVO XML / GET valores do arquivo XML

with open('tests/afd.xml', 'r') as f:
    file = f.read()

soup = BeautifulSoup(file, 'xml')

lines_states = soup.find_all('state')
STATES = []
for line in lines_states:
    STATES.append(line['value'])

lines_symbols = soup.find_all('symbol')
SYMBOLS = []
for line in lines_symbols:
    SYMBOLS.append(line['value'])

TRANSITIONS = soup.find_all('transition')

lines_finalState = soup.find_all('finalState')
FINAL_STATE = None
for line in lines_finalState:
    FINAL_STATE = line['id']

lines_initialState = soup.find_all('initialState')
INITIAL_STATE = None
for line in lines_initialState:
    INITIAL_STATE = line['id']

class DFA:

    def __init__(self):
        """Initialize DFSM object"""
        self.Q = self.populate_states()
        self.SIGMA = self.populate_alphabet()
        self.DELTA = self.populate_transition_function()
        self.START_STATE, self.ACCEPT_STATES = self.set_start_accept()
        self.CURRENT_STATE = None

    def set_start_accept(self):
        """Takes user input for START_STATE and ACCEPT_STATE, and checks if it's a valid state (if it belongs to Q)"""
        # while (True):
        start = INITIAL_STATE
        print("START STATE: {}".format(start))
        accept = FINAL_STATE
        print("FINAL STATE: {}".format(accept))

        return start, accept

    def populate_states(self):
        print("STATES: {}".format(STATES))
        return STATES

    def populate_alphabet(self):
        print("ALPHABET : {}".format(SYMBOLS))
        return SYMBOLS

    def populate_transition_function(self):
        """Creates the transition function (Q X SIGMA -> Q) and prints it out"""
        transition_dict = {el: {el_2: 'REJECT' for el_2 in self.SIGMA} for el in self.Q}
        print(transition_dict)

        for key in transition_dict.items():
            for transition in TRANSITIONS:
                transition_dict[transition['from']][transition['symbol']] = transition['to']

        print("\nTRANSITION FUNCTION Q X SIGMA -> Q")
        print("CURRENT STATE\tINPUT ALPHABET\tNEXT STATE")
        for key, dict_value in transition_dict.items():
            for input_alphabet, transition_state in dict_value.items():
                print("{}\t\t{}\t\t{}".format(key, input_alphabet, transition_state))

        return transition_dict

    def run_state_transition(self, input_symbol):
        """Takes in current state and goes to next state based on input symbol."""
        if (self.CURRENT_STATE == 'REJECT'):
            return False
        print("CURRENT STATE : {}\tINPUT SYMBOL : {}\t NEXT STATE : {}".format(self.CURRENT_STATE, input_symbol,self.DELTA[self.CURRENT_STATE][input_symbol]))
        self.CURRENT_STATE = self.DELTA[self.CURRENT_STATE][input_symbol]
        return self.CURRENT_STATE

    def check_if_accept(self):
        """Checks if the current state is one of the accept states."""
        if self.CURRENT_STATE in self.ACCEPT_STATES:
            return True
        else:
            return False

    def run_machine(self, in_string):
        """Run the machine on input string"""
        self.CURRENT_STATE = INITIAL_STATE
        for ele in in_string:
            check_state = self.run_state_transition(ele)
            # Check if new state is not REJECT
            if (check_state == 'REJECT'):
                return False
        return self.check_if_accept()


if __name__ == "__main__":
    check = True
    print("\nDeterministic Finite State Machine.")
    machine = DFA()
    while (check):
        choice = int(input("\nEnter Choice:\n1. Replace DFSM\n2. Run DFSM on input string\nEnter choice : "))
        if (choice == 1):
            machine = DFA()
        elif (choice == 2):
            input_string = list(input("Enter the input string : "))
            print("ACCEPTED" if machine.run_machine(input_string) else "REJECTED")
        else:
            check = False
