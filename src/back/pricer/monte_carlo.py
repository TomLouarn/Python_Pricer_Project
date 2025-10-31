"""
Module de simulation de Monte Carlo générique.

La classe `MonteCarloEngine` permet de simuler un processus log‑normal
ou de diffusion à sauts de Merton.  Elle fournit des méthodes pour
générer des trajectoires de prix et calculer le prix d'une option
européenne (call ou put) via l'estimation de Monte Carlo.  Le modèle
log‑normal est approprié pour la majorité des produits tandis que le
modèle de Merton intègre des sauts de Poisson.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Optional

import numpy as np
from scipy import stats  # type: ignore
import math


@dataclass
class MonteCarloEngine:
    spot: float
    volatility: float
    rate: float
    maturity: float
    strike: float
    dividend_yield: float = 0.0
    n_steps: int = 100
    n_paths: int = 10000
    seed: Optional[int] = None

    # paramètres de Merton (lambda, mu_j, sigma_j)
    jump_intensity: float = 0.0
    jump_mean: float = 0.0
    jump_vol: float = 0.0

    def _generate_paths(self) -> np.ndarray:
        rng = np.random.default_rng(self.seed)
        dt = self.maturity / self.n_steps
        drift = (self.rate - self.dividend_yield - 0.5 * self.volatility**2) * dt
        sigma_dt = self.volatility * math.sqrt(dt)
        paths = np.empty((self.n_paths, self.n_steps + 1))
        paths[:, 0] = self.spot
        for i in range(self.n_paths):
            for j in range(1, self.n_steps + 1):
                jump = 0.0
                if self.jump_intensity > 0:
                    # nombre de sauts sur dt
                    n_jumps = rng.poisson(self.jump_intensity * dt)
                    if n_jumps > 0:
                        jump = rng.normal(
                            loc=self.jump_mean * n_jumps,
                            scale=self.jump_vol * math.sqrt(n_jumps)
                        )
                z = rng.normal()
                paths[i, j] = paths[i, j - 1] * math.exp(drift + sigma_dt * z + jump)
        return paths

    def price_european(self, option_type: str = 'call') -> Tuple[float, float]:
        paths = self._generate_paths()
        payoffs = []
        for i in range(self.n_paths):
            final = paths[i, -1]
            if option_type == 'call':
                payoffs.append(max(final - self.strike, 0.0))
            else:
                payoffs.append(max(self.strike - final, 0.0))
        payoffs = np.array(payoffs)
        price = math.exp(-self.rate * self.maturity) * payoffs.mean()
        std_error = payoffs.std() / math.sqrt(self.n_paths)
        return float(price), float(std_error)
