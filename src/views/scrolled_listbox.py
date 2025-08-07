from tkinter import Scrollbar, Listbox
from tkinter.ttk import Frame


class ScrolledListBox(Frame):
    def __init__(self, master) -> None:
        """Create ListBox and Scrollbar"""
        self.search_list = list()
        super().__init__(master)
        self.scrollbar = Scrollbar(self)
        self.listbox = Listbox(
            self, selectmode="browse", yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def get_selection(self) -> str | None:
        """Return selected item or None if no item is selected"""
        index = self.listbox.curselection()
        if index:
            return self.listbox.get(index[0])
        return None

    def update_list(self, text_list: list[str]) -> None:
        """Update the listbox with the given text list"""
        self.listbox.delete(0, "end")
        for text in text_list:
            self.listbox.insert("end", text)
        self.search_list = text_list.copy()
    
    def append(self, text: str) -> None:
        self.listbox.insert("end", text)
        self.search_list.append(text)
    
    def remove(self, text: str) -> None:
        index = self.search_list.index(text)
        self.listbox.delete(index)
        self.search_list.remove(text)
