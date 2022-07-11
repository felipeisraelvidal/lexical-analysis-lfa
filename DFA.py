class DFA:

    def __init__(self, states, symbols, transitions, delimiters, final_state, initial_state):
        """Initialize DFSM object"""
        self.STATES = states
        self.SYMBOLS = symbols
        self.TRANSITIONS = transitions
        self.DELIMITERS = delimiters
        self.FINAL_STATE = final_state
        self.INITIAL_STATE = initial_state

        print('state: {}'.format(self.STATES))
        print('symbols: {}'.format(self.SYMBOLS))
        print('transitions: {}'.format(self.TRANSITIONS))
        print('delimiters: {}'.format(self.DELIMITERS))
        print('final_state: {}'.format(self.FINAL_STATE))
        print('initial_state: {}'.format(self.INITIAL_STATE))

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
        verifica_delimitador_unico = False

        with open("tests/leitura.txt", "r") as arquivo:
            palavras_arquivo = arquivo.read()

        for i in palavras_arquivo:
            rascunho_palavra += i
            achou_delimitador = [outros in self.DELIMITERS for outros in rascunho_palavra]
            
            if ((len(palavras_arquivo) == 1) and achou_delimitador[cont] == True):
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

    def set_start_accept(self):
        """Takes user input for START_STATE and ACCEPT_STATE, and checks if it's a valid state (if it belongs to Q)"""
        # while (True):
        start = self.INITIAL_STATE
        # print("ESTADO INICIAL: {}".format(start))
        accept = self.FINAL_STATE
        # print("ESTADO FINAL: {}".format(accept))

        return start, accept

    def populate_states(self):
        # print("ESTADOS: {}".format(STATES))
        return self.STATES

    def populate_alphabet(self):
        # print("ALFABETO: {}".format(SYMBOLS))
        return self.SYMBOLS

    def populate_transition_function(self):
        """Creates the transition function (Q X SIGMA -> Q) and prints it out"""
        transition_dict = {el: {el_2: 'REJECT' for el_2 in self.SIGMA} for el in self.Q}

        for key in transition_dict.items():
            for transition in self.TRANSITIONS:
                transition_dict[transition['from']][transition['symbol']] = transition['to']

        # print("\nFUNÇÃO TRANSIÇÃO Q X SIGMA -> Q")
        # print("ESTADO ATUAL\tALFABETO DE ENTRADA\tPRÓXIMO ESTADO")
        # for key, dict_value in transition_dict.items():
        #     for input_alphabet, transition_state in dict_value.items():
        #         print("{}\t\t{}\t\t{}".format(key, input_alphabet, transition_state))

        return transition_dict

    def run_state_transition(self, input_symbol):
        """Takes in current state and goes to next state based on input symbol."""
        if (self.CURRENT_STATE == 'REJECT'):
            return False
        # print("ESTADO ATUAL : {}\tSÍMBOLOS DE ENTRADA : {}\t PRÓXIMO ESTADO : {}".format(self.CURRENT_STATE, input_symbol,self.DELTA[self.CURRENT_STATE][input_symbol]))
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
        self.CURRENT_STATE = self.INITIAL_STATE
        for ele in in_string:
            check_state = self.run_state_transition(ele)
            # Check if new state is not REJECT
            if (check_state == 'REJECT'):
                return False
        return self.check_if_accept()
