from math import *
from scipy import stats

#Cette fonction calcule le prix et les greeks pour une call européenne avec le modèle de Black et Scholes (sj index)
def call_index_price_greeks_BS_model(stop, vol, rfr, lif, strp, divy):
    d1 = ((log(stop / strp)) + ((rfr - divy + ((vol**2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol*sqrt(lif))
    cdf11 = stats.norm.cdf(d1, loc = 0, scale = 1)
    cdf12 = stats.norm.cdf(d2, loc = 0, scale = 1)
    pdf11 = stats.norm.pdf(d1, loc = 0, scale = 1)
    price = (stop * exp(-divy*lif) * cdf11) - (strp * exp(-(rfr * lif)) * cdf12)
    delta = cdf11*exp(-divy*lif)
    gamma = (pdf11 *exp(-divy*lif)) / (stop * vol * sqrt(lif))
    vega = stop * sqrt(lif) * pdf11 * exp(-divy*lif)/ 100
    theta = ((-(stop * pdf11 * vol * exp(-divy*lif)) / (2 * sqrt(lif))) + (divy * stop * cdf11 * exp(-divy * lif)) - (rfr * strp * exp(-rfr * lif) * cdf12)) / 365
    rho = (strp * lif * exp(-rfr * lif) * cdf12) / 100
    return price, delta, gamma, vega, theta, rho

 #Cette fonction calcule le prix et les greeks pour un put européenne avec le modèle de Black et Scholes (sj index)
def put_index_price_greeks_BS_model(stop, vol, rfr, lif, strp, divy):
    d1 = ((log(stop / strp)) + ((rfr - divy + ((vol**2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol*sqrt(lif))
    cdf21 = stats.norm.cdf(-d1, loc = 0, scale = 1)
    cdf22 = stats.norm.cdf(-d2, loc = 0, scale = 1)
    pdf11 = stats.norm.pdf(d1, loc = 0, scale = 1)
    price = (strp * exp(-(rfr * lif)) * cdf22) - (stop * exp(-(divy*lif)) * cdf21)
    delta = -cdf21 * exp(-divy*lif)
    gamma = (pdf11 * exp(-divy*lif)) / (stop * vol * sqrt(lif))
    vega = stop * sqrt(lif) * pdf11 * exp(-divy * lif) /100
    theta = ((-(stop * pdf11 * vol * exp(-divy * lif)) / (2 * sqrt(lif))) - (divy*stop*cdf21*exp(-divy*lif)) + (rfr * strp * exp(-rfr * lif) * cdf22)) / 365
    rho = (-(strp * lif * exp(-rfr * lif) * cdf22)) / 100
    return price, delta, gamma, vega, theta, rho

