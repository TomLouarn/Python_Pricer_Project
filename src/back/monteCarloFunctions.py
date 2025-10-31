from scipy import stats
import statistics
import random
from math import *


def monteCarloEuropeanLogNormalCall(v1, v2, v3, v4, v5, v6, v7, v8, v9):
# Cette fonction renvoie le prix d'une option européenne d'achat via Monte Carlo avec le modèle log normal
#
# INPUTS
#----------------------------------------------------------------
# v1 : prix au comptant
# v2 : volatilité
# v3 : taux d'intérêt sans risque
# v4 : maturité
# v5 : prix d'exercice
# v6 : dividendes
# v7 : nombre d'itérations
# v8 : nombre de simulations
# v9 : fixation de l'aléa
#
# OUTPUT
#----------------------------------------------------------------
#
# Prix de l'option d'achat, l'écart type et les paths
#
#----------------------------------------------------------------

   timeStep = v4/v7 #Le pas d'itération

   tableauSpots = [[0] * (v7+1) for _ in range(v8)]
   
   # Fixe le générateur de nombre aléatoire
   random.seed(v9)
   u = random.random()
   
   #Tableau contenant le passage du temps
   global tableauTime
   tableauTime = [[0] * (1) for _ in range(v7+1)]
   tableauTime[0] = 0 #Initialisation
   for i in range(1,v7+1):
       tableauTime[i] = tableauTime[i-1] + timeStep

   #Simulation de Monte Carlo sous l'hypothèse que le sous-jacent suit une distribution log-normale
   for i in range (v8):
       tableauSpots[i][0] = v1
       for j in range (1, v7+1):
            u = random.random()
            z = stats.norm.ppf(u, 0, 1)
            tableauSpots[i][j] =  tableauSpots[i][j-1] * exp((v3 - v6 - ((v2**2) / 2)) * timeStep + (v2 * sqrt(timeStep) * z))
            u = random.random()
          
   #Calcul du prix de l'option et l'écart-type de la simulation
   tableauResults = [[0] * (1) for _ in range(v8)]
   priceCum = 0
   for i in range (v8):
       tableauResults[i] = max(tableauSpots[i][v7] - v5, 0) * exp(-v3 * v4)
       priceCum = priceCum + tableauResults[i]
   
   price = priceCum / v8
   standardDeviation = statistics.stdev(tableauResults) / sqrt(v8)
   
   return price, standardDeviation, tableauSpots


def monteCarloEuropeanLogNormalPut(v1, v2, v3, v4, v5, v6, v7, v8, v9):
# Cette fonction renvoie le prix d'une option européenne de vente via Monte Carlo avec le modèle log normal
#
# INPUTS
#----------------------------------------------------------------
# v1 : prix au comptant
# v2 : volatilité
# v3 : taux d'intérêt sans risque
# v4 : maturité
# v5 : prix d'exercice
# v6 : dividendes
# v7 : nombre d'itérations
# v8 : nombre de simulations
# v9 : fixation de l'aléa
#
# OUTPUT
#----------------------------------------------------------------
#
# Prix de l'option de vente, l'écart type et les paths
#
#----------------------------------------------------------------

   timeStep = v4/v7 #Le pas d'itération

   global tableauSpots
   tableauSpots = [[0] * (v7+1) for _ in range(v8)]
   
   # Fixe le générateur de nombre aléatoire
   random.seed(v9)
   u = random.random()
   
   #Tableau contenant le passage du temps
   global tableauTime
   tableauTime = [[0] * (1) for _ in range(v7+1)]
   tableauTime[0] = 0 #Initialisation
   for i in range(1,v7+1):
       tableauTime[i] = tableauTime[i-1] + timeStep

   #Simulation de Monte Carlo sous l'hypothèse que le sous-jacent suit une distribution log-normale
   for i in range (v8):
       tableauSpots[i][0] = v1
       for j in range (1, v7+1):
            u = random.random()
            z = stats.norm.ppf(u, 0, 1)
            tableauSpots[i][j] =  tableauSpots[i][j-1] * exp((v3 - v6 - ((v2**2) / 2)) * timeStep + (v2 * sqrt(timeStep) * z))
            u = random.random()
          
   #Calcul du prix de l'option et l'écart-type de la simulation
   tableauResults = [[0] * (1) for _ in range(v8)]
   priceCum = 0
   for i in range (v8):
       tableauResults[i] = max(v5 - tableauSpots[i][v7], 0) * exp(-v3 * v4)
       priceCum = priceCum + tableauResults[i]
      
   price = priceCum / v8
   standardDeviation = statistics.stdev(tableauResults) / sqrt(v8)

   return price, standardDeviation, tableauSpots



def monteCarloEuropeanMertonJumpDiffusionCall(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12):
# Cette fonction renvoie le prix d'une option européenne d'achat via Monte Carlo avec le modèle Merton Jump Diffusion
#
# INPUTS
#----------------------------------------------------------------
# v1 : prix au comptant
# v2 : volatilité
# v3 : taux d'intérêt sans risque
# v4 : maturité
# v5 : prix d'exercice
# v6 : dividendes
# v7 : nombre d'itérations
# v8 : nombre de simulations
# v9 : fixation de l'aléa
# v10: fréquence de saut par an 
# v11: moyenne des mouvements liée au saut
# v12: volatilité liée au saut
#
# OUTPUT
#----------------------------------------------------------------
#
# Prix de l'option d'achat, l'écart type et les paths
#
#----------------------------------------------------------------

   timeStep = v4/v7 #le pas d'itération
   kappa = exp(v11) - 1
   drift = v3 - v6 - (v10*kappa) - (0.5*(v2**2)) #la tendance
 
   # Fixe le générateur de nombre aléatoire
   random.seed(v9)
   u = random.random()

   #Tableau contenant le passage du temps
   global tableauTime
   tableauTime = [[0] * (1) for _ in range(v7+1)]
   tableauTime[0] = 0 #Initialisation
   for i in range(1,v7+1):
       tableauTime[i] = tableauTime[i-1] + timeStep

   global tableauSpots
   tableauSpots = [[0] * (v7+1) for _ in range(v8)]
    
   #Simulation de Monte Carlo avec le modèle de Merton
   for i in range (v8):
      tableauSpots[i][0] = v1
      for j in range (1,v7+1):
          jj = 0
          if v10 != 0: 
             N_tt = int(stats.poisson.ppf(u, v10 * timeStep))
             if N_tt > 0:
                for S in range(1,N_tt+1):
                    u = random.random()
                    jj = jj +  stats.norm.ppf(u, v11 - ((v12**2)) / 2, v12)
          u = random.random()
          z = stats.norm.ppf(random.random(), 0, 1)
          tableauSpots[i][j] = tableauSpots[i][j-1] * exp((drift * timeStep) + (v2 * sqrt(timeStep) * z) + jj)
 

   #Calcul du prix de l'option et l'écart-type de la simulation
   tableauResults = [[0] * (1) for _ in range(v8)]
   priceCum = 0
   for i in range(v8):
       tableauResults[i] = max(tableauSpots[i][v7] - v5, 0) * exp(-v3 * v4)
       priceCum = priceCum + tableauResults[i]
     
   price = priceCum / v8
   standardDeviation = statistics.stdev(tableauResults) / sqrt(v8)
 
   return price, standardDeviation, tableauSpots



def monteCarloEuropeanMertonJumpDiffusionPut(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12):
# Cette fonction renvoie le prix d'une option européenne de vente via Monte Carlo avec le modèle Merton Jump Diffusion
#
# INPUTS
#----------------------------------------------------------------
# v1 : prix au comptant
# v2 : volatilité
# v3 : taux d'intérêt sans risque
# v4 : maturité
# v5 : prix d'exercice
# v6 : dividendes
# v7 : nombre d'itérations
# v8 : nombre de simulations
# v9 : fixation de l'aléa
# v10: fréquence de saut par an 
# v11: moyenne des mouvements liée au saut
# v12: volatilité liée au saut
#
# OUTPUT
#----------------------------------------------------------------
#
# Prix de l'option de vente, l'écart type et les paths
#
#----------------------------------------------------------------

   timeStep = v4/v7 #le pas d'itération
   kappa = exp(v11) - 1
   drift = v3 - v6 - (v10*kappa) - (0.5*(v2**2)) #la tendance
 
   # Fixe le générateur de nombre aléatoire
   random.seed(v9)
   u = random.random()

   #Tableau contenant le passage du temps
   global tableauTime
   tableauTime = [[0] * (1) for _ in range(v7+1)]
   tableauTime[0] = 0 #Initialisation
   for i in range(1,v7+1):
       tableauTime[i] = tableauTime[i-1] + timeStep

   global tableauSpots
   tableauSpots = [[0] * (v7+1) for _ in range(v8)]
    
   #Simulation de Monte Carlo avec le modèle de Merton
   for i in range (v8):
      tableauSpots[i][0] = v1
      for j in range (1,v7+1):
          jj = 0
          if v10 != 0: 
             N_tt = int(stats.poisson.ppf(u, v10 * timeStep))
             if N_tt > 0:
                for S in range(1,N_tt+1):
                    u = random.random()
                    jj = jj +  stats.norm.ppf(u, v11 - ((v12**2)) / 2, v12)
          u = random.random()
          z = stats.norm.ppf(random.random(), 0, 1)
          tableauSpots[i][j] = tableauSpots[i][j-1] * exp((drift * timeStep) + (v2 * sqrt(timeStep) * z) + jj)
 

   #Calcul du prix de l'option et l'écart-type de la simulation
   tableauResults = [[0] * (1) for _ in range(v8)]
   priceCum = 0
   for i in range(v8):
       tableauResults[i] = max(v5 - tableauSpots[i][v7], 0) * exp(-v3 * v4)
       priceCum = priceCum + tableauResults[i]
       
   price = priceCum / v8
   standardDeviation = statistics.stdev(tableauResults) / sqrt(v8)
 
   return price, standardDeviation, tableauSpots
