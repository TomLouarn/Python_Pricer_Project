from tkinter import StringVar
from tkinter import ttk


class Label(ttk.Label):
    def __init__(self, tab):
        self.var = StringVar()
        super(Label, self).__init__(tab, self.var)

    def set(self, text):
        self.var.set(text)
