from tkinter import Tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo, showerror

# Models
from models import Macros

# Widgets
from views.file_menu import FileMenu
from views.scrolled_listbox import ScrolledListBox


class MenuController:
    def __init__(self, window: Tk, macros_model: Macros) -> None:
        self.window = window
        self.macros = macros_model
        self.list_of_macros = ScrolledListBox(window)
        self.menu = FileMenu(window, self)
        self.list_of_macros.update_list(self.macros.get_all())
        self.create_widgets()

    def create_widgets(self) -> None:
        self.list_of_macros.pack(side="top", fill="both", expand=True)
        self.menu.pack(side="bottom", fill="x")

    def create(self) -> None:
        macro = askstring(
            "Create Macro", "Name:", parent=self.window, initialvalue="new_macro"
        )
        if macro is None or macro == "":
            return
        if self.macros.create(macro) is None:
            showerror("Macro Recorder", "Macro already exists")
            return
        self.list_of_macros.append(macro)

    def delete(self) -> None:
        macro = self.list_of_macros.get_selection()
        if macro is None:
            return
        if not self.macros.delete(macro):
            showerror("Macro Recorder", "Can't delete macro")
            return
        self.list_of_macros.remove(macro)

    def select(self) -> None:
        pass
