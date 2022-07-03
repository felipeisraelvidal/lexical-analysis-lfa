import sys

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

lines_delimeters = soup.find_all('delimiter')
DELIMETERS = []
for line in lines_delimeters:
    DELIMETERS.append(line['value'])

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

    def leituraarquivo(self):
        palavras_arquivo = ""
        vet_palavra = []
        palavra = ""
        rascunho_palavra = ""
        cont = 0

        with open("tests/teste.txt","r") as arquivo:
            palavras_arquivo = arquivo.read()
        for i in palavras_arquivo:
            rascunho_palavra += i
            achou_delimitador = [outros in DELIMETERS for outros in rascunho_palavra]
            if (achou_delimitador[cont] == False):
                palavra += i
            else:
                palavra += i
                vet_palavra.append(palavra)
                palavra = ""
            cont += 1
        vet_palavra.append(palavra)
        print(vet_palavra)
        return vet_palavra

    def set_start_accept(self):
        """Takes user input for START_STATE and ACCEPT_STATE, and checks if it's a valid state (if it belongs to Q)"""
        # while (True):
        start = INITIAL_STATE
        print("ESTADO INICIAL: {}".format(start))
        accept = FINAL_STATE
        print("ESTADO FINAL: {}".format(accept))

        return start, accept

    def populate_states(self):
        print("ESTADOS: {}".format(STATES))
        return STATES

    def populate_alphabet(self):
        print("ALFABETO: {}".format(SYMBOLS))
        return SYMBOLS

    def populate_transition_function(self):
        """Creates the transition function (Q X SIGMA -> Q) and prints it out"""
        transition_dict = {el: {el_2: 'REJECT' for el_2 in self.SIGMA} for el in self.Q}

        for key in transition_dict.items():
            for transition in TRANSITIONS:
                transition_dict[transition['from']][transition['symbol']] = transition['to']

        print("\nFUNÇÃO TRANSIÇÃO Q X SIGMA -> Q")
        print("ESTADO ATUAL\tALFABETO DE ENTRADA\tPRÓXIMO ESTADO")
        for key, dict_value in transition_dict.items():
            for input_alphabet, transition_state in dict_value.items():
                print("{}\t\t{}\t\t{}".format(key, input_alphabet, transition_state))

        return transition_dict

    def run_state_transition(self, input_symbol):
        """Takes in current state and goes to next state based on input symbol."""
        if (self.CURRENT_STATE == 'REJECT'):
            return False
        print("ESTADO ATUAL : {}\tSÍMBOLOS DE ENTRADA : {}\t PRÓXIMO ESTADO : {}".format(self.CURRENT_STATE, input_symbol,self.DELTA[self.CURRENT_STATE][input_symbol]))
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
    print("\nMáquina de AFD.")
    machine = DFA()
    while (check):
        choice = int(input("\nEscolha uma opção:\n1. Exit\n2. Execute a palavra no AFD\nDigite a sua escolha : "))
        if (choice == 1):
            sys.exit()
        elif (choice == 2):
            palavra = machine.leituraarquivo()
            print(palavra)
            # print("ACEITA" if machine.run_machine(palavra) else "REJEITADA")
        else:
            check = False
