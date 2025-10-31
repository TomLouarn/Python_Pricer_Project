from tkinter import Tk
from tkinter import ttk

from src.front.tabs import _BaseTab, OptionsCalculatorTab, MonteCarloTab, BondsCalculatorTab, SwapsCalculator, RatesCurve


handle_tab = {
    "Options calculator": OptionsCalculatorTab,
    "Monte Carlo": MonteCarloTab,
    "Bonds calculator": BondsCalculatorTab,
    "Swaps calculator": SwapsCalculator,
    "Rates Curve": RatesCurve,
}


class WindowMain(Tk):
    def __init__(
        self,
        size="1000x800",
        title="Options/Bonds/Swaps/Greeks Pricer and Monte Carlo Method"
    ):
        super(WindowMain, self).__init__()
        
        #Dimensionnement de la fenêtre (1000pixels de large par 800 de haut)
        self.geometry(size)

        #Ajout d'un titre à la fenêtre
        self.title(title)

        #Changement de la couleur de fond et les marges de la fenêtre
        self.configure(bg="#000000", padx=10, pady=10)

        self.notebook = ttk.Notebook(self)

    def get_tab(self, name, title=''):
        if name in handle_tab:
            return handle_tab[name](self.notebook)

        return _BaseTab(self.notebook, name, title)