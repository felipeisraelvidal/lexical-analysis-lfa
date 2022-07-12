import getopt, sys
from DFA import DFA
from helpers import *

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
    
    max_token_length = len(max(tokens, key=len))
    for token in tokens:
        if token != '':
            if machine.run_machine(token):
                number_of_accepted_tokens += 1
                resultado.write(f"\t{f'{token}':<{max_token_length + 5}}{'ACCEPTED'}\n")
            else:
                number_of_invalid_tokens += 1
                resultado.write(f"\t{f'{token}':<{max_token_length + 5}}{'LEXICAL ERROR'}\n")
    
    resultado.write('\n------------------------------\n')
    resultado.write(f'Number of tokens analyzed: {number_of_accepted_tokens + number_of_invalid_tokens}\n')
    resultado.write(f'Number of accepted tokens: {number_of_accepted_tokens}\n')
    resultado.write(f'Number of invalid tokens: {number_of_invalid_tokens}\n')
    resultado.write('------------------------------\n')

    resultado.close()

def main(argv):
    check = True

    machine_file = ''
    output_file = ''

    try:
        opts, _ = getopt.getopt(argv, 'hm:o:', ['mfile=', 'ofile='])
    except getopt.GetoptError:
        print('app.py -m <machinefile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('app.py -m <machinefile> -o <outputfile>')
            sys.exit()
        elif opt in ("-m", "--mfile"):
            machine_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    if machine_file == '' or output_file == '':
        print('Invalid machine file or output file')
        sys.exit()

    afd = DFA.read_machine_file(machine_file)
    machine = DFA(afd[0], afd[1], afd[2], afd[3], afd[4], afd[5])

    while (check):
        choice = int(input("\nMenu:\n1. Read text file\n2. Enter text\n3. Exit\nChoose an option: "))
        if (choice == 1):
            default_input_file_path = 'resources/input.txt'
            
            print('------------------------------------------------------------')
            print('Input file:')
            print_italic(f'Hint: you can use the existing file at \'{default_input_file_path}\'. Tap enter to use it.')
            
            input_file = input('path: ')
            if input_file == '':
                input_file = default_input_file_path
            
            print('------------------------------------------------------------')

            str_input = read_input_file(input_file)

            start_analysis(machine, str_input, output_file)
        elif (choice == 2):
            print('------------------------------------------------------------')
            print('Input text:')

            str_input = input('text: ')

            print('------------------------------------------------------------')

            start_analysis(machine, str_input, output_file)
        elif (choice == 3):
            sys.exit()
        else:
            check = False

if __name__ == "__main__":
    main(sys.argv[1:])
