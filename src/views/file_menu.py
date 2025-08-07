from tkinter import Button
from tkinter.ttk import Frame


class FileMenu(Frame):
    def __init__(self, master, controller) -> None:
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """Render file menu"""
        self.btn_create = Button(self, text="Create", command=self.controller.create)
        self.btn_delete = Button(self, text="Delete", command=self.controller.delete)
        self.btn_select = Button(self, text="Select", command=self.controller.select)
        self.btn_create.pack(side="left", fill="x", expand=True)
        self.btn_delete.pack(side="left", fill="x", expand=True)
        self.btn_select.pack(side="left", fill="x", expand=True)