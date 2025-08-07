from pathlib import Path
from time import sleep

from pyautogui import typewrite, moveTo
from pynput import mouse, keyboard


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


class Player():
    def __init__(self, file: Path):
        self.file = file
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()

    def load(self, value_to_increment: int, step: int):
        self.tasks = []
        with self.file.open() as file:
            for line in file:
                parts = line.strip().split(';')

                if parts[0] == 'increment':
                    self.tasks.append(self.__type_task(value_to_increment))
                    value_to_increment += step
                elif parts[0] == 'wait':
                    self.tasks.append(self.__wait_task(parts[1]))
                elif parts[0] == 'key':
                    self.tasks.append(self.__key_task(*parts[1:]))
                elif parts[0] == 'click':
                    self.tasks.append(self.__click_task(*parts[1:]))
                elif parts[0] == 'typewrite':
                    self.tasks.append(self.__type_task(parts[2]))
                elif parts[0] == 'command':
                    self.tasks.append(self.__command_task(*parts[1:]))
        return value_to_increment

    def start(self, fast_mode: bool, value_to_increment: int, step: int, repeat: int):
        self.fast_mode = fast_mode
        for n in range(repeat):
            value_to_increment = self.load(value_to_increment, step)
            for task in self.tasks:
                task()

    def __command_task(self, time, *keys):
        time = float(time)
        if self.fast_mode:
            if time < 0.3:
                time = 0.1
            else:
                time = 0.4

        def task():
            sleep(time)
            for key in keys:
                self.keyboard.press(parse_key(key))
            for key in keys:
                self.keyboard.release(parse_key(key))
        return task
    def __wait_task(self, time):
        return lambda: sleep(float(time))
    def __type_task(self, text):
        return lambda: typewrite(str(text))
    def __key_task(self, time, key, state):
        time = float(time)
        if self.fast_mode:
            if time < 0.3:
                time = 0.1
            else:
                time = 0.5
        key = parse_key(key)
        def press():
            sleep(time)
            self.keyboard.press(key)

        def release():
            sleep(time)
            self.keyboard.release(key)

        if state == 'True':
            return press
        return release
    def __click_task(self, time, x, y, button, state):
        time = float(time)
        if self.fast_mode:
            if time < 0.3:
                time = 0.1
            else:
                time = 0.5

        button = parse_button(button)
        def press():
            sleep(time)
            moveTo(int(x), int(y))
            self.mouse.press(button)

        def release():
            sleep(time)
            moveTo(int(x), int(y))
            self.mouse.release(button)

        if state == 'True':
            return press
        return release
