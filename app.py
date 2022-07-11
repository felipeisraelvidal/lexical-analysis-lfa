import getopt, sys
from DFA import DFA
from bs4 import BeautifulSoup

def read_machine_file(file_path):
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

def main(argv):
    check = True

    machine_file = ''
    input_file = ''
    output_file = ''

    try:
        opts, args = getopt.getopt(argv, 'hm:i:o:', ['mfile=', 'ifile=', 'ofile='])
    except getopt.GetoptError:
        print('app.py -m <machinefile> -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('app.py -m <machinefile> -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-m", "--mfile"):
            machine_file = arg
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    afd = read_machine_file(machine_file)
    machine = DFA(afd[0], afd[1], afd[2], afd[3], afd[4], afd[5])
    
    while (check):
        choice = int(input("\nEscolha uma opção:\n1. Exit\n2. Execute a palavra no AFD\nDigite a sua escolha : "))
        if (choice == 1):
            sys.exit()
        elif (choice == 2):
            palavras = machine.leitura_arquivo(input_file)
            
            resultado = open(output_file, "w")
            resultado.write('Análise Léxica:\n')

            number_of_accepted_tokens = 0
            number_of_invalid_tokens = 0
            
            for palavra in palavras:
                if palavra != '':
                    if machine.run_machine(palavra):
                        number_of_accepted_tokens += 1
                        resultado.write("\t{}\t\t\tACCEPTED\n".format(palavra))
                    else:
                        number_of_invalid_tokens += 1
                        resultado.write("\t{}\t\t\tLEXICAL ERROR\n".format(palavra))
            
            resultado.write('\n------------------------------\n')
            resultado.write(f'Number of tokens analyzed: {number_of_accepted_tokens + number_of_invalid_tokens}\n')
            resultado.write(f'Number of accepted tokens: {number_of_accepted_tokens}\n')
            resultado.write(f'Number of invalid tokens: {number_of_invalid_tokens}\n')
            resultado.write('------------------------------\n')

            resultado.close()
        else:
            check = False

if __name__ == "__main__":
    main(sys.argv[1:])
