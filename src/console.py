def process_input(command_line):
    print(' processing command: ' + command_line)


def start_console():
    running = True
    while running:
        command_line = input("$ ")
        if command_line == 'exit':
            running = False
        else:
            process_input(command_line)
