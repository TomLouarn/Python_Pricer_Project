import numpy_financial as npf
import pandas as pd

from pandas.tseries.offsets import DateOffset
from datetime import datetime
from dateutil.relativedelta import relativedelta


def bond_calculation(principal,couponRate,settF,cpnDate,dataRatesCurve):
# Cette fonction calcule le prix, le YTM, la duration, la duration modifiée et la convexité d'un bond
#
# INPUTS
#------------------------------------------------------------------------------
# principal       : principal du bond
# couponRate      : le coupon du bond en pourcentage
# settF           : la fréquence du détachement des coupons
# cpnDate         : la date du dernier détachement de coupon
# dataRatesCurve  : matrice de taux
#------------------------------------------------------------------------------
# OUTPUTS
#------------------------------------------------------------------------------
# prix             : prix du bond en pourcentage du nominal 
# YTM              : yield to maturity (Taux Rendement Actuariel)
# macDuration      : duration Macaulay
# modDuration      : modified duration
# conv             : convexity
# sensi            : sensibilité du bond (modDuration + conv) si shift d'un bp
# fluxBond         : flux du bond
#------------------------------------------------------------------------------

    #Ajustement du format des dates:
    startDate = datetime.today()
    startDate = startDate.replace(hour=0, minute=0, second=0, microsecond=0)
    endDate = datetime.strptime(cpnDate, '%m/%d/%y')

    #Nombre de mois sur la période:
    months = (endDate.year - startDate.year)*12 + endDate.month - startDate.month

    #Ajustement en fonction des fréquences de roll:
    if settF == "Annual":
        ii = 1
        period = 12
    elif settF == "Semi-Annual":
        ii = 1/2
        period = 6
    elif settF == "Quarterly":
        ii = 1/4
        period = 3
    elif settF == "Monthly":
        ii = 1/12
        period = 1
    elif settF == "Zero-Coupon":
        ii = 1
        period = months


    #Flow tab:
    datesRoll = pd.DatetimeIndex([endDate - DateOffset(months=e) for e in range(0, months, period)][::-1]).insert(0, startDate)
  
    nbrDays = datesRoll[1:] - datesRoll[:-1]
    nbrDays = pd.DataFrame(data=nbrDays.days, columns=["Days"])

    startDates = pd.DataFrame(data=datesRoll[:-1], columns=["Start"])
    endDates = pd.DataFrame(data=datesRoll[1:], columns=["End"])

    #on décale les dates de paiement au prochain jour ouvré si close day:
    paymentDates = datesRoll[1:]
    for i, date in enumerate(paymentDates):
        if date.weekday() >= 5: # Saturday or Sunday
            paymentDates = paymentDates.delete(i)
            paymentDates = paymentDates.insert(i, date + pd.offsets.BDay())

    nbrDaysPay=paymentDates-pd.Timestamp(date.today())        
    nbrDaysPay=pd.DataFrame(data=nbrDaysPay.days, columns=["CumDays"])
    paymentDates=pd.DataFrame(data=paymentDates, columns=["Payment Date"])

    finalResults=pd.concat([startDates, endDates], axis=1) #start et end dates
    finalResults=pd.concat([finalResults, nbrDays], axis=1) #nbr de jours par période
    finalResults['Rate'] = couponRate
    finalResults['Nominal'] = principal 
    finalResults=pd.concat([finalResults, paymentDates], axis=1) # payment dates
    #finalResults['Flows'] = round(finalResults['Rate'] * ii * finalResults['Nominal'] / 100,2) #flows

    nbrDaysFullPeriod = datesRoll[1:] - (datesRoll[1:] + pd.DateOffset(months=-period))
    nbrDaysFullPeriod = pd.DataFrame(data=nbrDaysFullPeriod.days, columns=['Days'])
    finalResults['Flows'] = round(finalResults['Rate'] * ii * finalResults['Nominal'] * finalResults['Days'] / nbrDaysFullPeriod['Days'] / 100,2) #flows
    finalResults.loc[len(finalResults)-1, 'Flows'] = finalResults.loc[len(finalResults)-1, 'Flows'] + principal
    finalResults=pd.concat([finalResults, nbrDaysPay], axis=1) #nbr de jours pour l'actualisation

    #faire l'actualisation des flux -> récupérer le taux sans risque de la date de paiment et divisé le flux par ce taux (1+r)^per
    tableauDiscount = [[0] * (2) for _ in range(len(finalResults))]
    for i in range(len(finalResults)):
        a = finalResults.iloc[i]['Payment Date'].date() 
        a = a.strftime('%Y-%m-%d')
        tableauDiscount[i][0] = a
        tableauDiscount[i][1] = dataRatesCurve.iloc[dataRatesCurve.index.get_loc(a), dataRatesCurve.columns.get_loc('GERMANY')]

    # Convert list to DataFrame
    tableauDiscount_df = pd.DataFrame(tableauDiscount, columns=['Payment Date', 'Zeros'])
    tableauDiscount_df.drop(columns=['Payment Date'], inplace=True)

    finalResults = pd.concat([finalResults, round(tableauDiscount_df,5)], axis=1) #taux ZC
    finalResults['Discount'] = round(1 / ((1+((finalResults['Zeros']*ii/100)))**(finalResults['CumDays']/(360*ii))),5)

    finalResults['PV'] = round(finalResults['Flows'] * finalResults['Discount'],2)

    #prix de l'obligation en pourcentage du nominal
    prix = 100 * sum(finalResults['PV']) / principal

    # Taux de Rendement Actuariel (voir plus en détail comment ils ont développé cette fonction irr)
    if settF == "Zero-Coupon":
        flows = [0 for x in range((endDate.year - startDate.year)-1)]
        flows.append(100)

    else:
        flows = 100 * finalResults['Flows'] / principal
        flows = flows.to_list()

    flows.insert(0, -prix)
    YTM = npf.irr(flows) * 100 / ii
    
    # Macaulay Duration:
    if settF == "Zero-Coupon":
        delta = relativedelta(endDate, startDate)
        years = delta.years
        months = delta.months
        days = delta.days
        macDuration = years + months / 12 + days / 365.25
    else: 
        macDuration = 0 
        for i in range (len(finalResults)):
            macDuration = macDuration + (((i+1)*ii)*finalResults['PV'][i])
        macDuration = macDuration / (principal * prix / 100) 

    # Modified duration
    modDuration = macDuration / (1+(YTM/100))

    # Convexity : 
    conv = 0 
    for i in range (len(finalResults)):
        conv = conv + ((((i+1)*ii)**2)*finalResults['PV'][i])
    conv = conv / (principal * prix / 100) 
    
    # Sensi (shift d'un % - a voir si faut mettre le shift d'un bp plutôt): 
    sensi = ((-modDuration*0.01) + (0.5*conv*0.01*0.01)) * prix


    return prix, YTM , macDuration, modDuration, conv, sensi, finalResults






