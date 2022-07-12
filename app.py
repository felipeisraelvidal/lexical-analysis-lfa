import getopt, sys
from DFA import DFA
from bs4 import BeautifulSoup

def read_machine_file(file_path):
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

    transitions = soup.find('transitions').find_all('transition')

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

def read_input_file(file_path):
    with open(file_path, "r") as arquivo:
        str_input = arquivo.read()
        str_input = str_input.replace('\n', '')

    return str_input

def start_analysis(machine, str_input, output_file):
    tokens = machine.extract_tokens(str_input)
            
    resultado = open(output_file, "w")
    resultado.write('Lexical Analysis:\n')

    number_of_accepted_tokens = 0
    number_of_invalid_tokens = 0
    
    for token in tokens:
        if token != '':
            if machine.run_machine(token):
                number_of_accepted_tokens += 1
                resultado.write("\t{}\t\t\tACCEPTED\n".format(token))
            else:
                number_of_invalid_tokens += 1
                resultado.write("\t{}\t\t\tLEXICAL ERROR\n".format(token))
    
    resultado.write('\n------------------------------\n')
    resultado.write(f'Number of tokens analyzed: {number_of_accepted_tokens + number_of_invalid_tokens}\n')
    resultado.write(f'Number of accepted tokens: {number_of_accepted_tokens}\n')
    resultado.write(f'Number of invalid tokens: {number_of_invalid_tokens}\n')
    resultado.write('------------------------------\n')

    resultado.close()

def main(argv):
    check = True

    machine_file = ''
    input_file = ''
    output_file = ''

    try:
        opts, _ = getopt.getopt(argv, 'hm:i:o:', ['mfile=', 'ifile=', 'ofile='])
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

    str_input = read_input_file(input_file)
    
    while (check):
        choice = int(input("\nEscolha uma opção:\n1. Exit\n2. Execute a palavra no AFD\nDigite a sua escolha: "))
        if (choice == 1):
            sys.exit()
        elif (choice == 2):
            start_analysis(machine, str_input, output_file)
        else:
            check = False

if __name__ == "__main__":
    main(sys.argv[1:])
