# Interface graphique avec Tkinter------------------------------------------------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
from turtle import bgcolor, color

from src.back.pricer import *
from src.front.window import WindowMain


# N'est pas exécuté lors de l'import
if __name__ == '__main__':
    #Création de la fenêtre intéractive
    fenetre = WindowMain()
    
    tab1 = fenetre.get_tab(name='Options calculator')
    tab2 = fenetre.get_tab(name='Monte Carlo')
    tab3 = fenetre.get_tab(name='Bonds calculator') 
    tab4 = fenetre.get_tab(name='Swaps calculator')
    tab5 = fenetre.get_tab(name='Rates Curve')

    fenetre.notebook.pack(expand = 1, fill ="both")

    #Options calculator widgets - tab1--------------------------------------------------------------------------------------------------------------------------------------------------------
    tab1.label_titre.grid(column = 1,row = 0,padx = 20,pady = 20)

    def callback_option_calculation():
        ut2 = tab1.ut.get()
        stop2 = tab1.stop.get()
        vol2 = tab1.vol.get() / 100
        rfr2 = tab1.rfr.get() / 100
        ot2 = tab1.ot.get()
        lif2 = tab1.lif.get()
        strp2 = tab1.strp.get()
        valueRB2 = tab1.valueRB.get()
        valueCB2 = tab1.valueCB.get()
        
        #optional values
        ov1 = tab1.optionalEntry1.get()
        ov2 = tab1.optionalEntry2.get()
        ov3 = tab1.optionalEntry3.get()
        pri2 = tab1.valuePrice.get() 
        
        if valueCB2 == 0: 
             price, delta, gamma, vega, theta, rho = option_calculation(ut2,stop2,vol2,rfr2,ot2,lif2,strp2,valueRB2,valueCB2,ov1,ov2,ov3)
             tab1.valuePrice.set(round(price,5))
             tab1.valueDelta.set(round(delta,5))
             tab1.valueGamma.set(round(gamma,5))
             tab1.valueVega.set(round(vega,5))
             tab1.valueTheta.set(round(theta,5))
             tab1.valueRho.set(round(rho,5))

        elif valueCB2 == 1:
             vol = option_calculation_impliedVolatility(ut2,stop2,pri2,rfr2,ot2,lif2,strp2,valueRB2,valueCB2)
             tab1.vol.set(round(vol,5))

    ttk.Button(tab1,text = "CALCULATE",command=callback_option_calculation).grid(column = 0,row = 11,padx = 12,pady = 12)


    #Monte Carlo widgets - tab2--------------------------------------------------------------------------------------------------------------------------------------------------------
    tab2.label_titre.grid(columnspan = 5,row = 0,padx = 20,pady = 20)

    def callback_option_calculation_tab2():
        ut2_tab2 = tab2.ut_tab2.get()
        stop2_tab2 = tab2.stop_tab2.get()
        vol2_tab2 = tab2.vol_tab2.get() / 100
        rfr2_tab2 = tab2.rfr_tab2.get() / 100
        ot2_tab2 = tab2.ot_tab2.get()
        mt2_tab2 = tab2.mt_tab2.get()
        lif2_tab2 = tab2.lif_tab2.get()
        strp2_tab2 = tab2.strp_tab2.get()
        valueRB2_tab2 = tab2.valueRB_tab2.get()
        divy2_tab2 = tab2.divy_tab2.get() / 100
        nts2_tab2 = tab2.nts_tab2.get()
        nos2_tab2 = tab2.nos_tab2.get()
        rans2_tab2 = tab2.rans_tab2.get()

        #optional values
        ov1_tab2 = tab2.optionalEntry1_tab2.get()
        ov2_tab2 = tab2.optionalEntry2_tab2.get() / 100
        ov3_tab2 = tab2.optionalEntry3_tab2.get() / 100
     
        price, standardDeviation, tableauSpots = option_calculation_tab2(ut2_tab2,stop2_tab2,vol2_tab2,rfr2_tab2,ot2_tab2,mt2_tab2,lif2_tab2,strp2_tab2,valueRB2_tab2,divy2_tab2,nts2_tab2,nos2_tab2,rans2_tab2,ov1_tab2,ov2_tab2,ov3_tab2)
        tab2.valuePrice_tab2.set(round(price,5))
        tab2.valueSD_tab2.set(round(standardDeviation,5))
        
        #à corriger j'ai dix charts ou lieu d'un de dix !!!!!!!!!!!!!!!!!!!!!!!!!
        for i in range(min(nts2_tab2,10)):
            plt.plot(tableauSpots[i]) 
            plt.title('First Ten Simulation Trials')
            plt.xlabel('Time')
            plt.ylabel('Stock Price')
            plt.show()

    ttk.Button(tab2,text = "CALCULATE", command=callback_option_calculation_tab2).grid(column = 0,row = 13,padx = 1,pady = 11)


    #Bonds calculator widgets - tab3--------------------------------------------------------------------------------------------------------------------------------------------------------
    import pandas as pd
    tab3.label_titre.grid(columnspan = 4,row = 0,padx = 20,pady = 20) 

    def callback_bond_calculation_tab3():
        
        #courbes de taux:
        data = pd.read_excel('C:/Users/paul/OneDrive/Bureau/python/Pricer Python/ratesCurve.xlsx')
        dataRatesCurve = refreshCurve2(data)

        #récupération des inputs:
        prin2_tab3 = tab3.prin_tab3.get()
        cour2_tab3 = tab3.cour_tab3.get()
        setf2_tab3 = tab3.setf_tab3.get()
        couponDate_tab3 = tab3.couponDate_tab3.get() 

        global flows

        prix, YTM , macDuration, modDuration, conv, sensi, flows = bond_calculation(prin2_tab3, cour2_tab3, setf2_tab3, couponDate_tab3,dataRatesCurve)

        tab3.pric_tab3.set(round(prix,2))
        tab3.ytm_tab3.set(round(YTM,2))
        tab3.dur_tab3.set(round(macDuration,2))
        tab3.mdur_tab3.set(round(modDuration,2))
        tab3.con_tab3.set(round(conv,2))
        tab3.sen_tab3.set(round(sensi,2))

    ttk.Button(tab3,text = "CALCULATE", command=callback_bond_calculation_tab3).grid(column = 3,row = 16,padx = 1,pady = 11)

    #à revoir et à mettre au bon endroit + permettre le copier coller ? + mettre en commun avec tab4 (faire une classe?)
    def flows_display_tab3(tab):
        mywin=Tk()
        mywin.geometry('1650x400')

        df_list=list(tab.columns.values)
        df_rset=tab.to_numpy().tolist()
        df_tree=ttk.Treeview(mywin,columns=df_list)
        df_tree.pack()
    
        for i in df_list:
            df_tree.column(i,width=100,anchor='c')
            df_tree.heading(i,text=i)
        for dt in df_rset:
            v=[r for r in dt]
            df_tree.insert('','end',iid=v[0], values=v)

        mywin.mainloop()

    def callback_display_flows_tab3():
        flows_display_tab3(flows)

    ttk.Button(tab3,text = "Flows", command=callback_display_flows_tab3).grid(column = 1,row = 7,padx = 1,pady = 1)


    #Swaps calculator widgets - tab4--------------------------------------------------------------------------------------------------------------------------------------------------------
    import pandas as pd
 
    tab4.label_titre.grid(columnspan = 4,row = 0,padx = 20,pady = 20) 
     
    #idée: aller chercher les tenors sur internet via API ????
    def callback_option_calculation_1_tab4():
        dataToCopy = pd.read_excel('C:/Users/paul/OneDrive/Bureau/python/Pricer Python/ratesCurve.xlsx', header = None)
        for i in range(7):  # Boucle sur les colonnes de votre DataFrame (7 colonnes dans cet exemple)
        # Convertir les valeurs de la colonne en une chaîne de texte sans indexation
            col_str = dataToCopy.iloc[:20, i].to_string(index=False)
            ttk.Label(tab5, text=col_str).grid(column=i, row=2)
        
        data = pd.read_excel('C:/Users/paul/OneDrive/Bureau/python/Pricer Python/ratesCurve.xlsx')
        dataRatesCurve = refreshCurve(data)

    ttk.Button(tab4,text = "Refresh Curve", command=callback_option_calculation_1_tab4).grid(column = 0,row = 14,padx = 1,pady = 1)
    

    def callback_option_calculation_2_tab4():

        data = pd.read_excel('C:/Users/paul/OneDrive/Bureau/python/Pricer Python/ratesCurve.xlsx')
        dataRatesCurve = refreshCurve2(data)
        
        startDate_tab4 = tab4.startDate_tab4.get() #4/9/24
        endDate_tab4 = tab4.endDate_tab4.get() #4/9/24
        valueRB_tab4 = tab4.valueRB_tab4.get()  #vaut 0 actuellement quand on rec
        not1_tab4 =tab4.not1_tab4.get()
        not2_tab4 = tab4.not2_tab4.get()
        rat1_tab4 = tab4.rat1_tab4.get()
        setf1_tab4 = tab4.setf1_tab4.get()
        bas1_tab4 = tab4.bas1_tab4.get()
        fr2_tab4 = tab4.fr2_tab4.get()
        setf2_tab4 = tab4.setf2_tab4.get()
        bas2_tab4 = tab4.bas2_tab4.get()
        lase_tab4 = tab4.lase_tab4.get() 

        global tab1
        global tab2
        global tab22

        priceSwap, dv01, priceFixed, priceFloat, tab1, tab2, tab22 = swapComputation(startDate_tab4,endDate_tab4,valueRB_tab4,not1_tab4,not2_tab4,rat1_tab4,fr2_tab4,setf1_tab4,setf2_tab4,bas1_tab4,bas2_tab4,lase_tab4,dataRatesCurve)
        tab4.pri1_tab4.set(round(priceFixed,5))
        tab4.pri2_tab4.set(round(priceFloat,5))
        tab4.sen_tab4.set(round(dv01,5))
        tab4.sPri_tab4.set(round(priceSwap,5))

    ttk.Button(tab4,text = "CALCULATE",command=callback_option_calculation_2_tab4).grid(column = 0,row = 15,padx = 1,pady = 1)

    
    def callback_option_calculation_3_tab4():
        data = pd.read_excel('C:/Users/paul/OneDrive/Bureau/python/Pricer Python/ratesCurve.xlsx')
        dataRatesCurve = refreshCurve2(data)

        startDate_tab4 = tab4.startDate_tab4.get()
        endDate_tab4 = tab4.endDate_tab4.get()
        valueRB_tab4 = tab4.valueRB_tab4.get()
        not1_tab4 =tab4.not1_tab4.get()
        not2_tab4 = tab4.not2_tab4.get()
        
        setf1_tab4 = tab4.setf1_tab4.get()
        bas1_tab4 = tab4.bas1_tab4.get()
        fr2_tab4 = tab4.fr2_tab4.get()
        setf2_tab4 = tab4.setf2_tab4.get()
        bas2_tab4 = tab4.bas2_tab4.get()
        lase_tab4 = tab4.lase_tab4.get() 

        #calcul du flat rate
        df = dataRatesCurve[fr2_tab4]
        rat1_tab4 = df.mean()
        
        priceSwap, dv01, priceFixed, priceFloat, tab1, tab2, tab22 = swapComputation(startDate_tab4,endDate_tab4,valueRB_tab4,not1_tab4,not2_tab4,rat1_tab4,fr2_tab4,setf1_tab4,setf2_tab4,bas1_tab4,bas2_tab4,lase_tab4,dataRatesCurve)
    
        rateShift = priceSwap / dv01 / 100
        flatRate = rat1_tab4 + rateShift

        tab4.flatRate_tab4.set(round(flatRate,5))


    ttk.Button(tab4,text = "CALCULATE",command=callback_option_calculation_3_tab4).grid(column = 0,row = 18,padx = 1,pady = 1)


    #à revoir et à mettre au bon endroit + permettre le copier coller ? 
    def flows_display_tab4(tab):
        mywin=Tk()
        mywin.geometry('1650x400')

        df_list=list(tab.columns.values)
        df_rset=tab.to_numpy().tolist()
        df_tree=ttk.Treeview(mywin,columns=df_list)
        df_tree.pack()
    
        for i in df_list:
            df_tree.column(i,width=100,anchor='c')
            df_tree.heading(i,text=i)
        for dt in df_rset:
            v=[r for r in dt]
            df_tree.insert('','end',iid=v[0], values=v)

        mywin.mainloop()


    def callback_display_fixed_tab4():
        flows_display_tab4(tab1)

    def callback_display_float_tab4():
        flows_display_tab4(tab2)


    ttk.Button(tab4,text = "Fixed flows", command=callback_display_fixed_tab4).grid(column = 0,row = 3,padx = 1,pady = 1)

    ttk.Button(tab4,text = "Float flows", command=callback_display_float_tab4).grid(column = 2,row = 3,padx = 1,pady = 1)


    #Swaps Rates Curve - tab5--------------------------------------------------------------------------------------------------------------------------------------------------------

    tab5.label_titre.grid(columnspan = 6,row = 0,padx = 20,pady = 20) 


    #Affichage de la fenêtre intéractive
    fenetre.mainloop()
