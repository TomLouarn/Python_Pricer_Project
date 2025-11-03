from math import *
from scipy import stats
import random


#Cette fonction calcule la volatilité implicite pour un call avec le modèle Black et Scholes
def call_implied_volatility_BS(spot, strp, rfr, lif, prio, stav):
    dVol = 0.0000001
    epsilon = 0.0000001
    maxIter = 1000
    vol_1 = stav
    i = 1
    while True:
        Value_1 = call_price_greeks_BS_model(spot, vol_1, rfr, lif, strp)[0]
        vol_2 = vol_1 - dVol
        Value_2 = call_price_greeks_BS_model(spot, vol_2, rfr, lif, strp)[0]
        dx = (Value_2 - Value_1) / dVol
        if abs(dx) < epsilon or i == maxIter: break
        vol_1 = vol_1 - (prio - Value_1) / dx
        i = i + 1   
    return vol_1
   
#Cette fonction calcule la volatilité implicite pour un put avec le modèle Black et Scholes (sj equity)
def put_implied_volatility_BS(spot, strp, rfr, lif, prio, stav):
    dVol = 0.0000001
    epsilon = 0.0000001
    maxIter = 1000
    vol_1 = stav
    i = 1
    while True:
        Value_1 = put_price_greeks_BS_model(spot, vol_1, rfr, lif, strp)[0]
        vol_2 = vol_1 - dVol
        Value_2 = put_price_greeks_BS_model(spot, vol_2, rfr, lif, strp)[0]
        dx = (Value_2 - Value_1) / dVol
        if abs(dx) < epsilon or i == maxIter: break
        vol_1 = vol_1 - (prio - Value_1) / dx
        i = i + 1    
    return vol_1


#Cette fonction calcule le prix pour une call européenne avec le modèle de Black et Scholes (sj equity)
def call_price_BS_model(spot, vol, rfr, lif, strp):
    d1 = ((log(spot / strp)) + ((rfr + ((vol ** 2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol*sqrt(lif))
    cdf11 = stats.norm.cdf(d1, loc = 0, scale = 1)
    cdf12 = stats.norm.cdf(d2, loc = 0, scale = 1)
    price = (spot * cdf11) - (strp * exp(-(rfr * lif)) * cdf12)
    return price

 #Cette fonction calcule le prix pour un put européenne avec le modèle de Black et Scholes (sj equity)
def put_price_BS_model(spot, vol, rfr, lif, strp):
    d1 = ((log(spot / strp)) + ((rfr + ((vol ** 2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol*sqrt(lif))
    cdf22 = stats.norm.cdf(-d2, loc = 0, scale = 1)
    cdf1 = stats.norm.cdf(-d1, loc = 0, scale = 1)
    price = strp * exp(-(rfr * lif)) * cdf22 - (spot * cdf1)
    return price

 #Cette fonction calcule le prix et les greeks pour un call européenne avec le modèle de Black et Scholes (sj equity)
def call_price_greeks_BS_model(spot, vol, rfr, lif, strp):
    d1 = ((log(spot / strp)) + ((rfr + ((vol ** 2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol*sqrt(lif))
    phi1 = exp(-(d1**2 / 2)) / sqrt(2*pi)
    cdf11 = stats.norm.cdf(d1, loc = 0, scale = 1)
    cdf12 = stats.norm.cdf(d2, loc = 0, scale = 1)
    price = (spot * cdf11) - (strp * exp(-(rfr * lif)) * cdf12)
    delta = cdf11
    gamma = phi1 / (spot * vol * sqrt(lif))
    vega = spot * phi1 * sqrt(lif) / 100
    theta = (-((spot * phi1 * vol) / (2 * sqrt(lif))) - (rfr * strp * exp(-rfr * lif) * cdf12)) / 365
    rho = (strp * lif * exp(-rfr * lif) * cdf12) / 100
    return price, delta, gamma, vega, theta, rho

 #Cette fonction calcule le prix et les greeks pour un put européenne avec le modèle de Black et Scholes (sj equity)
def put_price_greeks_BS_model(spot, vol, rfr, lif, strp):
    d1 = ((log(spot / strp)) + ((rfr + ((vol ** 2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol*sqrt(lif))
    phi1 = exp(-(d1**2 / 2)) / sqrt(2*pi)
    cdf11 = stats.norm.cdf(d1, loc = 0, scale = 1)
    cdf22 = stats.norm.cdf(-d2, loc = 0, scale = 1)
    cdf1 = stats.norm.cdf(-d1, loc = 0, scale = 1)
    price = strp * exp(-(rfr * lif)) * cdf22 - (spot * cdf1)
    delta = cdf11-1
    gamma = phi1 / (spot * vol * sqrt(lif))
    vega = spot * phi1 * sqrt(lif) / 100
    theta = (-((spot * phi1 * vol) / (2 * sqrt(lif))) + (rfr * strp * exp(-rfr * lif) * cdf22)) / 365
    rho = (-strp * lif * exp(-rfr * lif) * cdf22) / 100
    return price, delta, gamma, vega, theta, rho


####################################################################### Binomial models ##########################################################################


#Cette fonction calcule le prix d'un call européenne avec le modèle Binomial (sj equity)
def call_price_binomial_european_model(spot, vol, rfr, lif, strp, niter):
    up = exp(vol*sqrt(lif/niter))
    down = 1/up
    prob = (exp(rfr*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_ = 1-prob #probabilité d'un mouvement de baisse
    res = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'tableau'
        res.append(spot * (down ** i) * (up ** (niter - i)))
        if res[i] < strp:
            res[i] = 0
        else:
            res[i] = res[i] - strp
    timeStep = lif/niter
    for i in range(1,(niter+1)):
        for j in range((niter+1)-i):
            res[j] = exp((-rfr)*timeStep)*(prob*res[j]+prob_*res[j+1])
    price = res[0]
    return price
    
#Cette fonction calcule le prix d'un put européenne avec le modèle Binomial (sj equity)
def put_price_binomial_european_model(spot, vol, rfr, lif, strp, niter):
    up = exp(vol*sqrt(lif/niter))
    down = 1/up
    prob = (exp(rfr*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_ = 1-prob #probabilité d'un mouvement de baisse
    res = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'tableau'
        res.append(spot * (down ** i) * (up ** (niter - i)))
        if res[i] > strp:
            res[i] = 0
        else:
            res[i] = strp - res[i]
    timeStep = lif/niter
    for i in range(1,(niter+1)):
        for j in range((niter+1)-i):
            res[j] = exp((-rfr)*timeStep)*(prob*res[j]+prob_*res[j+1])
    price = res[0]
    return price

#Cette fonction calcule les greeks d'un call européenne avec le modèle Binomial (sj equity)
def call_greeks_binomial_european_model(spot, vol, rfr, lif, strp, niter):
    vol2 = vol + 0.01
    rfr2 = rfr + 0.01
    up = exp(vol*sqrt(lif/niter))
    down = 1/up
    prob = (exp(rfr*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_ = 1-prob #probabilité d'un mouvement de baisse
    res = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'res'
        res.append(spot * (down ** i) * (up ** (niter - i)))
        if res[i] < strp:
            res[i] = 0
        else:
            res[i] = res[i] - strp
    #Lorsque la volatilité varie de +1% (pour le calcul de vega)
    up2 = exp(vol2*sqrt(lif/niter))
    down2 = 1/up2
    prob2 = (exp(rfr*lif/niter)-down2)/(up2-down2) #probabilité d'un mouvement de hausse
    prob_2 = 1-prob2 #probabilité d'un mouvement de baisse
    res2 = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'res2'
        res2.append(spot * (down2 ** i) * (up2 ** (niter - i)))
        if res2[i] < strp:
            res2[i] = 0
        else:
            res2[i] = res2[i] - strp
    #Lorsque le taux sans risque varie de +1% (pour le calcul de rho):
    prob3 = (exp(rfr2*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_3 = 1-prob3 #probabilité d'un mouvement de baisse
    timeStep = lif/niter #le pas d'itération
    res3 = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'tableau3' lorsque le taux sans risque varie de 1%
        res3.append(res[i])
    
    for i in range(1,niter+1): #Boucle qui détermine le prix initial de l'option d'achat (backward-looking)
        for j in range(niter+1-i):
            res[j] = exp((-rfr)*timeStep)*(prob*res[j]+prob_*res[j+1])
            if i == niter - 1 and j == 0:
                fu = res[0]
            elif i == niter - 1 and j == 1: 
                fd = res[1]
            elif i == niter - 2 and j == 0:
                fuu = res[0]
            elif i == niter - 2 and j == 1:
                fud = res[1]
            elif i == niter - 2 and j == 2:
                fdd = res[2]
            res2[j]=exp((-rfr) * timeStep) * (prob2 * res2[j] + prob_2 * res2[j + 1])
            res3[j]=exp((-rfr2) * timeStep) * (prob3 * res3[j] + prob_3 * res3[j + 1])
    delta = (fu - fd) / ((spot * up) - (spot * down))
    gamma = (((fuu - fud) / (spot * up * up - spot * up * down)) - ((fud - fdd) / (spot * up * down - spot * down * down))) / ((spot * up * up - spot * down * down) / 2)
    vega = res2[0] - res[0]
    theta = (fud - res[0]) / (2 * lif * 365 / niter)
    rho = res3[0] - res[0]
    return delta, gamma, vega, theta, rho

#Cette fonction calcule les greeks d'un put européenne avec le modèle Binomial (sj equity)
def put_greeks_binomial_european_model(spot, vol, rfr, lif, strp, niter):
    vol2 = vol + 0.01
    rfr2 = rfr + 0.01
    up = exp(vol*sqrt(lif/niter))
    down = 1/up
    prob = (exp(rfr*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_ = 1-prob #probabilité d'un mouvement de baisse
    res = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'res'
        res.append(spot * (down ** i) * (up ** (niter - i)))
        if res[i] > strp:
            res[i] = 0
        else:
            res[i] = strp - res[i]
    #Lorsque la volatilité varie de +1% (pour le calcul de vega)
    up2 = exp(vol2*sqrt(lif/niter))
    down2 = 1/up2
    prob2 = (exp(rfr*lif/niter)-down2)/(up2-down2) #probabilité d'un mouvement de hausse
    prob_2 = 1-prob2 #probabilité d'un mouvement de baisse
    res2 = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'res2'
        res2.append(spot * (down2 ** i) * (up2 ** (niter - i)))
        if res2[i] > strp:
            res2[i] = 0
        else:
            res2[i] = strp - res2[i]
    #Lorsque le taux sans risque varie de +1% (pour le calcul de rho):
    prob3 = (exp(rfr2*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_3 = 1-prob3 #probabilité d'un mouvement de baisse
    timeStep = lif/niter #le pas d'itération
    res3 = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'tableau3' lorsque le taux sans risque varie de 1%
        res3.append(res[i])
    
    for i in range(1,niter+1): #Boucle qui détermine le prix initial de l'option d'achat (backward-looking)
        for j in range(niter+1-i):
            res[j] = exp((-rfr)*timeStep)*(prob*res[j]+prob_*res[j+1])
            if i == niter - 1 and j == 0:
                fu = res[0]
            elif i == niter - 1 and j == 1: 
                fd = res[1]
            elif i == niter - 2 and j == 0:
                fuu = res[0]
            elif i == niter - 2 and j == 1:
                fud = res[1]
            elif i == niter - 2 and j == 2:
                fdd = res[2]
            res2[j]=exp((-rfr) * timeStep) * (prob2 * res2[j] + prob_2 * res2[j + 1])
            res3[j]=exp((-rfr2) * timeStep) * (prob3 * res3[j] + prob_3 * res3[j + 1])
    delta = (fu - fd) / ((spot * up) - (spot * down))
    gamma = (((fuu - fud) / (spot * up * up - spot * up * down)) - ((fud - fdd) / (spot * up * down - spot * down * down))) / ((spot * up * up - spot * down * down) / 2)
    vega = res2[0] - res[0]
    theta = (fud - res[0]) / (2 * lif * 365 / niter)
    rho = res3[0] - res[0]
    #res_B_greeks = [delta, gamma, vega, theta, rho]
    #return res_B_greeks
    return delta, gamma, vega, theta, rho

#Cette fonction calcule le prix d'un call american avec le modèle Binomial (sj equity)
def call_price_binomial_american_model(spot, vol, rfr, lif, strp, niter):
    up = exp(vol*sqrt(lif/niter))
    down = 1/up
    prob = (exp(rfr*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_ = 1-prob #probabilité d'un mouvement de baisse
    res = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'tableau'
        res.append(spot * (down ** i) * (up ** (niter - i)))
        if res[i] < strp:
            res[i] = 0
        else:
            res[i] = res[i] - strp
    timeStep = lif/niter
    for i in range(1,niter+1):
        for j in range(niter+1-i):
            res[j] = exp((-rfr)*timeStep)*(prob*res[j]+prob_*res[j+1])
            if res[j] < (spot * (up ** (niter - i - j)) * (down ** j)) - strp:
                 res[j] = (spot * (up ** (niter - i - j)) * (down ** j)) - strp
    price = res[0]
    return price

#Cette fonction calcule le prix d'un put american avec le modèle Binomial (sj equity)
def put_price_binomial_american_model(spot, vol, rfr, lif, strp, niter):
    up = exp(vol*sqrt(lif/niter))
    down = 1/up
    prob = (exp(rfr*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_ = 1-prob #probabilité d'un mouvement de baisse
    res = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'tableau'
        res.append(spot * (down ** i) * (up ** (niter - i)))
        if res[i] > strp:
            res[i] = 0
        else:
            res[i] = strp - res[i]
    timeStep = lif/niter
    for i in range(1,(niter+1)):
        for j in range((niter+1)-i):
            res[j] = exp((-rfr) * timeStep) * (prob * res[j] + prob_ * res[j+1])
            if res[j] < strp - (spot * (up ** (niter - i - j)) * (down ** j)):
                 res[j] = strp - (spot * (up ** (niter - i - j)) * (down ** j))
    price = res[0]
    return price

#Cette fonction calcule les greeks d'un call american avec le modèle Binomial (sj equity)
def call_greeks_binomial_american_model(spot, vol, rfr, lif, strp, niter):
    vol2 = vol + 0.01
    rfr2 = rfr + 0.01
    up = exp(vol*sqrt(lif/niter))
    down = 1/up
    prob = (exp(rfr*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_ = 1-prob #probabilité d'un mouvement de baisse
    res = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'res'
        res.append(spot * (down ** i) * (up ** (niter - i)))
        if res[i] < strp:
            res[i] = 0
        else:
            res[i] = res[i] - strp
    #Lorsque la volatilité varie de +1% (pour le calcul de vega)
    up2 = exp(vol2*sqrt(lif/niter))
    down2 = 1/up2
    prob2 = (exp(rfr*lif/niter)-down2)/(up2-down2) #probabilité d'un mouvement de hausse
    prob_2 = 1-prob2 #probabilité d'un mouvement de baisse
    res2 = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'res2'
        res2.append(spot * (down2 ** i) * (up2 ** (niter - i)))
        if res2[i] < strp:
            res2[i] = 0
        else:
            res2[i] = res2[i] - strp
    #Lorsque le taux sans risque varie de +1% (pour le calcul de rho):
    prob3 = (exp(rfr2*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_3 = 1-prob3 #probabilité d'un mouvement de baisse
    timeStep = lif/niter #le pas d'itération
    res3 = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'tableau3' lorsque le taux sans risque varie de 1%
        res3.append(res[i])
    
    for i in range(1,niter+1): #Boucle qui détermine le prix initial de l'option d'achat (backward-looking)
        for j in range(niter+1-i):
            res[j] = exp((-rfr)*timeStep)*(prob*res[j]+prob_*res[j+1])
            if res[j] < (spot * (up ** (niter - i - j)) * (down ** j)) - strp:
                 res[j] = (spot * (up ** (niter - i - j)) * (down ** j)) - strp
            if i == niter - 1 and j == 0:
                fu = res[0]
            elif i == niter - 1 and j == 1: 
                fd = res[1]
            elif i == niter - 2 and j == 0:
                fuu = res[0]
            elif i == niter - 2 and j == 1:
                fud = res[1]
            elif i == niter - 2 and j == 2:
                fdd = res[2]
            res2[j]=exp((-rfr) * timeStep) * (prob2 * res2[j] + prob_2 * res2[j + 1])
            if res2[j] < (spot * (up ** (niter - i - j)) * (down ** j)) - strp:
                 res2[j] = (spot * (up ** (niter - i - j)) * (down ** j)) - strp
            res3[j]=exp((-rfr2) * timeStep) * (prob3 * res3[j] + prob_3 * res3[j + 1])
            if res3[j] < (spot * (up ** (niter - i - j)) * (down ** j)) - strp:
                 res3[j] = (spot * (up ** (niter - i - j)) * (down ** j)) - strp
    delta = (fu - fd) / ((spot * up) - (spot * down))
    gamma = (((fuu - fud) / (spot * up * up - spot * up * down)) - ((fud - fdd) / (spot * up * down - spot * down * down))) / ((spot * up * up - spot * down * down) / 2)
    vega = res2[0] - res[0]
    theta = (fud - res[0]) / (2 * lif * 365 / niter)
    rho = res3[0] - res[0]
    return delta, gamma, vega, theta, rho

#Cette fonction calcule les greeks d'un put american avec le modèle Binomial (sj equity)
def put_greeks_binomial_american_model(spot, vol, rfr, lif, strp, niter):
    vol2 = vol + 0.01
    rfr2 = rfr + 0.01
    up = exp(vol*sqrt(lif/niter))
    down = 1/up
    prob = (exp(rfr*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_ = 1-prob #probabilité d'un mouvement de baisse
    res = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'res'
        res.append(spot * (down ** i) * (up ** (niter - i)))
        if res[i] > strp:
            res[i] = 0
        else:
            res[i] = strp - res[i]
    #Lorsque la volatilité varie de +1% (pour le calcul de vega)
    up2 = exp(vol2*sqrt(lif/niter))
    down2 = 1/up2
    prob2 = (exp(rfr*lif/niter)-down2)/(up2-down2) #probabilité d'un mouvement de hausse
    prob_2 = 1-prob2 #probabilité d'un mouvement de baisse
    res2 = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'res2'
        res2.append(spot * (down2 ** i) * (up2 ** (niter - i)))
        if res2[i] > strp:
            res2[i] = 0
        else:
            res2[i] = strp - res2[i]
    #Lorsque le taux sans risque varie de +1% (pour le calcul de rho):
    prob3 = (exp(rfr2*lif/niter)-down)/(up-down) #probabilité d'un mouvement de hausse
    prob_3 = 1-prob3 #probabilité d'un mouvement de baisse
    timeStep = lif/niter #le pas d'itération
    res3 = []
    for i in range(niter+1): #Boucle qui stocke les valeurs finales de l'arbre binomial dans 'tableau3' lorsque le taux sans risque varie de 1%
        res3.append(res[i])
    
    for i in range(1,niter+1): #Boucle qui détermine le prix initial de l'option d'achat (backward-looking)
        for j in range(niter+1-i):
            res[j] = exp((-rfr) * timeStep) * (prob * res[j] + prob_ * res[j+1])
            if res[j] < strp - (spot * (up ** (niter - i - j)) * (down ** j)):
                 res[j] = strp - (spot * (up ** (niter - i - j)) * (down ** j))
            if i == niter - 1 and j == 0:
                fu = res[0]
            elif i == niter - 1 and j == 1: 
                fd = res[1]
            elif i == niter - 2 and j == 0:
                fuu = res[0]
            elif i == niter - 2 and j == 1:
                fud = res[1]
            elif i == niter - 2 and j == 2:
                fdd = res[2]
            res2[j]=exp((-rfr) * timeStep) * (prob2 * res2[j] + prob_2 * res2[j + 1])
            if res2[j] < strp - (spot * (up ** (niter - i - j)) * (down ** j)):
                 res2[j] = strp - (spot * (up ** (niter - i - j)) * (down ** j))
            res3[j]=exp((-rfr2) * timeStep) * (prob3 * res3[j] + prob_3 * res3[j + 1])
            if res3[j] < strp - (spot * (up ** (niter - i - j)) * (down ** j)):
                 res3[j] = strp - (spot * (up ** (niter - i - j)) * (down ** j))
    delta = (fu - fd) / ((spot * up) - (spot * down))
    gamma = (((fuu - fud) / (spot * up * up - spot * up * down)) - ((fud - fdd) / (spot * up * down - spot * down * down))) / ((spot * up * up - spot * down * down) / 2)
    vega = res2[0] - res[0]
    theta = (fud - res[0]) / (2 * lif * 365 / niter)
    rho = res3[0] - res[0]
    return delta, gamma, vega, theta, rho


########################################################################################### Asian model#######################################################################


def callPriceAsian(spot, strp, vol, rfr, lif, avgt, avgs):
    """Cette fonction calcule le prix d'une option d'achat asiatique

    INPUTS
    ----------------------------------------------------------------
    spot : prix au comptant
    strp : prix d'exercice
    vol : volatilité
    rfr : taux d'intérêt sans risque
    lif : maturité
    avgt : temps depuis la création de l'option
    avgs : moyenne actuelle du cours du sous-jacent"""

    numberSteps = 50
    numberSimulations = 500
    timeStep = (lif - avgt) / numberSteps

# Fixe le générateur de nombre aléatoire
    randomSeed = 366
    random.seed(randomSeed)
    u = random.random()

    tableauSpots = [[0] * (numberSteps+1) for _ in range(numberSimulations)]
# Simulation de Monte Carlo sous l'hypothèse que le sous-jacent suit une distribution log-normale
    for i in range (numberSimulations):
        tableauSpots[i][0] = spot
        for j in range(1, numberSteps+1):
            u = random.random()
            z = stats.norm.ppf(u, 0, 1)
            tableauSpots[i][j] = tableauSpots[i][j-1] * exp((rfr - ((vol ** 2) / 2)) * timeStep + (vol * sqrt(timeStep) * z))
            u = random.random()
         
    tableauResults = [0 * 1 for _ in range(numberSimulations)]
    result = 0
    for i in range(numberSimulations):
        for j in range (numberSteps+1):
            tableauResults[i] = tableauResults[i] + tableauSpots[i][j]
        tableauResults[i] = ((avgt / lif) * avgs) + (((lif - avgt) / lif) * (tableauResults[i] / numberSteps))
        tableauResults[i] = max(0, tableauResults[i] - strp) * exp(-rfr * lif)
        result = result + (tableauResults[i] / numberSimulations)
      
    return result


def putPriceAsian(spot, strp, vol, rfr, lif, avgt, avgs):
    """Cette fonction calcule le prix d'une option de vente asiatique

    INPUTS
    ----------------------------------------------------------------
    spot : prix au comptant
    strp : prix d'exercice
    vol : volatilité
    rfr : taux d'intérêt sans risque
    lif : maturité
    avgt : temps depuis la création de l'option
    avgs : moyenne actuelle du cours du sous-jacent"""

    numberSteps = 50
    numberSimulations = 500

    timeStep = (lif - avgt) / numberSteps

# Fixe le générateur de nombre aléatoire
    randomSeed = 366
    random.seed(randomSeed)
    u = random.random()

    tableauSpots = [[0] * (numberSteps+1) for _ in range(numberSimulations)]
# Simulation de Monte Carlo sous l'hypothèse que le sous-jacent suit une distribution log-normale
    for i in range (numberSimulations):
        tableauSpots[i][0] = spot
        for j in range(1, numberSteps+1):
            u = random.random()
            z = stats.norm.ppf(u, 0, 1)
            tableauSpots[i][j] = tableauSpots[i][j-1] * exp((rfr - ((vol ** 2) / 2)) * timeStep + (vol * sqrt(timeStep) * z))
            u = random.random()
         
    tableauResults = [0 * 1 for _ in range(numberSimulations)]
    result = 0
    for i in range(numberSimulations):
        for j in range (numberSteps+1):
            tableauResults[i] = tableauResults[i] + tableauSpots[i][j]
        tableauResults[i] = ((avgt / lif) * avgs) + (((lif - avgt) / lif) * (tableauResults[i] / numberSteps))
        tableauResults[i] = max(0, strp - tableauResults[i]) * exp(-rfr * lif)
        result = result + (tableauResults[i] / numberSimulations)
      
    return result


def call_price_greeks_asian(spot, vol, rfr, lif, strp, avgt, avgs):
    """Cette fonction calcule le prix et les grecques d'une option d'achat asiatique

    INPUTS
    ----------------------------------------------------------------
    spot : prix au comptant
    strp : prix d'exercice
    vol : volatilité
    rfr : taux d'intérêt sans risque
    lif : maturité
    avgt : temps depuis la création de l'option
    avgs : moyenne actuelle du cours du sous-jacent"""

    spot2 = spot + 1 #spot augmentant de 1€
    spot3 = spot + 2 #spot augmentant de 2€
    vol2 = vol + 0.01 #volatilité augmentant de 1%
    rfr2 = rfr + 0.01 #taux snas risque augmentant de 1%
    lif2 = lif * (364 / 365) #maturité moins 1 jour
    avgt2 = avgt * (366 / 365) #temps écoulé depuis la création + 1 jour
    avgs2 = avgs  #moyenne actuelle du cours en jour + 1

    #Prix du call au spot :
    price = callPriceAsian(spot, strp, vol, rfr, lif, avgt, avgs)
    #Prix du call au spot + 1 :
    price2 = callPriceAsian(spot2, strp, vol, rfr, lif, avgt, avgs)
    #Prix du call au spot + 2 :
    price3 = callPriceAsian(spot3, strp, vol, rfr, lif, avgt, avgs)

    #Delta du call au niveau du spot :
    delta = price2 - price
    #Delta du call au niveau du spot + 1 :
    delta2 = price3 - price2

    #Gamma
    gamma = delta2 - delta
    #Vega
    vega = callPriceAsian(spot, strp, vol2, rfr, lif, avgt, avgs) - price
    #Theta
    theta = callPriceAsian(spot, strp, vol, rfr, lif2, avgt2, avgs2) - price
    #Rho
    rho = callPriceAsian(spot, strp, vol, rfr2, lif, avgt, avgs) - price

    return price, delta, gamma, vega, theta, rho


def put_price_greeks_asian(spot, vol, rfr, lif, strike, avgt, avgs):
    """Cette fonction calcule le prix et les grecques d'une option de vente asiatique

    INPUTS
    ----------------------------------------------------------------
    spot : prix au comptant
    strp : prix d'exercice
    vol : volatilité
    rfr : taux d'intérêt sans risque
    lif : maturité
    avgt : temps depuis la création de l'option
    avgs : moyenne actuelle du cours du sous-jacent"""

    spot2 = spot + 1 #spot augmentant de 1€
    spot3 = spot + 2 #spot augmentant de 2€
    vol2 = vol + 0.01 #volatilité augmentant de 1%
    rfr2 = rfr + 0.01 #taux sans risque augmentant de 1%
    lif2 = lif * (364 / 365) #maturité moins 1 jour
    avgt2 = avgt * (366 / 365) #temps écoulé depuis la création + 1 jour
    avgs2 = avgs  #moyenne actuelle du cours en jour + 1

    #Prix du call au spot :
    price = putPriceAsian(spot, strike, vol, rfr, lif, avgt, avgs)
    #Prix du call au spot + 1 :
    price2 = putPriceAsian(spot2, strike, vol, rfr, lif, avgt, avgs)
    #Prix du call au spot + 2 :
    price3 = putPriceAsian(spot3, strike, vol, rfr, lif, avgt, avgs)

    #Delta du call au niveau du spot :
    delta = price2 - price
    #Delta du call au niveau du spot + 1 :
    delta2 = price3 - price2

    #Gamma
    gamma = delta2 - delta
    #Vega
    vega = putPriceAsian(spot, strike, vol2, rfr, lif, avgt, avgs) - price
    #Theta
    theta = putPriceAsian(spot, strike, vol, rfr, lif2, avgt2, avgs2) - price
    #Rho
    rho = putPriceAsian(spot, strike, vol, rfr2, lif, avgt, avgs) - price

    return price, delta, gamma, vega, theta, rho


########################################################################################### Barrière Up and Out ############################################################################


def call_price_greeks_barrier_up_and_out(spot, vol, rfr, lif, strike, step, barrier):
    #step nombre d'itérations
    spot2 = spot + 1 #spot augmentant de 1€
    spot3 = spot + 2 #spot augmentant de 2€
    vol2 = vol + 0.01 #volatilité augmentant de 1%
    rfr2 = rfr + 0.01 #taux snas risque augmentant de 1%
    lif2 = lif * (364 / 365) #maturité moins 1 jour
    #Prix du call au spot :
    price = callPriceBarrierUpAndOut(spot, vol, rfr, lif, strike, step, barrier)
    #Prix du call au spot + 1 :
    price2 = callPriceBarrierUpAndOut(spot2, vol, rfr, lif, strike, step, barrier)
    #Prix du call au spot + 2 :
    price3 = callPriceBarrierUpAndOut(spot3, vol, rfr, lif, strike, step, barrier)
    if price2 - price < 0:
        delta = -price / (barrier - spot)
    else:
        delta = price2 - price
    gamma = (price3-price2)-(price2-price)
    vega = callPriceBarrierUpAndOut(spot, vol2, rfr, lif, strike, step, barrier) - price
    theta = callPriceBarrierUpAndOut(spot, vol, rfr, lif2, strike, step, barrier) - price
    rho = callPriceBarrierUpAndOut(spot, vol, rfr2, lif, strike, step, barrier) - price
    return price, delta, gamma, vega, theta, rho

def put_price_greeks_barrier_up_and_out(spot, vol, rfr, lif, strike, step, barrier):
    #step nombre d'itérations
    spot2 = spot + 1 #spot augmentant de 1€
    spot3 = spot + 2 #spot augmentant de 2€
    vol2 = vol + 0.01 #volatilité augmentant de 1%
    rfr2 = rfr + 0.01 #taux snas risque augmentant de 1%
    lif2 = lif * (364 / 365) #maturité moins 1 jour
    #Prix du call au spot :
    price = putPriceBarrierUpAndOut(spot, vol, rfr, lif, strike, step, barrier)
    #Prix du call au spot + 1 :
    price2 = putPriceBarrierUpAndOut(spot2, vol, rfr, lif, strike, step, barrier)
    #Prix du call au spot + 2 :
    price3 = putPriceBarrierUpAndOut(spot3, vol, rfr, lif, strike, step, barrier)
    #delta
    if price2 - price > 0:
        delta = price / (spot - barrier)
    else:
        delta = price2 - price
    gamma = (price3-price2)-(price2-price)
    vega = putPriceBarrierUpAndOut(spot, vol2, rfr, lif, strike, step, barrier) - price
    theta = putPriceBarrierUpAndOut(spot, vol, rfr, lif2, strike, step, barrier) - price
    rho = putPriceBarrierUpAndOut(spot, vol, rfr2, lif, strike, step, barrier) - price
    return price, delta, gamma, vega, theta, rho

def callPriceBarrierUpAndOut(spot, vol, rfr, lif, strike, step, barrier):
    #Cette fonction calcule le prix d'une option d'achat Barrier Up And Out

    timeStep = lif / step

    # Work out lambda (nn)
    n = log(barrier / spot) / (vol * sqrt(timeStep))

    if (n > 2):
        nn = n / int(n)
    else:
       nn = n

    # Precompute invariant quantities
    dx = nn * vol * sqrt(timeStep)
    discount = exp(-rfr * timeStep)
    u = rfr - ((vol**2) / 2)

    pu = (1 / (2 * (nn**2))) + ((u * sqrt(timeStep)) / (2 * nn * vol))
    pd = (1 / (2 * (nn**2))) - ((u * sqrt(timeStep)) / (2 * nn * vol))
    pm = 1 - (1 / (nn**2))

    p_u = discount * pu
    p_d = discount * pd
    p_m = discount * pm

    #Work out stock price
    Stree = [0 * 1 for _ in range(2 * step + 1)]
    Stree[0] = spot * exp(-step * dx)
    exp_dx = exp(dx)

    for i in range (1,2 * step + 1):
        Stree[i] = exp_dx * Stree[i - 1]

    #Work out option price
    OptionValues = [[0] * (2) for _ in range(2 * step + 1)]

    T = (step%2)

    for i in range (2*step + 1):
        if (Stree[i] >= barrier):
            OptionValues[i][T] = 0
        elif (Stree[i] - strike > 0):
            OptionValues[i][T] = Stree[i] - strike
        else:
            OptionValues[i][T] = 0

    for T in range (step-1, -1, -1):
        know = (T % 2)
        knext = ((T + 1) % 2)
        for i in range (step-T, step+T+1):
            if (Stree[i] >= barrier):
                OptionValues[i][know] = 0
            else:
                OptionValues[i][know] = p_d * OptionValues[i - 1][knext] + p_m * OptionValues[i][knext] + p_u * OptionValues[i + 1][knext]

    price = OptionValues[step][0]

    return price

def putPriceBarrierUpAndOut(spot, vol, rfr, lif, strike, step, barrier):
    #Cette fonction calcule le prix d'une option de vente Barrier Up And Out


    timeStep = lif / step

    # Work out lambda (nn)
    n = log(barrier / spot) / (vol * sqrt(timeStep))

    if (n > 2):
        nn = n / int(n)
    else:
       nn = n

    # Precompute invariant quantities
    dx = nn * vol * sqrt(timeStep)
    discount = exp(-rfr * timeStep)
    u = rfr - ((vol**2) / 2)

    pu = (1 / (2 * (nn**2))) + ((u * sqrt(timeStep)) / (2 * nn * vol))
    pd = (1 / (2 * (nn**2))) - ((u * sqrt(timeStep)) / (2 * nn * vol))
    pm = 1 - (1 / (nn**2))

    p_u = discount * pu
    p_d = discount * pd
    p_m = discount * pm

    #Work out stock price
    #ReDim Stree(1 To 2 * step + 1)
    Stree = [0 * 1 for _ in range(2 * step + 1)]
    Stree[0] = spot * exp(-step * dx)
    exp_dx = exp(dx)

    for i in range (1,2 * step + 1):
        Stree[i] = exp_dx * Stree[i - 1]

    #Work out option price
    OptionValues = [[0] * (2) for _ in range(2 * step + 1)]

    T = (step%2)

    for i in range (2*step + 1):
        if (Stree[i] >= barrier):
            OptionValues[i][T] = 0
        elif (Stree[i] - strike < 0):
            OptionValues[i][T] = strike - Stree[i]
        else:
            OptionValues[i][T] = 0

    for T in range (step-1, -1, -1):
        know = (T % 2)
        knext = ((T + 1) % 2)
        for i in range (step-T, step+T+1):
            if (Stree[i] >= barrier):
                OptionValues[i][know] = 0
            else:
                OptionValues[i][know] = p_d * OptionValues[i - 1][knext] + p_m * OptionValues[i][knext] + p_u * OptionValues[i + 1][knext]

    price = OptionValues[step][0]

    return price


########################################################################################### Barrière Down and Out ############################################################################


def call_price_greeks_barrier_down_and_out(spot, vol, rfr, lif, strike, step, barrier):
    #step nombre d'itérations
    spot2 = spot + 1 #spot augmentant de 1€
    spot3 = spot + 2 #spot augmentant de 2€
    vol2 = vol + 0.01 #volatilité augmentant de 1%
    rfr2 = rfr + 0.01 #taux snas risque augmentant de 1%
    lif2 = lif * (364 / 365) #maturité moins 1 jour
    #Prix du call au spot :
    price = callPriceBarrierDownAndOut(spot, vol, rfr, lif, strike, step, barrier)
    #Prix du call au spot + 1 :
    price2 = callPriceBarrierDownAndOut(spot2, vol, rfr, lif, strike, step, barrier)
    #Prix du call au spot + 2 :
    price3 = callPriceBarrierDownAndOut(spot3, vol, rfr, lif, strike, step, barrier)
    if price2 - price < 0:
        delta = -price / (barrier - spot)
    else:
        delta = price2 - price
    gamma = (price3-price2)-(price2-price)
    vega = callPriceBarrierDownAndOut(spot, vol2, rfr, lif, strike, step, barrier) - price
    theta = callPriceBarrierDownAndOut(spot, vol, rfr, lif2, strike, step, barrier) - price
    rho = callPriceBarrierDownAndOut(spot, vol, rfr2, lif, strike, step, barrier) - price
    return price, delta, gamma, vega, theta, rho

def put_price_greeks_barrier_down_and_out(spot, vol, rfr, lif, strike, step, barrier):
    #step nombre d'itérations
    spot2 = spot + 1 #spot augmentant de 1€
    spot3 = spot + 2 #spot augmentant de 2€
    vol2 = vol + 0.01 #volatilité augmentant de 1%
    rfr2 = rfr + 0.01 #taux snas risque augmentant de 1%
    lif2 = lif * (364 / 365) #maturité moins 1 jour
    #Prix du call au spot :
    price = putPriceBarrierDownAndOut(spot, vol, rfr, lif, strike, step, barrier)
    #Prix du call au spot + 1 :
    price2 = putPriceBarrierDownAndOut(spot2, vol, rfr, lif, strike, step, barrier)
    #Prix du call au spot + 2 :
    price3 = putPriceBarrierDownAndOut(spot3, vol, rfr, lif, strike, step, barrier)
    #delta
    if price2 - price > 0:
        delta = price / (spot - barrier)
    else:
        delta = price2 - price
    gamma = (price3-price2)-(price2-price)
    vega = putPriceBarrierDownAndOut(spot, vol2, rfr, lif, strike, step, barrier) - price
    theta = putPriceBarrierDownAndOut(spot, vol, rfr, lif2, strike, step, barrier) - price
    rho = putPriceBarrierDownAndOut(spot, vol, rfr2, lif, strike, step, barrier) - price
    return price, delta, gamma, vega, theta, rho

def callPriceBarrierDownAndOut(spot, vol, rfr, life, strike, step, barrier):
    #Cette fonction calcule le prix d'une option d'achat Barrier Down And Out

    timeStep = life / step

    # Work out lambda (nn)
    n = log(spot/barrier) / (vol * sqrt(timeStep))

    if (n > 2):
        nn = n / int(n)
    else:
       nn = n

    # Precompute invariant quantities
    dx = nn * vol * sqrt(timeStep)
    discount = exp(-rfr * timeStep)
    u = rfr - ((vol**2) / 2)

    pu = (1 / (2 * (nn**2))) + ((u * sqrt(timeStep)) / (2 * nn * vol))
    pd = (1 / (2 * (nn**2))) - ((u * sqrt(timeStep)) / (2 * nn * vol))
    pm = 1 - (1 / (nn**2))

    p_u = discount * pu
    p_d = discount * pd
    p_m = discount * pm

    #Work out stock price
    Stree = [0 * 1 for _ in range(2 * step + 1)]
    Stree[0] = spot * exp(-step * dx)
    exp_dx = exp(dx)

    for i in range (1,2 * step + 1):
        Stree[i] = exp_dx * Stree[i - 1]

    #Work out option price
    OptionValues = [[0] * (2) for _ in range(2 * step + 1)]

    T = (step%2)

    for i in range (2*step + 1):
        if (Stree[i] <= barrier):
            OptionValues[i][T] = 0
        elif (Stree[i] - strike > 0):
            OptionValues[i][T] = Stree[i] - strike
        else:
            OptionValues[i][T] = 0

    for T in range (step-1, -1, -1):
        know = (T % 2)
        knext = ((T + 1) % 2)
        for i in range (step-T, step+T+1):
            if (Stree[i] <= barrier):
                OptionValues[i][know] = 0
            else:
                OptionValues[i][know] = p_d * OptionValues[i - 1][knext] + p_m * OptionValues[i][knext] + p_u * OptionValues[i + 1][knext]

    price = OptionValues[step][0]

    return price

def putPriceBarrierDownAndOut(spot, vol, rfr, life, strp, step, barrier):
    #Cette fonction calcule le prix d'une option de vente Barrier Down And Out

    timeStep = life / step

    # Work out lambda (nn)
    n = log(spot/barrier) / (vol * sqrt(timeStep))

    if (n > 2):
        nn = n / int(n)
    else:
       nn = n

    # Precompute invariant quantities
    dx = nn * vol * sqrt(timeStep)
    discount = exp(-rfr * timeStep)
    u = rfr - ((vol**2) / 2)

    pu = (1 / (2 * (nn**2))) + ((u * sqrt(timeStep)) / (2 * nn * vol))
    pd = (1 / (2 * (nn**2))) - ((u * sqrt(timeStep)) / (2 * nn * vol))
    pm = 1 - (1 / (nn**2))

    p_u = discount * pu
    p_d = discount * pd
    p_m = discount * pm

    #Work out stock price
    Stree = [0 * 1 for _ in range(2 * step + 1)]
    Stree[0] = spot * exp(-step * dx)
    exp_dx = exp(dx)

    for i in range (1,2 * step + 1):
        Stree[i] = exp_dx * Stree[i - 1]

    #Work out option price
    OptionValues = [[0] * (2) for _ in range(2 * step + 1)]

    T = (step%2)

    for i in range (2*step + 1):
        if (Stree[i] <= barrier):
            OptionValues[i][T] = 0
        elif (Stree[i] - strp < 0):
            OptionValues[i][T] = strp - Stree[i]
        else:
            OptionValues[i][T] = 0

    for T in range (step-1, -1, -1):
        know = (T % 2)
        knext = ((T + 1) % 2)
        for i in range (step-T, step+T+1):
            if (Stree[i] <= barrier):
                OptionValues[i][know] = 0
            else:
                OptionValues[i][know] = p_d * OptionValues[i - 1][knext] + p_m * OptionValues[i][knext] + p_u * OptionValues[i + 1][knext]

    price = OptionValues[step][0]

    return price


########################################################################################### Barrière Down and In ############################################################################


def call_price_greeks_barrier_down_and_in(spot, vol, rfr, lif, strp, barrier):
    #step nombre d'itérations
    spot2 = spot + 1 #spot augmentant de 1€
    spot3 = spot + 2 #spot augmentant de 2€
    vol2 = vol + 0.01 #volatilité augmentant de 1%
    rfr2 = rfr + 0.01 #taux snas risque augmentant de 1%
    lif2 = lif * (364 / 365) #maturité moins 1 jour
    #Prix du call au spot :
    price = callPriceBarrierDownAndIn(spot, vol, rfr, lif, strp, barrier)
    #Prix du call au spot + 1 :
    price2 = callPriceBarrierDownAndIn(spot2, vol, rfr, lif, strp, barrier)
    #Prix du call au spot + 2 :
    price3 = callPriceBarrierDownAndIn(spot3, vol, rfr, lif, strp, barrier)
    delta = price2 - price
    gamma = (price3-price2)-(price2-price)
    vega = callPriceBarrierDownAndIn(spot, vol2, rfr, lif, strp, barrier) - price
    theta = callPriceBarrierDownAndIn(spot, vol, rfr, lif2, strp, barrier) - price
    rho = callPriceBarrierDownAndIn(spot, vol, rfr2, lif, strp, barrier) - price
    return price, delta, gamma, vega, theta, rho

def put_price_greeks_barrier_down_and_in(spot, vol, rfr, lif, strp, barrier):
    #step nombre d'itérations
    spot2 = spot + 1 #spot augmentant de 1€
    spot3 = spot + 2 #spot augmentant de 2€
    vol2 = vol + 0.01 #volatilité augmentant de 1%
    rfr2 = rfr + 0.01 #taux snas risque augmentant de 1%
    lif2 = lif * (364 / 365) #maturité moins 1 jour
    #Prix du call au spot :
    price = putPriceBarrierDownAndIn(spot, vol, rfr, lif, strp, barrier)
    #Prix du call au spot + 1 :
    price2 = putPriceBarrierDownAndIn(spot2, vol, rfr, lif, strp, barrier)
    #Prix du call au spot + 2 :
    price3 = putPriceBarrierDownAndIn(spot3, vol, rfr, lif, strp, barrier)
    delta = price2 - price
    gamma = (price3-price2)-(price2-price)
    vega = putPriceBarrierDownAndIn(spot, vol2, rfr, lif, strp, barrier) - price
    theta = putPriceBarrierDownAndIn(spot, vol, rfr, lif2, strp, barrier) - price
    rho = putPriceBarrierDownAndIn(spot, vol, rfr2, lif, strp, barrier) - price
    return price, delta, gamma, vega, theta, rho

def callPriceBarrierDownAndIn(spot, vol, rfr, lif, strike, barrier):
    #Cette fonction calcule le prix d'une option d'achat Barrier Down And In

    lam = (rfr + ((vol**2) / 2)) / (vol**2)
    y = log((barrier**2) / (spot*strike)) / (vol * sqrt(lif)) + lam * vol * sqrt(lif)

    a = spot*((barrier/spot)**(2*lam))*stats.norm.cdf(y, 0, 1)
    b = (strike * exp(-rfr * lif)) * ((barrier / spot) ** (2 * lam - 2)) * stats.norm.cdf(y - vol * sqrt(lif), 0, 1)

    price = a - b

    return price


def putPriceBarrierDownAndIn(spot, vol, rfr, life, strp, barrier):
    #Cette fonction calcule le prix d'une option de vente Barrier Down And In

    lam = (rfr + ((vol**2) / 2)) / (vol**2)
    y = log((barrier**2) / (spot * strp)) / (vol * sqrt(life)) + lam * vol * sqrt(life)
    x1 = log(spot/barrier) / (vol*sqrt(life)) + (lam*vol*sqrt(life))
    y1 = log(barrier/spot) / (vol*sqrt(life)) + (lam*vol*sqrt(life))

    a = (-spot) * stats.norm.cdf(-x1, 0, 1)
    b = (strp * exp(-rfr * life)) * stats.norm.cdf(-x1 + (vol * sqrt(life)), 0, 1)
    c = spot * ((barrier/spot)**(2*lam)) * (stats.norm.cdf(y, 0, 1) - stats.norm.cdf(y1, 0, 1))
    d = (-strp * exp(-rfr * life)) * ((barrier / spot) ** (2 * lam - 2)) * (stats.norm.cdf(y - (vol * sqrt(life)), 0, 1) - stats.norm.cdf(y1 - (vol * sqrt(life)), 0, 1))

    price = a + b + c + d

    return price


####################################################################### Binary Cash or Nothing #############################################################################


def callPriceBinaryCashOrNothing(spot, strp, vol, rfr, lif, cash) :
    # Cette fonction calcule le prix d'une option d'achat Binary Cash Or Nothing

    d1 = ((log(spot / strp)) + ((rfr + ((vol ** 2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol * sqrt(lif))
    cdf = stats.norm.cdf(d2, 0, 1)
    price = exp(-(rfr * lif)) * cdf * cash
   
    return price


def putPriceBinaryCashOrNothing(spot, strp, vol, rfr, lif, cash):
    # Cette fonction calcule le prix d'une option de vente Binary Cash Or Nothing

    d1 = ((log(spot / strp)) + ((rfr + ((vol ** 2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol * sqrt(lif))
    cdf = stats.norm.cdf(d2, 0, 1)
    price = exp(-rfr * lif) * (1 - cdf) * cash

    return price


def call_Binary_Cash_Or_Nothing_model(spot, vol, rfr, life, strp, cash):
    # Cette fonction calcule le prix et les greeks d'une option d'achat Binary Cash Or Nothing

    d1 = ((log(spot / strp)) + ((rfr + ((vol ** 2) / 2)) * life)) / (vol * sqrt(life))
    d2 = d1 - (vol * sqrt(life))

    Pi = pi #nombre Pi
    phi1 = exp(-(d1**2 / 2)) / sqrt(2 * Pi)

    cdf2 = stats.norm.cdf(d2, 0, 1) #fonction de répartition de la loi normale

    price = exp(-(rfr * life)) * cdf2 * cash #price
    delta = ((spot / strp) * (phi1 / (spot * vol * sqrt(life)))) * cash #delta
    gamma = (-((phi1 / (spot * vol * sqrt(life))) / strp) * (d1 / (vol * sqrt(life)))) * cash #gamma
    #Vega
    vol2 = vol + 0.01 #Lorsque la volatilité augmente de 1%
    d1Vol = ((log(spot / strp)) + ((rfr + ((vol2 ** 2) / 2)) * life)) / (vol2 * sqrt(life))
    d2Vol = d1Vol - (vol2 * sqrt(life))
    cdf2Vol = stats.norm.cdf(d2Vol, 0, 1)
    vega = (exp(-(rfr * life)) * cdf2Vol * cash) - (exp(-(rfr * life)) * cdf2 * cash)
    #Theta
    life2 = life * 0.99726027 #Maturité - 1 jour
    d1life = ((log(spot / strp)) + ((rfr + ((vol ** 2) / 2)) * life2)) / (vol * sqrt(life2))
    d2life = d1life - (vol * sqrt(life2))
    cdf2life = stats.norm.cdf(d2life, 0, 1)
    theta = (exp(-(rfr * life2)) * cdf2life * cash) - (exp(-(rfr * life)) * cdf2 * cash)
    #Rho
    rfr2 = rfr + 0.01 #Lorsque le taux sans risque augmente de 1%
    d1RFR = ((log(spot / strp)) + ((rfr2 + ((vol ** 2) / 2)) * life)) / (vol * sqrt(life))
    d2RFR = d1RFR - (vol * sqrt(life))
    cdf2RFR = stats.norm.cdf(d2RFR, 0, 1)
    rho = (exp(-(rfr2 * life)) * cdf2RFR * cash) - (exp(-(rfr * life)) * cdf2 * cash)

    return price, delta, gamma, vega, theta, rho

def put_Binary_Cash_Or_Nothing_model(spot, vol, rfr, lif, strp, cash):
    # Cette fonction calcule le prix et les greeks d'une option de vente Binary Cash Or Nothing

    d1 = ((log(spot / strp)) + ((rfr + ((vol ** 2) / 2)) * lif)) / (vol * sqrt(lif))
    d2 = d1 - (vol * sqrt(lif))

    Pi = pi #nombre Pi
    phi1 = exp(-(d1**2 / 2)) / sqrt(2 * Pi)

    cdf2 = stats.norm.cdf(d2, 0, 1) #fonction de répartition de la loi normale

    price = exp(-(rfr * lif)) * (1 - cdf2) * cash #price
    delta = (-(spot / strp)) * (phi1 / (spot * vol * sqrt(lif))) * cash #delta
    gamma = (((phi1 / (spot * vol * sqrt(lif))) / strp) * (d1 / (vol * sqrt(lif)))) * cash #gamma
    #Vega
    vol2 = vol + 0.01 #Lorsque la volatilité augmente de 1%
    d1Vol = ((log(spot / strp)) + ((rfr + ((vol2 ** 2) / 2)) * lif)) / (vol2 * sqrt(lif))
    d2Vol = d1Vol - (vol2 * sqrt(lif))
    cdf2Vol = stats.norm.cdf(d2Vol, 0, 1)
    vega = (exp(-(rfr * lif)) * (1 - cdf2Vol) * cash) - (exp(-(rfr * lif)) * (1 - cdf2) * cash)
    #Theta
    life2 = lif * 0.99726027 #Maturité - 1 jour
    d1life = ((log(spot / strp)) + ((rfr + ((vol ** 2) / 2)) * life2)) / (vol * sqrt(life2))
    d2life = d1life - (vol * sqrt(life2))
    cdf2life = stats.norm.cdf(d2life, 0, 1)
    theta = (exp(-(rfr * life2)) * (1-cdf2life) * cash) - (exp(-(rfr * lif)) * (1 - cdf2) * cash)
    #Rho
    rfr2 = rfr + 0.01 #Lorsque le taux sans risque augmente de 1%
    d1RFR = ((log(spot / strp)) + ((rfr2 + ((vol ** 2) / 2)) * lif)) / (vol * sqrt(lif))
    d2RFR = d1RFR - (vol * sqrt(lif))
    cdf2RFR = stats.norm.cdf(d2RFR, 0, 1)
    rho = (exp(-(rfr2 * lif)) * (1 - cdf2RFR) * cash) - (exp(-(rfr * lif)) * (1 - cdf2) * cash)

    return price, delta, gamma, vega, theta, rho


################################################################################ Binary Asset or Nothing ####################################################################################

def call_Binary_Asset_Or_Nothing_model(spot, vol, rfr, lif, strp):
    spot2 = spot+1
    spot3 = spot+2
    vol2 = vol+0.01
    rfr2 = rfr+0.01
    life2= lif * (364 / 365)
    price = sum(call_price_BS_model(spot, vol, rfr, lif, strp) + list([callPriceBinaryCashOrNothing(spot, strp, vol, rfr, lif, strp)])) #prix du call au spot
    price2 =sum(call_price_BS_model(spot2, vol, rfr, lif, strp) + list([callPriceBinaryCashOrNothing(spot2, strp, vol, rfr, lif, strp)]))#prix du call au spot + 1
    price3 = sum(call_price_BS_model(spot3, vol, rfr, lif, strp) + list([callPriceBinaryCashOrNothing(spot3, strp, vol, rfr, lif, strp)])) #prix du call au spot + 2
    delta = price2 - price #delta du call au niveau du spot
    delta2 = price3 - price2 #delta du call au niveau du spot + 1
    gamma = delta2-delta #gamma
    vega = sum(-price + call_price_BS_model(spot, vol2, rfr, lif, strp) + list([callPriceBinaryCashOrNothing(spot, strp, vol2, rfr, lif, strp)])) #vega
    theta = sum(-price + call_price_BS_model(spot, vol, rfr, life2, strp) + list([callPriceBinaryCashOrNothing(spot, strp, vol, rfr, life2, strp)])) #theta
    rho = sum(-price + call_price_BS_model(spot, vol, rfr2, lif, strp) + list([callPriceBinaryCashOrNothing(spot, strp, vol, rfr2, lif, strp)])) #rho
    return price, delta, gamma, vega, theta, rho

def put_Binary_Asset_Or_Nothing_model(spot, vol, rfr, lif, strp):
    spot2 = spot+1
    spot3 = spot+2
    vol2 = vol+0.01
    rfr2 = rfr+0.01
    life2= lif * (364 / 365)
    price = sum(put_price_BS_model(spot, vol, rfr, lif, strp) + list([putPriceBinaryCashOrNothing(spot, strp, vol, rfr, lif, strp)])) #prix du call au spot
    price2 =sum(put_price_BS_model(spot2, vol, rfr, lif, strp) + list([putPriceBinaryCashOrNothing(spot2, strp, vol, rfr, lif, strp)]))#prix du call au spot + 1
    price3 = sum(put_price_BS_model(spot3, vol, rfr, lif, strp) + list([putPriceBinaryCashOrNothing(spot3, strp, vol, rfr, lif, strp)])) #prix du call au spot + 2
    delta = price2 - price #delta du call au niveau du spot
    delta2 = price3 - price2 #delta du call au niveau du spot + 1
    gamma = delta2-delta #gamma
    vega = sum(-price + put_price_BS_model(spot, vol2, rfr, lif, strp) + list([putPriceBinaryCashOrNothing(spot, strp, vol2, rfr, lif, strp)])) #vega
    theta = sum(-price + put_price_BS_model(spot, vol, rfr, life2, strp) + list([putPriceBinaryCashOrNothing(spot, strp, vol, rfr, life2, strp)])) #theta
    rho = sum(-price + put_price_BS_model(spot, vol, rfr2, lif, strp) + list([putPriceBinaryCashOrNothing(spot, strp, vol, rfr2, lif, strp)])) #rho
    return price, delta, gamma, vega, theta, rho

