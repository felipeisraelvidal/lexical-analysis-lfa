import imp
import sys
from bs4 import BeautifulSoup
from helpers import validate_file_extension

class DFA:

    def __init__(self, states, symbols, transitions, delimiters, final_state, initial_state):
        """Initialize DFSM object"""
        self.states = states
        self.symbols = symbols
        self.transitions = transitions
        self.delimiters = delimiters
        self.final_state = final_state
        self.initial_state = initial_state

        self.q = self.populate_states()
        self.sigma = self.populate_alphabet()
        self.delta = self.populate_transition_function()
        self.state_state, self.accept_states = self.__set_start_accept()
        self.current_state = None

    @staticmethod
    def read_machine_file(file_path):

        is_valid_extension = validate_file_extension(file_path, '.xml')
        if is_valid_extension == False:
            print('Invalid machine file extension')
            sys.exit()

        with open(file_path, 'r') as f:
            file = f.read()

        soup = BeautifulSoup(file, 'xml')

        lines_states = soup.find('states').find_all('state')
        states = []
        for line in lines_states:
            states.append(line['id'])

        lines_symbols = soup.find('symbols').find_all('symbol')
        symbols = []
        for line in lines_symbols:
            symbols.append(line['id'])

        lines_transitions = soup.find('transitions').find_all('transition')
        transitions = []
        for line in lines_transitions:
            transitions.append({
                'from': line['from'],
                'to': line['to'],
                'symbol': line['symbol']
            })

        lines_delimeters = soup.find_all('delimiter')
        delimiters = []
        for line in lines_delimeters:
            delimiters.append(line['value'])

        lines_final_states = soup.find('finalStates').find_all('finalState')
        final_states = None
        for line in lines_final_states:
            final_states = line['id']

        lines_initial_state = soup.find_all('initialState')
        initial_state = None
        for line in lines_initial_state:
            initial_state = line['id']

        return (states, symbols, transitions, delimiters, final_states, initial_state)

    def populate_states(self):
        return self.states

    def populate_alphabet(self):
        return self.symbols

    def populate_transition_function(self):
        """Creates the transition function (Q X SIGMA -> Q) and prints it out"""
        transition_dict = {el: {el_2: 'REJECT' for el_2 in self.sigma} for el in self.q}

        for _ in transition_dict.items():
            for transition in self.transitions:
                transition_dict[transition['from']][transition['symbol']] = transition['to']

        return transition_dict

    def extract_tokens(self, str_input):
        vet_palavra = []
        palavra = ""
        rascunho_palavra = ""
        cont = 0
        verifica_delimitador_unico = False

        for i in str_input:
            rascunho_palavra += i
            achou_delimitador = [outros in self.delimiters for outros in rascunho_palavra]
            
            if ((len(str_input) == 1) and achou_delimitador[cont] == True):
                verifica_delimitador_unico = True
                break
            elif (achou_delimitador[cont] == False):
                palavra += i
            else:
                vet_palavra.append(palavra)
                palavra = ""
            
            cont += 1

        if(verifica_delimitador_unico != True):
            vet_palavra.append(palavra)

        return vet_palavra

    def __set_start_accept(self):
        """Takes user input for START_STATE and ACCEPT_STATE, and checks if it's a valid state (if it belongs to Q)"""
        start = self.initial_state
        accept = self.final_state
        return start, accept

    def __run_state_transition(self, input_symbol):
        """Takes in current state and goes to next state based on input symbol."""
        if (self.current_state == 'REJECT'):
            return False

        if input_symbol not in self.symbols:
            self.current_state = 'REJECT'
        else:
            self.current_state = self.delta[self.current_state][input_symbol]
        
        return self.current_state

    def run_machine(self, in_string):
        """Run the machine on input string"""
        self.current_state = self.initial_state
        
        for ele in in_string:
            check_state = self.__run_state_transition(ele)
            
            # Check if new state is not REJECT
            if (check_state == 'REJECT'):
                return False

        if self.current_state in self.accept_states:
            return True
        else:
            return False
