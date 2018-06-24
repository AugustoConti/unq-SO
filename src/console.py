from termcolor import colored


# TODO COMANDOS: ls, ps -a, mem, mostrame la memoria, tabla de paginas

def process_input(command_line):
    print(' processing command: ' + command_line)


def read():
    folder = ''
    user = '{u}@{pc} {f} '.format(u=colored('root', 'magenta'), pc=colored('contillini', 'green'),
                                  f=colored('~{f} $'.format(f=folder), 'blue'))
    return input(user)


def start_console():
    command_line = read()
    while command_line != 'exit':
        process_input(command_line)
        command_line = read()
