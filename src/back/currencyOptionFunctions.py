from math import *
from scipy import stats

#Cette fonction calcule le prix et les greeks pour une call européenne avec le modèle de Black et Scholes (sj currency)
def call_currency_price_greeks_BS_model(spot, vol, rfr, T, strike, rfrf):
    d1 = ((log(spot / strike)) + ((rfr - rfrf + ((vol ** 2) / 2)) * T)) / (vol * sqrt(T))
    d2 = d1 - (vol * sqrt(T))
    cdf11 = stats.norm.cdf(d1, loc = 0, scale = 1)
    cdf12 = stats.norm.cdf(d2, loc = 0, scale = 1)
    pdf11 = stats.norm.pdf(d1, loc = 0, scale = 1)
    price = (spot * exp(-rfrf * T) * cdf11) - (strike * exp(-(rfr * T)) * cdf12)
    delta = cdf11*exp(-rfrf * T)
    gamma = (pdf11 * exp(-rfrf * T)) / (spot * vol * sqrt(T))
    vega = spot * sqrt(T) * pdf11 * exp(-rfrf * T) / 100
    theta = ((-(spot * pdf11 * vol * exp(-rfrf * T)) / (2 * sqrt(T))) + (rfrf * spot * cdf11 * exp(-rfrf * T)) - (rfr * strike * exp(-rfr * T) * cdf12)) / 365
    rho = (strike * T * exp(-rfr * T) * cdf12) / 100
    return price, delta, gamma, vega, theta, rho

 #Cette fonction calcule le prix et les greeks pour un put européenne avec le modèle de Black et Scholes (sj currency)
def put_currency_price_greeks_BS_model(spot, vol, rfr, T, strike, rfrf):
    d1 = ((log(spot / strike)) + ((rfr - rfrf + ((vol ** 2) / 2)) * T)) / (vol * sqrt(T))
    d2 = d1 - (vol * sqrt(T))
    cdf21 = stats.norm.cdf(-d1, loc = 0, scale = 1)
    cdf22 = stats.norm.cdf(-d2, loc = 0, scale = 1)
    pdf11 = stats.norm.pdf(d1, loc = 0, scale = 1)
    price = (strike * exp(-(rfr * T)) * cdf22) - (spot * exp(-(rfrf * T)) * cdf21)
    delta = -cdf21 * exp(-rfrf * T)
    gamma = (pdf11 * exp(-rfrf * T)) / (spot * vol * sqrt(T))
    vega = spot * sqrt(T) * pdf11 * exp(-rfrf * T) / 100
    theta = ((-(spot * pdf11 * vol * exp(-rfrf * T)) / (2 * sqrt(T))) - (rfrf * spot * cdf21 * exp(-rfrf * T)) + (rfr * strike * exp(-rfr * T) * cdf22)) / 365
    rho = (-(strike * T * exp(-rfr * T) * cdf22)) / 100
    return price, delta, gamma, vega, theta, rho


