from typing import Literal
from pathlib import Path
from time import time

from pynput import mouse, keyboard
from pynput.keyboard import Key


MAX_TIME_TO_DOUBLE_CLICK = 0.3

STATES_TYPE = Literal['stopped', 'hotkey', 'typing', 'command', 'waiting']
ACTION_TYPES = Literal[
    'increment',
    'click',
    'key',
    'command',
    'wait',
    'typewrite'
]

def parse_button(button: str):
    if button == 'Button.left':
        return mouse.Button.left
    elif button == 'Button.right':
        return mouse.Button.right
    elif button == 'Button.middle':
        return mouse.Button.middle
    else:
        raise ValueError("Unknown mouse button: '{button}' ")

def parse_key(key: str):
    if key.startswith('Key.'):
        return eval(f'keyboard.Key.{key.removeprefix('Key.')}')
    elif key.startswith("'\\x"):
        index = int(key.removeprefix("'\\x").removesuffix("'"), 16) - 1
        letter = chr(ord('a') + index)
        return letter
    elif key.startswith("'"):
        return key[1]
    elif len(key) == 1:
        return key
    else:
        raise ValueError(f"Unknown mouse key: '{key}' ")

def delta_time():
    """Return the time passed until last call of delta_time"""
    last_time = time()
    yield 0
    while True:
        current_time = time()
        yield current_time - last_time
        last_time = current_time


class Action():
    def __init__(self, name: ACTION_TYPES, time: float, *args):
        self.name = name
        self.time = time
        self.args = args

    def __str__(self):
        return f'{self.name};{round(self.time, 2)};{";".join(map(str,self.args))}'

class Recorder():
    def __init__(self, file: Path) -> None:
        self.state: STATES_TYPE = 'stopped'
        self.file = file
        self.commands = list()
        self.type_list = list()
        self.queue = list()
        self.keyboard_listener = keyboard.Listener(
            on_press=self.__on_press,
            on_release=self.__on_release
        )
        self.mouse_listener = mouse.Listener(on_click=self.__on_click)

    def start(self):
        self.state = 'hotkey'
        self.queue = list() 
        self.time_generator = delta_time()
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop(self):
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.time_generator.close()
        self.state = 'stopped'
        if self.queue[-1].name == 'click':
            self.queue.pop() # remove last click: (click to stop)
            self.queue.pop()
        with self.file.open('w') as file:
            print(*self.queue, sep='\n', file=file)

    def __on_click(self, x, y, button, state):
        if self.state == 'waiting':
            self.__add_sleep()
            self.state = 'hotkey'
        if self.state == 'typing':
            if self.type_list:
                self.__add_typewrite()
            self.state = 'hotkey'

        self.__add_click(x, y, button, state)

    def __on_press(self, key):
        key = parse_key(str(key))
        if self.state == 'waiting':
            self.__add_sleep()
            self.state = 'hotkey'
        if self.state == 'typing':
            if key == Key.backspace:
                if self.type_list:
                    self.type_list.pop()
                else:
                    self.__add_typewrite()
                    self.__add_key(key, 'True')
            elif type(key) is str or key == Key.space: # se for um caracter
                if key == Key.space:
                    key = ' '
                self.type_list.append(key)
            else:
                self.__add_typewrite()
                self.__add_key(key, 'True')
            return
        if self.state == 'hotkey':
            if key == 't':
                self.state = 'typing'
                return
            if type(key) is not str:
                self.state = 'command'
        if self.state == 'command':
            if key not in self.commands:
                self.commands.append(key)

    def __on_release(self, key):
        key = parse_key(str(key))
        if self.state == 'typing':
            if type(key) is str or key == Key.space:
                return
            self.__add_typewrite()
            self.__add_key(key, 'False')
            if key == Key.esc:
                self.state = 'hotkey'
            return
        if self.state == 'hotkey':
            if key == 'i':
                self.__add_increment()
                return
            if key == 'w':
                self.state = 'waiting'
                self.__timer() # reset timer
                return
        if self.state == 'command':
            self.__add_command()
            self.commands.remove(key)
            if len(self.commands) == 0:
                self.state = 'hotkey'

    def __timer(self):
        return next(self.time_generator)
    def __add_increment(self):
        self.queue.append(Action('increment', self.__timer()))
    def __add_key(self, key, state):
        self.queue.append(Action('key', self.__timer(), key, state))
    def __add_typewrite(self):
        if len(self.type_list) == 0:
            return
        text = ''.join(map(str, self.type_list))
        self.type_list.clear()
        self.queue.append(Action('typewrite', self.__timer(), text))
    def __add_command(self):
        self.queue.append(Action('command', self.__timer(), *self.commands))
    def __add_click(self, x, y, button, state):
        self.queue.append(Action('click', self.__timer(), x, y, button, state))
    def __add_sleep(self):
        self.queue.append(Action('wait', self.__timer()))
