from termcolor import colored


def process_input(command_line):
    print(' processing command: ' + command_line)


def start_console():
    running = True
    while running:
        folder = ''
        command_line = input(
            colored('root', 'magenta') + '@' +
            colored('contillini', 'green') +
            colored(' ~' + folder + ' $', 'blue'))
        if command_line == 'exit':
            running = False
        else:
            process_input(command_line)
