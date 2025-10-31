"""
Ce module reprend l’implémentation des options du package `pricer`.
Veuillez consulter `choix_conception.md` pour la justification détaillée
des choix de conception.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple

import numpy as np
from scipy import stats


class OptionType(Enum):
    CALL = "call"
    PUT = "put"


@dataclass
class BaseOption:
    spot: float
    strike: float
    maturity: float
    volatility: float
    rate: float
    dividend_yield: float
    option_type: OptionType

    def __post_init__(self) -> None:
        if self.spot <= 0:
            raise ValueError("Le prix du sous-jacent doit être positif.")
        if self.strike <= 0:
            raise ValueError("Le strike doit être positif.")
        if self.maturity <= 0:
            raise ValueError("La maturité doit être positive.")
        if self.volatility <= 0:
            raise ValueError("La volatilité doit être positive.")

    def _d1_d2(self) -> Tuple[float, float]:
        s, k, t, sigma, r, q = (
            self.spot,
            self.strike,
            self.maturity,
            self.volatility,
            self.rate,
            self.dividend_yield,
        )
        d1 = (
            math.log(s / k)
            + (r - q + 0.5 * sigma**2) * t
        ) / (sigma * math.sqrt(t))
        d2 = d1 - sigma * math.sqrt(t)
        return d1, d2

    def price(self) -> float:
        raise NotImplementedError

    def greeks(self) -> Dict[str, float]:
        raise NotImplementedError


@dataclass
class EuropeanOption(BaseOption):
    def price(self) -> float:
        d1, d2 = self._d1_d2()
        s, k, t, sigma, r, q = (
            self.spot,
            self.strike,
            self.maturity,
            self.volatility,
            self.rate,
            self.dividend_yield,
        )
        disc_r = math.exp(-r * t)
        disc_q = math.exp(-q * t)
        if self.option_type is OptionType.CALL:
            return disc_q * s * stats.norm.cdf(d1) - disc_r * k * stats.norm.cdf(d2)
        else:
            return disc_r * k * stats.norm.cdf(-d2) - disc_q * s * stats.norm.cdf(-d1)

    def greeks(self) -> Dict[str, float]:
        d1, d2 = self._d1_d2()
        s, k, t, sigma, r, q = (
            self.spot,
            self.strike,
            self.maturity,
            self.volatility,
            self.rate,
            self.dividend_yield,
        )
        disc_r = math.exp(-r * t)
        disc_q = math.exp(-q * t)
        pdf_d1 = stats.norm.pdf(d1)
        cdf_d1 = stats.norm.cdf(d1)
        cdf_d2 = stats.norm.cdf(d2)
        price = self.price()
        if self.option_type is OptionType.CALL:
            delta = disc_q * cdf_d1
        else:
            delta = disc_q * (cdf_d1 - 1)
        gamma = disc_q * pdf_d1 / (s * sigma * math.sqrt(t))
        vega = s * disc_q * pdf_d1 * math.sqrt(t) / 100
        term1 = -s * disc_q * pdf_d1 * sigma / (2 * math.sqrt(t))
        if self.option_type is OptionType.CALL:
            term2 = q * s * disc_q * cdf_d1
            term3 = -r * k * disc_r * cdf_d2
        else:
            term2 = -q * s * disc_q * stats.norm.cdf(-d1)
            term3 = r * k * disc_r * stats.norm.cdf(-d2)
        theta = (term1 + term2 + term3) / 365
        if self.option_type is OptionType.CALL:
            rho = k * t * disc_r * cdf_d2 / 100
        else:
            rho = -k * t * disc_r * stats.norm.cdf(-d2) / 100
        return {
            "price": price,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
        }


@dataclass
class AmericanOption(BaseOption):
    steps: int = 100
    def _tree_params(self) -> Tuple[float, float, float, float]:
        t, sigma, r, q = self.maturity, self.volatility, self.rate, self.dividend_yield
        dt = t / self.steps
        up = math.exp(sigma * math.sqrt(dt))
        down = 1.0 / up
        disc = math.exp((r - q) * dt)
        p = (disc - down) / (up - down)
        return up, down, disc, p
    def price(self) -> float:
        up, down, disc, p = self._tree_params()
        s0 = self.spot
        n = self.steps
        idx = np.arange(n + 1)
        spots = s0 * (up ** (n - idx)) * (down ** idx)
        if self.option_type is OptionType.CALL:
            values = np.maximum(spots - self.strike, 0.0)
        else:
            values = np.maximum(self.strike - spots, 0.0)
        for step in range(n - 1, -1, -1):
            values = disc * (p * values[:-1] + (1 - p) * values[1:])
            spots = s0 * (up ** (step - np.arange(step + 1))) * (down ** np.arange(step + 1))
            if self.option_type is OptionType.CALL:
                intrinsic = np.maximum(spots - self.strike, 0.0)
            else:
                intrinsic = np.maximum(self.strike - spots, 0.0)
            values = np.maximum(values, intrinsic)
        return float(values[0])
    def greeks(self) -> Dict[str, float]:
        eps_spot = 1e-2
        eps_rate = 1e-4
        eps_vol = 1e-4
        base_price = self.price()
        up_opt = self.__class__(
            spot=self.spot + eps_spot,
            strike=self.strike,
            maturity=self.maturity,
            volatility=self.volatility,
            rate=self.rate,
            dividend_yield=self.dividend_yield,
            option_type=self.option_type,
            steps=self.steps,
        ).price()
        down_opt = self.__class__(
            spot=self.spot - eps_spot,
            strike=self.strike,
            maturity=self.maturity,
            volatility=self.volatility,
            rate=self.rate,
            dividend_yield=self.dividend_yield,
            option_type=self.option_type,
            steps=self.steps,
        ).price()
        delta = (up_opt - down_opt) / (2 * eps_spot)
        gamma = (up_opt - 2 * base_price + down_opt) / (eps_spot**2)
        up_vol = self.__class__(
            spot=self.spot,
            strike=self.strike,
            maturity=self.maturity,
            volatility=self.volatility + eps_vol,
            rate=self.rate,
            dividend_yield=self.dividend_yield,
            option_type=self.option_type,
            steps=self.steps,
        ).price()
        vega = (up_vol - base_price) / eps_vol / 100
        up_rate = self.__class__(
            spot=self.spot,
            strike=self.strike,
            maturity=self.maturity,
            volatility=self.volatility,
            rate=self.rate + eps_rate,
            dividend_yield=self.dividend_yield,
            option_type=self.option_type,
            steps=self.steps,
        ).price()
        rho = (up_rate - base_price) / eps_rate / 100
        reduced = self.__class__(
            spot=self.spot,
            strike=self.strike,
            maturity=self.maturity - 1 / 365,
            volatility=self.volatility,
            rate=self.rate,
            dividend_yield=self.dividend_yield,
            option_type=self.option_type,
            steps=self.steps,
        ).price()
        theta = (reduced - base_price) * 365
        return {
            "price": base_price,
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho,
        }


@dataclass
class AsianOption(BaseOption):
    n_steps: int = 50
    n_simulations: int = 500
    random_seed: int = 42
    def price(self) -> float:
        rng = np.random.default_rng(self.random_seed)
        dt = self.maturity / self.n_steps
        drift = (self.rate - self.dividend_yield - 0.5 * self.volatility**2) * dt
        diffusion = self.volatility * math.sqrt(dt)
        payoffs = np.zeros(self.n_simulations)
        for i in range(self.n_simulations):
            path = np.empty(self.n_steps + 1)
            path[0] = self.spot
            for t in range(1, self.n_steps + 1):
                z = rng.normal()
                path[t] = path[t - 1] * math.exp(drift + diffusion * z)
            average_price = path.mean()
            if self.option_type is OptionType.CALL:
                payoffs[i] = max(average_price - self.strike, 0.0)
            else:
                payoffs[i] = max(self.strike - average_price, 0.0)
        return float(math.exp(-self.rate * self.maturity) * payoffs.mean())
    def greeks(self) -> Dict[str, float]:
        base_price = self.price()
        eps_spot = 1e-2
        eps_vol = 1e-4
        up_price = self.__class__(
            spot=self.spot + eps_spot,
            strike=self.strike,
            maturity=self.maturity,
            volatility=self.volatility,
            rate=self.rate,
            dividend_yield=self.dividend_yield,
            option_type=self.option_type,
            n_steps=self.n_steps,
            n_simulations=self.n_simulations,
            random_seed=self.random_seed,
        ).price()
        delta = (up_price - base_price) / eps_spot
        up_vol_price = self.__class__(
            spot=self.spot,
            strike=self.strike,
            maturity=self.maturity,
            volatility=self.volatility + eps_vol,
            rate=self.rate,
            dividend_yield=self.dividend_yield,
            option_type=self.option_type,
            n_steps=self.n_steps,
            n_simulations=self.n_simulations,
            random_seed=self.random_seed,
        ).price()
        vega = (up_vol_price - base_price) / eps_vol / 100
        return {
            "price": base_price,
            "delta": delta,
            "vega": vega,
        }


@dataclass
class BarrierOption(BaseOption):
    barrier: float
    n_steps: int = 100
    def price(self) -> float:
        t_step = self.maturity / self.n_steps
        n = math.log(self.barrier / self.spot) / (self.volatility * math.sqrt(t_step))
        nn = n / int(n) if n > 2 else n
        dx = nn * self.volatility * math.sqrt(t_step)
        disc = math.exp(-self.rate * t_step)
        u = self.rate - self.dividend_yield - 0.5 * self.volatility**2
        pu = 0.5 / (nn**2) + (u * math.sqrt(t_step)) / (2 * nn * self.volatility)
        pd = 0.5 / (nn**2) - (u * math.sqrt(t_step)) / (2 * nn * self.volatility)
        pm = 1 - 1 / (nn**2)
        pu_, pd_, pm_ = disc * pu, disc * pd, disc * pm
        spots = [0.0] * (2 * self.n_steps + 1)
        spots[0] = self.spot * math.exp(-self.n_steps * dx)
        exp_dx = math.exp(dx)
        for i in range(1, len(spots)):
            spots[i] = spots[i - 1] * exp_dx
        option = [[0.0, 0.0] for _ in range(len(spots))]
        T = self.n_steps % 2
        for i, s_t in enumerate(spots):
            if s_t >= self.barrier:
                option[i][T] = 0.0
            else:
                if self.option_type is OptionType.CALL:
                    option[i][T] = max(s_t - self.strike, 0.0)
                else:
                    option[i][T] = max(self.strike - s_t, 0.0)
        for t in range(self.n_steps - 1, -1, -1):
            current = t % 2
            next_ = (t + 1) % 2
            for i in range(self.n_steps - t, self.n_steps + t + 1):
                s_t = spots[i]
                if s_t >= self.barrier:
                    option[i][current] = 0.0
                else:
                    option[i][current] = (
                        pd_ * option[i - 1][next_]
                        + pm_ * option[i][next_]
                        + pu_ * option[i + 1][next_]
                    )
        return option[self.n_steps][0]
    def greeks(self) -> Dict[str, float]:
        base = self.price()
        eps_spot = 1e-2
        up = self.__class__(
            spot=self.spot + eps_spot,
            strike=self.strike,
            maturity=self.maturity,
            volatility=self.volatility,
            rate=self.rate,
            dividend_yield=self.dividend_yield,
            option_type=self.option_type,
            barrier=self.barrier,
            n_steps=self.n_steps,
        ).price()
        down = self.__class__(
            spot=self.spot - eps_spot,
            strike=self.strike,
            maturity=self.maturity,
            volatility=self.volatility,
            rate=self.rate,
            dividend_yield=self.dividend_yield,
            option_type=self.option_type,
            barrier=self.barrier,
            n_steps=self.n_steps,
        ).price()
        delta = (up - down) / (2 * eps_spot)
        gamma = (up - 2 * base + down) / (eps_spot**2)
        return {"price": base, "delta": delta, "gamma": gamma}