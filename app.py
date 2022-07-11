import sys
from DFA import DFA
from bs4 import BeautifulSoup

def read_file(file_path):
    with open(file_path, 'r') as f:
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

    return (STATES, SYMBOLS, TRANSITIONS, DELIMETERS, FINAL_STATE, INITIAL_STATE)

if __name__ == "__main__":
    check = True
    # print("\nMáquina de AFD.")
    afd = read_file('tests/afd.xml')
    print('teste: {}'.format(afd[0]))
    machine = DFA(afd[0], afd[1], afd[2], afd[3], afd[4], afd[5])
    while (check):
        choice = int(input("\nEscolha uma opção:\n1. Exit\n2. Execute a palavra no AFD\nDigite a sua escolha : "))
        if (choice == 1):
            sys.exit()
        elif (choice == 2):
            palavras = machine.leituraarquivo()
            resultado = open("resultado.txt", "w")
            for palavra in palavras:
                resultado.write("{} : ACEITA\n".format(palavra) if machine.run_machine(palavra) else "{} : Erro lexico!\n".format(palavra))
            resultado.close()
        else:
            check = False
