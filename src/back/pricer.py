#Tab1
from src.back.equityOptionFunctions import *
from src.back.currencyOptionFunctions import *
from src.back.indexOptionFunctions import *
from src.back.futuresOptionFunctions import *

#Tab2
from src.back.monteCarloFunctions import *
import matplotlib.pyplot as plt
from tkinter import messagebox

#Tab3
from src.back.bondsPricingFunctions import *

#Tab4
from src.back.ratesCurveFunctions import *


"""
from imaplib import Time2Internaldate
from math import *
from pickle import STOP
from numpy.random import normal
from scipy import stats
import pandas as pd
import numpy as np
import random
import statistics
import matplotlib.pyplot as plt
from tkinter import messagebox
#from datetime import datetime, timedelta
from scipy import interpolate

print(__file__)
from pathlib import Path
print(Path("."))
"""


#####################################Tab 1#####################################

#Cette fonction lance la fonction selon le modèle et le sj sélectionnés par l'utilisateur en Tab1:
def option_calculation(ut2, stop2, vol2, rfr2, ot2, lif2, strp2, valueRB2,valueCB2, ov1=0, ov2=0, ov3=0, pri2=0):
        
        #equity
        if (ut2 == "Equity" and ot2 == "Black Scholes European" and valueRB2 == 0 and valueCB2 == 0): 
            price, delta, gamma, vega, theta, rho = call_price_greeks_BS_model(stop2,vol2,rfr2,lif2,strp2)
            
        elif (ut2 == "Equity" and ot2 == "Black Scholes European" and valueRB2 == 1 and valueCB2 == 0):
            price, delta, gamma, vega, theta, rho = put_price_greeks_BS_model(stop2,vol2,rfr2,lif2,strp2)
            
        elif (ut2 == "Equity" and ot2 == "Binomial European" and valueRB2 == 0 and valueCB2 == 0):
            ov2 = int(ov2)
            price = call_price_binomial_european_model(stop2, vol2, rfr2, lif2, strp2, ov2)
            delta, gamma, vega, theta, rho = call_greeks_binomial_european_model(stop2, vol2, rfr2, lif2, strp2, ov2)

        elif (ut2 == "Equity" and ot2 == "Binomial European" and valueRB2 == 1 and valueCB2 == 0):
            ov2 = int(ov2)
            price = put_price_binomial_european_model(stop2, vol2, rfr2, lif2, strp2, ov2)
            delta, gamma, vega, theta, rho = put_greeks_binomial_european_model(stop2, vol2, rfr2, lif2, strp2, ov2)

        elif (ut2 == "Equity" and ot2 == "Binomial American" and valueRB2 == 0 and valueCB2 == 0):
            ov2 = int(ov2)
            price = call_price_binomial_american_model(stop2, vol2, rfr2, lif2, strp2, ov2)
            delta, gamma, vega, theta, rho = call_greeks_binomial_american_model(stop2, vol2, rfr2, lif2, strp2, ov2)
      
        elif (ut2 == "Equity" and ot2 == "Binomial American" and valueRB2 == 1 and valueCB2 == 0):
            ov2 = int(ov2)
            price = put_price_binomial_american_model(stop2, vol2, rfr2, lif2, strp2, ov2)
            delta, gamma, vega, theta, rho = put_greeks_binomial_american_model(stop2, vol2, rfr2, lif2, strp2, ov2)

        elif (ut2 == "Equity" and ot2 == "Asian" and valueRB2 == 0 and valueCB2 == 0):
            tsi2 = float(ov2)
            ca2 = float(ov3)
            price, delta, gamma, vega, theta, rho = call_price_greeks_asian(stop2, vol2, rfr2, lif2, strp2, tsi2, ca2)
            
        elif (ut2 == "Equity" and ot2 == "Asian" and valueRB2 == 1 and valueCB2 == 0):
            tsi2 = float(ov2)
            ca2 = float(ov3)
            price, delta, gamma, vega, theta, rho = put_price_greeks_asian(stop2, vol2, rfr2, lif2, strp2, tsi2, ca2)
        
       # elif (ut2 == "Equity" and ot2 == "Barrier Up And In" and valueRB2 == 0 and valueCB2 == 0):
       #     bar2 = int(ov2)
       #     price, delta, gamma, vega, theta, rho = call_price_greeks_barrier_up_and_in(stop2, vol2, rfr2, lif2, strp2, 2000, bar2)

       # elif (ut2 == "Equity" and ot2 == "Barrier Up And In" and valueRB2 == 1 and valueCB2 == 0):
       #     bar2 = int(ov2)
       #     price, delta, gamma, vega, theta, rho = put_price_greeks_barrier_up_and_in(stop2, vol2, rfr2, lif2, strp2, 2000, bar2)

        elif (ut2 == "Equity" and ot2 == "Barrier Up And Out" and valueRB2 == 0 and valueCB2 == 0):
            bar2 = int(ov2)
            price, delta, gamma, vega, theta, rho = call_price_greeks_barrier_up_and_out(stop2, vol2, rfr2, lif2, strp2, 2000,bar2)

        elif (ut2 == "Equity" and ot2 == "Barrier Up And Out" and valueRB2 == 1 and valueCB2 == 0):
            bar2 = int(ov2)
            price, delta, gamma, vega, theta, rho = put_price_greeks_barrier_up_and_out(stop2, vol2, rfr2, lif2, strp2, 2000, bar2)

        elif (ut2 == "Equity" and ot2 == "Barrier Down And In" and valueRB2 == 0 and valueCB2 == 0):
            bar2 = int(ov2)
            price, delta, gamma, vega, theta, rho = call_price_greeks_barrier_down_and_in(stop2, vol2, rfr2, lif2, strp2, bar2)

        elif (ut2 == "Equity" and ot2 == "Barrier Down And In" and valueRB2 == 1 and valueCB2 == 0):
            bar2 = int(ov2)
            price, delta, gamma, vega, theta, rho = put_price_greeks_barrier_down_and_in(stop2, vol2, rfr2, lif2, strp2, bar2)

        elif (ut2 == "Equity" and ot2 == "Barrier Down And Out" and valueRB2 == 0 and valueCB2 == 0):
            bar2 = int(ov2)
            price, delta, gamma, vega, theta, rho = call_price_greeks_barrier_down_and_out(stop2, vol2, rfr2, lif2, strp2, 2000, bar2)

        elif (ut2 == "Equity" and ot2 == "Barrier Down And Out" and valueRB2 == 1 and valueCB2 == 0):
            bar2 = int(ov2)
            price, delta, gamma, vega, theta, rho = put_price_greeks_barrier_down_and_out(stop2, vol2, rfr2, lif2, strp2, 2000, bar2)
  
        elif (ut2 == "Equity" and ot2 == "Binary Cash Or Nothing" and valueRB2 == 0 and valueCB2 == 0):
            cash = int(ov2)
            price, delta, gamma, vega, theta, rho =  call_Binary_Cash_Or_Nothing_model(stop2, vol2, rfr2, lif2, strp2, cash)

        elif (ut2 == "Equity" and ot2 == "Binary Cash Or Nothing" and valueRB2 == 1 and valueCB2 == 0):
            cash = int(ov2)
            price, delta, gamma, vega, theta, rho =  put_Binary_Cash_Or_Nothing_model(stop2, vol2, rfr2, lif2, strp2, cash)

        elif (ut2 == "Equity" and ot2 == "Binary Asset Or Nothing" and valueRB2 == 0 and valueCB2 == 0):
            price, delta, gamma, vega, theta, rho = call_Binary_Asset_Or_Nothing_model(stop2, vol2, rfr2, lif2, strp2)
            
        elif (ut2 == "Equity" and ot2 == "Binary Asset Or Nothing" and valueRB2 == 1 and valueCB2 == 0):
            price, delta, gamma, vega, theta, rho = put_Binary_Asset_Or_Nothing_model(stop2, vol2, rfr2, lif2, strp2)
        

        #currency 
        elif (ut2 == "Currency" and ot2 == "Black Scholes European" and valueRB2 == 0 and valueCB2 == 0):
            frfr2 = float(ov1) / 100
            price, delta, gamma, vega, theta, rho = call_currency_price_greeks_BS_model(stop2,vol2,rfr2,lif2,strp2, frfr2)  

        elif (ut2 == "Currency" and ot2 == "Black Scholes European" and valueRB2 == 1 and valueCB2 == 0):
            frfr2 = float(ov1) / 100
            price, delta, gamma, vega, theta, rho = put_currency_price_greeks_BS_model(stop2,vol2,rfr2,lif2,strp2, frfr2)


        #index 
        elif (ut2 == "Index" and ot2 == "Black Scholes European" and valueRB2 == 0 and valueCB2 == 0):
            divy2 = float(ov1) / 100
            price, delta, gamma, vega, theta, rho = call_index_price_greeks_BS_model(stop2,vol2,rfr2,lif2,strp2, divy2)  

        elif (ut2 == "Index" and ot2 == "Black Scholes European" and valueRB2 == 1 and valueCB2 == 0):
            divy2 = float(ov1) / 100
            price, delta, gamma, vega, theta, rho = put_index_price_greeks_BS_model(stop2,vol2,rfr2,lif2,strp2, divy2)


        #futures
        elif (ut2 == "Futures" and ot2 == "Black Scholes European" and valueRB2 == 0 and valueCB2 == 0):
            price, delta, gamma, vega, theta, rho = call_futures_price_greeks_BS_model(stop2,vol2,rfr2,lif2,strp2)  

        elif (ut2 == "Futures" and ot2 == "Black Scholes European" and valueRB2 == 1 and valueCB2 == 0):
            price, delta, gamma, vega, theta, rho = put_futures_price_greeks_BS_model(stop2,vol2,rfr2,lif2,strp2)


        return price, delta, gamma, vega, theta, rho


#Cette fonction lance la fonction qui calcule la volatilité implicite en Tab1:     
def option_calculation_impliedVolatility(ut2, stop2, prio2, rfr2, ot2, lif2, strp2, valueRB2,valueCB2):
        
        if (ut2 == "Equity" and ot2 == "Black Scholes European" and valueRB2 == 0 and valueCB2 == 1): #implied vol pour un call
            stav = 0.2 #on assume une volatilité égale à 20% sur le marché action  
            impliedVolatility = round(call_implied_volatility_BS(stop2, strp2, rfr2, lif2, prio2, stav) * 100, 5)
        
        elif (ut2 == "Equity" and ot2 == "Black Scholes European" and valueRB2 == 1 and valueCB2 == 1): #implied vol pour un put
            stav = 0.2 #on assume une volatilité égale à 20% sur le marché action  
            impliedVolatility = round(put_implied_volatility_BS(stop2, strp2, rfr2, lif2, prio2, stav) * 100, 5)

        return impliedVolatility


#####################################Tab 2#####################################

#Cette fonction lance la fonction qui calcule le prix de l'option via Monte Carlo:
def option_calculation_tab2(ut2_tab2, stop2_tab2, vol2_tab2, rfr2_tab2, ot2_tab2, mt2_tab2, lif2_tab2, strp2_tab2, valueRB2_tab2, divy2_tab2, nts2_tab2, nos2_tab2, rans2_tab2, ov1_tab2=0,ov2_tab2=0,ov3_tab2=0):
        
        if nts2_tab2 < 2 or  nts2_tab2 > 200 :
            messagebox.showinfo("Alert", "Number of time steps must be between 2 and 200")
            return
        elif nos2_tab2 < 4 or  nos2_tab2 > 10000 :
             messagebox.showinfo("Alert", "Number of simulations must be between 4 and 10000")
             return
        
        elif ut2_tab2 == "Equity" and ot2_tab2 == "European" and mt2_tab2 == "Log Normal" and valueRB2_tab2 == 0: #Lancement de la simulation Monte-Carlo (modèle : Log-Normal) pour un Call
            price, standardError, tableauSpots = monteCarloEuropeanLogNormalCall(stop2_tab2, vol2_tab2 , rfr2_tab2, lif2_tab2, strp2_tab2, divy2_tab2, int(nts2_tab2), int(nos2_tab2), rans2_tab2)
        
        elif ut2_tab2 == "Equity" and ot2_tab2 == "European" and mt2_tab2 == "Log Normal" and valueRB2_tab2 == 1: #Lancement de la simulation Monte-Carlo (modèle : Log-Normal) pour un Put
            price, standardError, tableauSpots = monteCarloEuropeanLogNormalPut(stop2_tab2, vol2_tab2 , rfr2_tab2, lif2_tab2, strp2_tab2, divy2_tab2, int(nts2_tab2), int(nos2_tab2), rans2_tab2)
        
        elif ut2_tab2 == "Equity" and ot2_tab2 == "European" and mt2_tab2 == "Merton Jump Diffusion" and valueRB2_tab2 == 0: #Lancement de la simulation Monte-Carlo (modèle : Merton Jump Diffusion) pour un Call
            jpy = int(ov1_tab2)
            ajs = float(ov2_tab2)
            jsd = float(ov3_tab2)
            price, standardError, tableauSpots = monteCarloEuropeanMertonJumpDiffusionCall(stop2_tab2, vol2_tab2 , rfr2_tab2, lif2_tab2, strp2_tab2, divy2_tab2, int(nts2_tab2), int(nos2_tab2), rans2_tab2,jpy, ajs, jsd)
        
        elif ut2_tab2 == "Equity" and ot2_tab2 == "European" and mt2_tab2 == "Merton Jump Diffusion" and valueRB2_tab2 == 1: #Lancement de la simulation Monte-Carlo (modèle : Merton Jump Diffusion) pour un Put
            jpy = int(ov1_tab2)
            ajs = float(ov2_tab2)
            jsd = float(ov3_tab2) 
            price, standardError, tableauSpots = monteCarloEuropeanMertonJumpDiffusionPut(stop2_tab2, vol2_tab2 , rfr2_tab2, lif2_tab2, strp2_tab2, divy2_tab2, int(nts2_tab2), int(nos2_tab2), rans2_tab2,jpy, ajs, jsd)

        return price, standardError, tableauSpots



#####################################Tab 3#####################################


#####################################Tab 4#####################################


