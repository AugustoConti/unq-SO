from threading import Thread
from time import sleep

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import TextArea


def show_full_screen(name, func):
    text_area = TextArea()
    kb = KeyBindings()

    @kb.add('c-c')
    @kb.add('q')
    def _(event):
        event.app.exit()

    application = Application(
        layout=Layout(container=text_area),
        key_bindings=kb,
        full_screen=True)

    Thread(target=application.run).start()
    while application.is_running:
        text_area.text = 'Press q to quit\n\n' + name + '\n' + func()
        sleep(0.3)
