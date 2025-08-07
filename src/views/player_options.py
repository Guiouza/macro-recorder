from typing import Tuple
from tkinter import (
    Toplevel, Frame, Label, Entry, Checkbutton, Button, BooleanVar, IntVar
)


class PlayerOption(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.fast_mode = BooleanVar(self, value=False)
        self.increment_from = IntVar(self, value=1)
        self.increment_by = IntVar(self, value=1)
        self.times = IntVar(self, value=1)
        self.result = None
        self.setup_dialog()
        self.create_widgets()

    def create_widgets(self):
        Button(self, text="play", command=self.on_ok, width=10).pack(side='bottom', pady=10)
        Checkbutton(self, text="Fast Mode", variable=self.fast_mode).pack()
        frame = Frame(self)
        frame.pack(padx=20)
        Label(frame, text="Increment from").pack(side='left')
        Entry(frame, textvariable=self.increment_from, width=3).pack(side='left')
        Label(frame, text="by").pack(side='left')
        Entry(frame, textvariable=self.increment_by, width=3).pack(side='left')
        Label(frame, text=",").pack(side='left')
        Entry(frame, textvariable=self.times, width=3).pack(side='left')
        Label(frame, text="times").pack(side='left')

    def setup_dialog(self):
        self.title("Player Options")
        self.grab_set()
        self.update_idletasks()
        self.resizable(False, False)

    def on_ok(self):
        self.result = (
            self.fast_mode.get(),
            self.increment_from.get(),
            self.increment_by.get(),
            self.times.get(),
        )
        self.destroy()


def askplayeroptions(parent) -> Tuple[bool, int, int, int] | None:
    dialog = PlayerOption(parent)
    # Variable to hold the result
    dialog.wait_window()
    return dialog.result
