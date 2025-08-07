from pathlib import Path
from tkinter import Text
from tkinter.ttk import LabelFrame


class MacroDisplay(LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Commands")
        self.display = Text(
            self, borderwidth=1, relief="solid", bg="white", state='disabled'
        )
        self.create_widgets()

    def create_widgets(self):
        self.display.pack(side="top", fill="both", expand=True)

    def display_macro(self, macro: Path):
        self.display.config(state='normal')
        self.display.delete('1.0', 'end')
        with macro.open() as file:
            self.display.insert('end', file.read())
        self.display.config(state='disabled')
