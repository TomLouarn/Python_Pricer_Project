"""
Module des courbes de taux zéro.

La classe `ZeroCurve` offre des méthodes pour interpoler des taux
spot/forward, calculer des facteurs d'actualisation et appliquer une
perturbation (shift) uniforme de la courbe.  Elle repose sur un
DataFrame qui contient une colonne 'DATE' en index et plusieurs
colonnes de taux (ESTER, EURIB1, EURIB3, etc.).  Par défaut, la
colonne 'GERMANY' est utilisée pour l'actualisation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union, Optional

import numpy as np
import pandas as pd
from scipy import interpolate


@dataclass
class ZeroCurve:
    """Courbe de taux zéro avec interpolation linéaire."""

    data: pd.DataFrame  # index = date string, colonnes = taux
    ref_col: str = 'GERMANY'

    def forward_rate(self, target_date: str) -> float:
        """Retourne le taux forward à la date cible par interpolation linéaire."""
        if target_date not in self.data.index:
            # interpolation entre les deux dates les plus proches
            dates = pd.to_datetime(self.data.index)
            target = pd.to_datetime(target_date)
            ords = (dates - dates[0]).days
            target_ord = (target - dates[0]).days
            f = interpolate.interp1d(ords, self.data[self.ref_col], fill_value="extrapolate")
            return float(f(target_ord))
        return float(self.data.loc[target_date, self.ref_col])

    def discount_factor(self, target_date: str) -> float:
        """Facteur d'actualisation pour la date cible (act/365).

        On suppose que la courbe fournit des taux annuels en %.  Le
        facteur d'actualisation est exp(−r × t), où t est le temps en
        années jusqu'à la date cible.
        """
        dates = pd.to_datetime(self.data.index)
        start = dates[0]
        target = pd.to_datetime(target_date)
        t = (target - start).days / 365
        rate = self.forward_rate(target_date) / 100
        return float(np.exp(-rate * t))

    def bump(self, bp: float) -> 'ZeroCurve':
        """Renvoie une nouvelle courbe avec un shift uniforme de bp (en %).

        Exemple : bp=0.0001 (1 bp) ajoutera 0.01 % aux taux.
        """
        bumped = self.data.copy()
        bumped[self.ref_col] = self.data[self.ref_col] + bp * 100
        return ZeroCurve(bumped, ref_col=self.ref_col)
