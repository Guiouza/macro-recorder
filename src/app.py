from os import getenv
from tkinter import Tk

# Controllers
from models import Macros
from controllers import MenuController


class App(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Macro Recorder")
        folder = getenv("APPDATA")
        if folder is None:
            raise FileNotFoundError
        folder += "/macro-recorder"
        self.macros = Macros(folder)
        self.menu_ctrl = MenuController(self, self.macros)


if __name__ == "__main__":
    app = App()
    app.mainloop()
