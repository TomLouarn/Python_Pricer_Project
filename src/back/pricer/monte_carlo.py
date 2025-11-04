"""
Module de simulation de Monte Carlo générique.

La classe `MonteCarloEngine` permet de simuler un processus log‑normal
ou de diffusion à sauts de Merton.  Elle fournit des méthodes pour
générer des trajectoires de prix et calculer le prix d'une option
européenne (call ou put) via l'estimation de Monte Carlo.  Le modèle
log‑normal est approprié pour la majorité des produits tandis que le
modèle de Merton intègre des sauts (processus de Poisson composé de sauts
log-normaux). Le drift est compensé chez Merton pour garantir la neutralité
au risque
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Optional
import numpy as np
import math


@dataclass
class MonteCarloEngine:
    spot: float = 100.0
    volatility: float = 0.25
    rate: float = 0.02
    maturity: float = 1.0
    strike: float = 100.0
    dividend_yield: float = 0.04
    n_steps: int = 100
    n_paths: int = 10000
    seed: Optional[int] = None

    # paramètres de Merton (fja, avgm, jvol)
    jump_intensity: float = 0.0
    jump_mean: float = 0.0
    jump_vol: float = 0.0

    def _risk_neutral_drift_dt(self) -> float:
        """
        Drift par pas (log-prix) sous Q, avec compensation de saut si Merton.

        Pour GBM : (r - q - 0.5*sigma^2)*dt
        Pour Merton:  (r - q - 0.5*sigma^2 - λ*k)*dt, k = E[e^J]-1 = exp(μ_j + 0.5 σ_j^2) - 1
        """

        dt = self.maturity / self.n_steps
        base = self.rate - self.dividend_yield - 0.5 * self.volatility ** 2
        if self.jump_intensity > 0:
            k = math.exp(self.jump_mean + 0.5 * self.jump_vol ** 2)-1
            return (base - self.jump_intensity*k)*dt
        return base * dt

    def _generate_paths(self) -> np.ndarray:
        """
        Génère des trajectoires sous-jacentes (vectorisé).

        Vectorisation complète:
        - on applique d'un coup tous les chocs browniens Z ~ N(0,1)
        - si λ>0, on applique tous les nombres de sauts N ~ Poisson(λ*dt)
          et les chocs de saut agrégés J ~ Normal(μ_j*N, σ_j*sqrt(N))
        - on additionne drift + sigma*sqrt(dt)*Z + J sur tous les pas
        - on cumule (cumsum) sur l'axe temps (log-returns) puis on exponentielle
        """
        rng = np.random.default_rng(self.seed)

        dt = self.maturity / self.n_steps
        drift = self._risk_neutral_drift_dt
        sigma_dt = self.volatility * math.sqrt(dt)

        # 1) Bruit brownien (tous les tirages d'un coup)
        Z = rng.standard_normal((self.n_paths, self.n_steps))

        # 2) Terme de saut agrégé par pas (J) si λ>0
        if self.jump_intensity > 0.0:
            lam_dt = self.jump_intensity * dt
            N = rng.poisson(lam=lam_dt, size=(self.n_paths, self.n_steps))  # nb de sauts sur chaque dt
            # somme de N Normaux(μ_j, σ_j^2) ~ Normal( N*μ_j, N*σ_j^2 )
            # donc J = μ_j*N + σ_j*sqrt(N)*Z_j
            sqrtN = np.sqrt(N, dtype=float)
            Zj = rng.standard_normal((self.n_paths, self.n_steps))
            J = self.jump_mean * N + self.jump_vol * sqrtN * Zj
        else:
            J = 0.0

        # 3) Incréments du log-prix: drift + sigma*sqrt(dt)*Z + J
        log_increments = drift + sigma_dt * Z + J

        # 4) Cumul temporel des log-returns
        log_paths = np.cumsum(log_increments, axis=1)
        # S_t = S_0 * exp(log_paths)
        S = self.spot * np.exp(log_paths)
        # prépend S0 comme colonne 0
        S0 = np.full((self.n_paths, 1), self.spot, dtype=float)

        return np.concatenate([S0, S], axis=1)

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