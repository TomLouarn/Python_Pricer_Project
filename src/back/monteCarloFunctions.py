from scipy import stats
import statistics
import random
from math import *


def monteCarloEuropeanLogNormalCall(spot, vol, rfr, lif, strp, divy, nts, nos, rans):
# Cette fonction renvoie le prix d'une option européenne d'achat via Monte Carlo avec le modèle log normal

   timeStep = lif / nts #Le pas d'itération

   tableauSpots = [[0] * (nts + 1) for _ in range(nos)]
   
   # Fixe le générateur de nombre aléatoire
   random.seed(rans)
   u = random.random()
   
   #Tableau contenant le passage du temps
   global tableauTime
   tableauTime = [[0] * (1) for _ in range(nts + 1)]
   tableauTime[0] = 0 #Initialisation
   for i in range(1, nts + 1):
       tableauTime[i] = tableauTime[i-1] + timeStep

   #Simulation de Monte Carlo sous l'hypothèse que le sous-jacent suit une distribution log-normale
   for i in range (nos):
       tableauSpots[i][0] = spot
       for j in range (1, nts + 1):
            u = random.random()
            z = stats.norm.ppf(u, 0, 1)
            tableauSpots[i][j] =  tableauSpots[i][j-1] * exp((rfr - divy - ((vol ** 2) / 2)) * timeStep + (vol * sqrt(timeStep) * z))
            u = random.random()
          
   #Calcul du prix de l'option et l'écart-type de la simulation
   tableauResults = [[0] * (1) for _ in range(nos)]
   priceCum = 0
   for i in range (nos):
       tableauResults[i] = max(tableauSpots[i][nts] - strp, 0) * exp(-rfr * lif)
       priceCum = priceCum + tableauResults[i]
   
   price = priceCum / nos
   standardDeviation = statistics.stdev(tableauResults) / sqrt(nos)
   
   return price, standardDeviation, tableauSpots


def monteCarloEuropeanLogNormalPut(spot, vol, rfr, lif, strp, divy, nts, nos, rans):
# Cette fonction renvoie le prix d'une option européenne de vente via Monte Carlo avec le modèle log normal


   timeStep = lif / nts #Le pas d'itération

   global tableauSpots
   tableauSpots = [[0] * (nts + 1) for _ in range(nos)]
   
   # Fixe le générateur de nombre aléatoire
   random.seed(rans)
   u = random.random()
   
   #Tableau contenant le passage du temps
   global tableauTime
   tableauTime = [[0] * (1) for _ in range(nts + 1)]
   tableauTime[0] = 0 #Initialisation
   for i in range(1, nts + 1):
       tableauTime[i] = tableauTime[i-1] + timeStep

   #Simulation de Monte Carlo sous l'hypothèse que le sous-jacent suit une distribution log-normale
   for i in range (nos):
       tableauSpots[i][0] = spot
       for j in range (1, nts + 1):
            u = random.random()
            z = stats.norm.ppf(u, 0, 1)
            tableauSpots[i][j] =  tableauSpots[i][j-1] * exp((rfr - divy - ((vol ** 2) / 2)) * timeStep + (vol * sqrt(timeStep) * z))
            u = random.random()
          
   #Calcul du prix de l'option et l'écart-type de la simulation
   tableauResults = [[0] * (1) for _ in range(nos)]
   priceCum = 0
   for i in range (nos):
       tableauResults[i] = max(strp - tableauSpots[i][nts], 0) * exp(-rfr * lif)
       priceCum = priceCum + tableauResults[i]
      
   price = priceCum / nos
   standardDeviation = statistics.stdev(tableauResults) / sqrt(nos)

   return price, standardDeviation, tableauSpots



def monteCarloEuropeanMertonJumpDiffusionCall(spot, vol, rfr, lif, strp, divy, nts, nos, rans, fja, avgm, jvol):
# Cette fonction renvoie le prix d'une option européenne d'achat via Monte Carlo avec le modèle Merton Jump Diffusion
#


   timeStep = lif / nts #le pas d'itération
   kappa = exp(avgm) - 1
   drift = rfr - divy - (fja * kappa) - (0.5 * (vol ** 2)) #la tendance
 
   # Fixe le générateur de nombre aléatoire
   random.seed(rans)
   u = random.random()

   #Tableau contenant le passage du temps
   global tableauTime
   tableauTime = [[0] * (1) for _ in range(nts + 1)]
   tableauTime[0] = 0 #Initialisation
   for i in range(1, nts + 1):
       tableauTime[i] = tableauTime[i-1] + timeStep

   global tableauSpots
   tableauSpots = [[0] * (nts + 1) for _ in range(nos)]
    
   #Simulation de Monte Carlo avec le modèle de Merton
   for i in range (nos):
      tableauSpots[i][0] = spot
      for j in range (1, nts + 1):
          jj = 0
          if fja != 0:
             N_tt = int(stats.poisson.ppf(u, fja * timeStep))
             if N_tt > 0:
                for S in range(1,N_tt+1):
                    u = random.random()
                    jj = jj +  stats.norm.ppf(u, avgm - ((jvol ** 2)) / 2, jvol)
          u = random.random()
          z = stats.norm.ppf(random.random(), 0, 1)
          tableauSpots[i][j] = tableauSpots[i][j-1] * exp((drift * timeStep) + (vol * sqrt(timeStep) * z) + jj)
 

   #Calcul du prix de l'option et l'écart-type de la simulation
   tableauResults = [[0] * (1) for _ in range(nos)]
   priceCum = 0
   for i in range(nos):
       tableauResults[i] = max(tableauSpots[i][nts] - strp, 0) * exp(-rfr * lif)
       priceCum = priceCum + tableauResults[i]
     
   price = priceCum / nos
   standardDeviation = statistics.stdev(tableauResults) / sqrt(nos)
 
   return price, standardDeviation, tableauSpots



def monteCarloEuropeanMertonJumpDiffusionPut(spot, vol, rfr, lif, strp, divy, nts, nos, rans, fja, avgm, jvol):
# Cette fonction renvoie le prix d'une option européenne de vente via Monte Carlo avec le modèle Merton Jump Diffusion


   timeStep = lif / nts #le pas d'itération
   kappa = exp(avgm) - 1
   drift = rfr - divy - (fja * kappa) - (0.5 * (vol ** 2)) #la tendance
 
   # Fixe le générateur de nombre aléatoire
   random.seed(rans)
   u = random.random()

   #Tableau contenant le passage du temps
   global tableauTime
   tableauTime = [[0] * (1) for _ in range(nts + 1)]
   tableauTime[0] = 0 #Initialisation
   for i in range(1, nts + 1):
       tableauTime[i] = tableauTime[i-1] + timeStep

   global tableauSpots
   tableauSpots = [[0] * (nts + 1) for _ in range(nos)]
    
   #Simulation de Monte Carlo avec le modèle de Merton
   for i in range (nos):
      tableauSpots[i][0] = spot
      for j in range (1, nts + 1):
          jj = 0
          if fja != 0:
             N_tt = int(stats.poisson.ppf(u, fja * timeStep))
             if N_tt > 0:
                for S in range(1,N_tt+1):
                    u = random.random()
                    jj = jj +  stats.norm.ppf(u, avgm - ((jvol ** 2)) / 2, jvol)
          u = random.random()
          z = stats.norm.ppf(random.random(), 0, 1)
          tableauSpots[i][j] = tableauSpots[i][j-1] * exp((drift * timeStep) + (vol * sqrt(timeStep) * z) + jj)
 

   #Calcul du prix de l'option et l'écart-type de la simulation
   tableauResults = [[0] * (1) for _ in range(nos)]
   priceCum = 0
   for i in range(nos):
       tableauResults[i] = max(strp - tableauSpots[i][nts], 0) * exp(-rfr * lif)
       priceCum = priceCum + tableauResults[i]
       
   price = priceCum / nos
   standardDeviation = statistics.stdev(tableauResults) / sqrt(nos)
 
   return price, standardDeviation, tableauSpots
