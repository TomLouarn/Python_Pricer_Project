"""
Module obligations pour le projet global.
Cette version reprend la classe `FixedRateBond` présentée dans la refonte.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd
import numpy_financial as npf
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


@dataclass
class FixedRateBond:
    principal: float
    coupon_rate: float
    issue_date: date
    maturity_date: date
    frequency: str
    curve: pd.DataFrame
    def _payment_schedule(self) -> pd.DataFrame:
        freq_to_months = {
            "Annual": 12,
            "Semi-Annual": 6,
            "Quarterly": 3,
            "Monthly": 1,
        }
        months = freq_to_months.get(self.frequency, 12)
        num_periods = int(((self.maturity_date.year - self.issue_date.year) * 12 + (self.maturity_date.month - self.issue_date.month)) / months)
        dates = [self.maturity_date - relativedelta(months=months * i) for i in range(num_periods + 1)][::-1]
        business_dates = []
        for dt in dates[1:]:
            while dt.weekday() >= 5:
                dt += timedelta(days=1)
            business_dates.append(dt)
        df = pd.DataFrame({
            'start': dates[:-1],
            'end': dates[1:],
            'payment': business_dates,
        })
        df['days'] = (df['end'] - df['start']).dt.days
        period = months / 12
        df['coupon'] = self.coupon_rate * period * self.principal / 100
        df.loc[df.index[-1], 'coupon'] += self.principal
        today = datetime.today().date()
        df['daycount'] = (df['payment'] - today).dt.days.clip(lower=0)
        return df
    def price(self) -> float:
        schedule = self._payment_schedule()
        zeros = []
        for dt in schedule['payment']:
            key = dt.strftime('%Y-%m-%d')
            zeros.append(self.curve.loc[key, 'GERMANY'])
        schedule['zero_rate'] = np.array(zeros)
        period = {
            "Annual": 1,
            "Semi-Annual": 0.5,
            "Quarterly": 0.25,
            "Monthly": 1 / 12,
        }[self.frequency]
        schedule['discount'] = 1 / (1 + (schedule['zero_rate'] * period / 100)) ** (schedule['daycount'] / (365 * period))
        schedule['pv'] = schedule['coupon'] * schedule['discount']
        price_pct = 100 * schedule['pv'].sum() / self.principal
        return float(price_pct)
    def ytm(self) -> float:
        schedule = self._payment_schedule()
        flows = 100 * schedule['coupon'] / self.principal
        flows = flows.tolist()
        price_pct = self.price()
        flows.insert(0, -price_pct)
        freq = {
            "Annual": 1,
            "Semi-Annual": 2,
            "Quarterly": 4,
            "Monthly": 12,
        }[self.frequency]
        irr = npf.irr(flows)
        return float(irr * freq * 100)
    def duration(self) -> Tuple[float, float]:
        schedule = self._payment_schedule()
        pv = []
        t = []
        freq = {
            "Annual": 1,
            "Semi-Annual": 2,
            "Quarterly": 4,
            "Monthly": 12,
        }[self.frequency]
        period = 1 / freq
        zeros = []
        for dt in schedule['payment']:
            zeros.append(self.curve.loc[dt.strftime('%Y-%m-%d'), 'GERMANY'])
        for i, row in schedule.iterrows():
            df = 1 / (1 + (zeros[i] / 100) / freq) ** (row['daycount'] * freq / 365)
            pv.append(row['coupon'] * df)
            t.append((i + 1) * period)
        pv = np.array(pv)
        t = np.array(t)
        price_pct = 100 * pv.sum() / self.principal
        macaulay = (pv * t).sum() / (price_pct / 100 * self.principal)
        modified = macaulay / (1 + self.ytm() / 100 / freq)
        return float(macaulay), float(modified)
    def convexity(self) -> float:
        schedule = self._payment_schedule()
        freq = {
            "Annual": 1,
            "Semi-Annual": 2,
            "Quarterly": 4,
            "Monthly": 12,
        }[self.frequency]
        period = 1 / freq
        zeros = []
        for dt in schedule['payment']:
            zeros.append(self.curve.loc[dt.strftime('%Y-%m-%d'), 'GERMANY'])
        pv = []
        convex = []
        for i, row in schedule.iterrows():
            df = 1 / (1 + (zeros[i] / 100) / freq) ** (row['daycount'] * freq / 365)
            pv_i = row['coupon'] * df
            pv.append(pv_i)
            t = (i + 1) * period
            convex.append(pv_i * t**2)
        price_pct = 100 * sum(pv) / self.principal
        return float(sum(convex) / (price_pct / 100 * self.principal))
    def dv01(self) -> float:
        price_base = self.price()
        bump = 0.0001
        bumped_curve = self.curve.copy()
        bumped_curve['GERMANY'] = self.curve['GERMANY'] + bump * 100
        bumped_bond = FixedRateBond(
            principal=self.principal,
            coupon_rate=self.coupon_rate,
            issue_date=self.issue_date,
            maturity_date=self.maturity_date,
            frequency=self.frequency,
            curve=bumped_curve,
        )
        price_bumped = bumped_bond.price()
        return float(price_bumped - price_base)