from termcolor import colored


# TODO implementar comandos

def process_input(command_line):
    {
        'ls': ls,
        'mem': mem,
        'top': top,
        'pagetable': page_table,
        'help': ayuda,
    }[command_line]()
    print(' processing command: ' + command_line)


def ls():
    pass


def ps():
    pass


def mem():
    pass


def top():
    pass


def page_table():
    pass


def ayuda():
    pass


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
