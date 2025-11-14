from math import sqrt, log, exp
from scipy import stats

#Cette fonction calcule le prix et les greeks pour une call européenne avec le modèle de Black et Scholes (sj currency)
def call_currency_price_greeks_BS_model(spot, vol, rfr, lif, strike, rfrf):
    d1 = ((log(spot / strike)) + ((rfr - rfrf + ((vol ** 2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol * sqrt(lif))
    cdf11 = stats.norm.cdf(d1, loc = 0, scale = 1)
    cdf12 = stats.norm.cdf(d2, loc = 0, scale = 1)
    pdf11 = stats.norm.pdf(d1, loc = 0, scale = 1)
    price = (spot * exp(-rfrf * lif) * cdf11) - (strike * exp(-(rfr * lif)) * cdf12)
    delta = cdf11*exp(-rfrf * lif)
    gamma = (pdf11 * exp(-rfrf * lif)) / (spot * vol * sqrt(lif))
    vega = spot * sqrt(lif) * pdf11 * exp(-rfrf * lif) / 100
    theta = ((-(spot * pdf11 * vol * exp(-rfrf * lif)) / (2 * sqrt(lif))) + (rfrf * spot * cdf11 * exp(-rfrf * lif)) - (rfr * strike * exp(-rfr * lif) * cdf12)) / 365
    rho = (strike * lif * exp(-rfr * lif) * cdf12) / 100
    return price, delta, gamma, vega, theta, rho

 #Cette fonction calcule le prix et les greeks pour un put européenne avec le modèle de Black et Scholes (sj currency)
def put_currency_price_greeks_BS_model(spot, vol, rfr, lif, strike, rfrf):
    d1 = ((log(spot / strike)) + ((rfr - rfrf + ((vol ** 2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol * sqrt(lif))
    cdf21 = stats.norm.cdf(-d1, loc = 0, scale = 1)
    cdf22 = stats.norm.cdf(-d2, loc = 0, scale = 1)
    pdf11 = stats.norm.pdf(d1, loc = 0, scale = 1)
    price = (strike * exp(-(rfr * lif)) * cdf22) - (spot * exp(-(rfrf * lif)) * cdf21)
    delta = -cdf21 * exp(-rfrf * lif)
    gamma = (pdf11 * exp(-rfrf * lif)) / (spot * vol * sqrt(lif))
    vega = spot * sqrt(lif) * pdf11 * exp(-rfrf * lif) / 100
    theta = ((-(spot * pdf11 * vol * exp(-rfrf * lif)) / (2 * sqrt(lif))) - (rfrf * spot * cdf21 * exp(-rfrf * lif)) + (rfr * strike * exp(-rfr * lif) * cdf22)) / 365
    rho = (-(strike * lif * exp(-rfr * lif) * cdf22)) / 100
    return price, delta, gamma, vega, theta, rho


