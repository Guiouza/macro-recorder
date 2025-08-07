from tkinter import Label, Tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror

# Models
from models import Macros

# Widgets
from views.player_options import askplayeroptions
from views.macro_display import MacroDisplay
from views.file_menu import FileMenu
from views.scrolled_listbox import ScrolledListBox

# Services
from services.player import Player
from services.recorder import Recorder


class MenuController:
    @staticmethod
    def with_selection(method):
        """Get the macro_name of ScrolledListBox and pass it to the method.
        If nothing was selected quit without doing nothing"""

        def wrapper(self, *args, **kwargs):
            macro_name = self.list_of_macros.get_selection()
            if macro_name is None:
                print("No selection")
                return  # if not select do nothing
            return method(self, macro_name, *args, **kwargs)
        return wrapper

    def __init__(self, window: Tk, macros_model: Macros) -> None:
        self.window = window
        self.macros = macros_model
        self.list_of_macros = ScrolledListBox(window)
        self.menu = FileMenu(window, self)
        self.macro_display = MacroDisplay(window)
        self.list_of_macros.update_list(self.macros.get_all())
        self.list_of_macros.listbox.bind(
            "<<ListboxSelect>>", lambda e: self.select() # type: ignore
        ) # the parmetter is passed by the wrapper `with_slection`
        self.create_widgets()

    def create_widgets(self) -> None:
        self.menu.pack(side="bottom", fill="x")
        self.list_of_macros.pack(side="left", fill="both", expand=True)
        self.macro_display.pack(side="right", fill="both", expand=True)

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

    @with_selection
    def delete(self, macro: str) -> None:
        if not self.macros.delete(macro):
            showerror("Macro Recorder", "Can't delete macro")
            return
        self.list_of_macros.remove(macro)

    @with_selection
    def record(self, macro_name: str) -> None:
        macro = self.macros.search_by_name(macro_name)
        if macro is None:
            showerror("Macro Recorder", "Can't find macro")
            return
        self.recorder = Recorder(macro)
        self.recorder.start()
        self.menu.btn_record.config(text='Stop', command=self.stop_record)

    def stop_record(self):
        self.recorder.stop()
        self.menu.btn_record.config(
            text='Record', command=self.record # type: ignore
        ) # the parmetter is passed by the wrapper `with_slection`
        self.select() # type: ignore

    @with_selection
    def play(self, macro_name: str) -> None:
        macro = self.macros.search_by_name(macro_name)
        if macro is None:
            showerror("Macro Recorder", "Can't find macro")
            return
        self.player = Player(macro)
        result = askplayeroptions(self.window)
        if result is None:
            return
        self.player.start(*result)

    @with_selection
    def select(self, macro_name: str) -> None:
        macro = self.macros.search_by_name(macro_name)
        if macro is None:
            showerror("Macro Recorder", "Can't find macro")
            return
        self.macro_display.display_macro(macro)
