"""
Swaps de taux d'intérêt pour le projet global.
Cette classe s'appuie sur `ZeroCurve` du module rates pour l'actualisation.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Tuple
from .rates import ZeroCurve


@dataclass
class InterestRateSwap:
    start_date: str
    end_date: str
    notional_fixed: float
    notional_float: float
    fixed_rate: float
    float_spread: float
    pay_fixed: bool
    freq_fixed: str
    freq_float: str
    daycount_fixed: int
    daycount_float: int
    curve: ZeroCurve
    def _generate_dates(self, freq: str) -> pd.DatetimeIndex:
        freq_to_months = {
            "Annual": 12,
            "Semi-Annual": 6,
            "Quarterly": 3,
            "Monthly": 1,
        }
        months = freq_to_months.get(freq, 12)
        start = datetime.fromisoformat(self.start_date).date()
        end = datetime.fromisoformat(self.end_date).date()
        months_total = (end.year - start.year) * 12 + (end.month - start.month)
        dates = [end - pd.DateOffset(months=i * months) for i in range(int(months_total / months) + 1)][::-1]
        adjusted = []
        for d in dates[1:]:
            d = d.to_pydatetime().date()
            while d.weekday() >= 5:
                d += timedelta(days=1)
            adjusted.append(d)
        return pd.DatetimeIndex(adjusted)
    def _payment_matrix(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        fixed_dates = self._generate_dates(self.freq_fixed)
        float_dates = self._generate_dates(self.freq_float)
        df_fixed = pd.DataFrame({
            'payment': fixed_dates,
        })
        df_fixed['year_frac'] = np.diff(
            [datetime.fromisoformat(self.start_date).date()] + list(df_fixed['payment'])
        ).astype('timedelta64[D]').astype(int) / self.daycount_fixed
        df_fixed['forward_rate'] = self.fixed_rate
        df_fixed['notional'] = self.notional_fixed
        df_float = pd.DataFrame({
            'payment': float_dates,
        })
        df_float['year_frac'] = np.diff(
            [datetime.fromisoformat(self.start_date).date()] + list(df_float['payment'])
        ).astype('timedelta64[D]').astype(int) / self.daycount_float
        forwards = []
        for d in df_float['payment']:
            fixing = d - timedelta(days=2)
            forwards.append(self.curve.forward_rate(fixing.strftime('%Y-%m-%d')))
        df_float['forward_rate'] = np.array(forwards) + self.float_spread
        df_float['notional'] = self.notional_float
        return df_fixed, df_float
    def price(self) -> float:
        df_fixed, df_float = self._payment_matrix()
        pv_fixed = 0.0
        pv_float = 0.0
        for _, row in df_fixed.iterrows():
            disc = self.curve.discount_factor(row['payment'].strftime('%Y-%m-%d'))
            pv_fixed += row['notional'] * row['forward_rate'] / 100 * row['year_frac'] * disc
        for _, row in df_float.iterrows():
            disc = self.curve.discount_factor(row['payment'].strftime('%Y-%m-%d'))
            pv_float += -row['notional'] * row['forward_rate'] / 100 * row['year_frac'] * disc
        return pv_fixed + pv_float
    def dv01(self) -> float:
        base_price = self.price()
        bump = 0.0001
        bumped_curve = self.curve.bump(bump)
        bumped_swap = InterestRateSwap(
            start_date=self.start_date,
            end_date=self.end_date,
            notional_fixed=self.notional_fixed,
            notional_float=self.notional_float,
            fixed_rate=self.fixed_rate,
            float_spread=self.float_spread,
            pay_fixed=self.pay_fixed,
            freq_fixed=self.freq_fixed,
            freq_float=self.freq_float,
            daycount_fixed=self.daycount_fixed,
            daycount_float=self.daycount_float,
            curve=bumped_curve,
        )
        return bumped_swap.price() - base_price