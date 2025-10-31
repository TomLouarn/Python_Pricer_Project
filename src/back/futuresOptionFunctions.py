from math import *
from scipy import stats

 #Cette fonction calcule le prix et les greeks pour un call européenne avec le modèle de Black et Scholes (sj futures)
def call_futures_price_greeks_BS_model(stop, vol, rfr, lif, strp):
    d1 = ((log(stop/strp)) + ((rfr + ((vol**2)/2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol*sqrt(lif))
    phi1 = exp(-(d1**2 / 2)) / sqrt(2*pi)
    cdf11 = stats.norm.cdf(d1, loc = 0, scale = 1)
    cdf12 = stats.norm.cdf(d2, loc = 0, scale = 1)
    price = exp(-(rfr*lif))*((stop*cdf11)-(strp*cdf12))
    delta = exp(-rfr*lif)*cdf11
    gamma = exp(-rfr*lif)*phi1/(stop*vol*sqrt(lif))
    vega = exp(-rfr*lif)*stop*phi1*sqrt(lif)/100
    theta = (-((exp(-rfr*lif)*stop*phi1*vol)/(2*sqrt(lif)))+(rfr*stop*exp(-rfr*lif)*cdf11)-(rfr*strp*exp(-rfr*lif)*cdf12))/365
    rho = (-lif * price) / 100
    return price, delta, gamma, vega, theta, rho

 #Cette fonction calcule le prix et les greeks pour un put européenne avec le modèle de Black et Scholes (sj futures)
def put_futures_price_greeks_BS_model(stop, vol, rfr, lif, strp):
    d1 = ((log(stop/strp)) + ((rfr + ((vol**2)/2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol*sqrt(lif))
    phi1 = exp(-(d1**2 / 2)) / sqrt(2*pi)
    cdf1 = stats.norm.cdf(d1, loc = 0, scale = 1)
    cdf11 = stats.norm.cdf(-d1, loc = 0, scale = 1)
    cdf22 = stats.norm.cdf(-d2, loc = 0, scale = 1)
    price = exp(-(rfr*lif))*((strp*cdf22)-(stop*cdf11))
    delta = exp(-rfr*lif)*(cdf1-1)
    gamma = exp(-rfr*lif)*phi1/(stop*vol*sqrt(lif))
    vega = exp(-rfr*lif)*stop*phi1*sqrt(lif)/100
    theta = (-((exp(-rfr*lif)*stop*phi1*vol)/(2*sqrt(lif)))+(rfr*strp*exp(-rfr*lif)*cdf22)-(rfr*stop*exp(-rfr*lif)*cdf11))/365
    rho = (-lif * price) / 100
    return price, delta, gamma, vega, theta, rho

