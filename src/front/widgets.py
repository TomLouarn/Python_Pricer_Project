from tkinter import StringVar, DoubleVar, IntVar
from tkinter import ttk
import pandas as pd


class Label(ttk.Label):
    def __init__(self, tab):
        self.var = StringVar()
        super(Label, self).__init__(tab, textvariable=self.var)

    def set(self, text):
        self.var.set(text)


class Entry(ttk.Entry):
    def __init__(self, tab):
        self.var = DoubleVar()
        super(Entry, self).__init__(tab, textvariable=self.var)

    def get(self):
        return self.var.get()

    def set(self, text):
        self.var.set(text)
    
    def grid(self, *args, **kwargs):
        super(Entry, self).grid(*args, **kwargs)
        return self


class Radiobutton():
    def __init__(self, tab, **kwargs):
        self.var = IntVar()
        self.store = {}

        for key, arg in kwargs.items():
            self.store[key] = ttk.Radiobutton(tab, variable=self.var, text=key, value=arg)
 
    def get(self):
        return self.var.get()
    
    def grid(self, *args, **kwargs):
        super(Radiobutton, self).grid(*args, **kwargs)
        return self


class Checkbutton(ttk.Checkbutton):
    def __init__(self, tab, text):
        self.var = IntVar()
        super(Checkbutton,self).__init__(tab, variable=self.var, text=text)
   
    def get(self):
        return self.var.get()

    def grid(self, *args, **kwargs):
        super(Checkbutton, self).grid(*args, **kwargs)
        return self
