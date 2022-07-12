import getopt, sys
from DFA import DFA

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
    print(max_token_length)
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

    afd = DFA.read_machine_file(machine_file)
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
