"""
Created on Sun Apr  5 12:06:56 2020

@author: corentinguery
"""

import matplotlib.pyplot as plt
import numpy as np
import random as rd


### Affichage profil d'un tabeau Scenario * Temps
def PlotTableauScenarioxT(Tab,unite,titre, labl):
    """ 
    Tab is a (N,T) vector. Each line correspond to a scenario and each column to a time t.
    This function plots a grouped bar diagram with the average values of the vector for each t.
    For the path_to_folder, mind putting '\\' instead of '/'.
    """
    N=int(Tab.size/Tab[0].size)
    T=int(Tab.size/N)
    TabL=np.zeros(T) #vector with the average values for each t
    E=np.zeros(T) #vector with the STD for each t
    Total=0
    
    for t in range(T):
        TabL[t]=np.mean(Tab[:,t])
        E[t]=np.std(Tab[:,t])
        Total+=TabL[t]
        
    ind=np.arange(T)
    width=0.15

    p1=plt.bar(ind, TabL, 3*width, color='r', bottom=0,label = labl, yerr=E)
    plt.ylabel(unite)
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    plt.title(titre)
    plt.grid(True)
    
    plt.show()
        

"""
### Chargement des fichiers 
#Pour tous les acteurs
bill=np.load("C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\PIR\\16-05-2019-S2\\16-05-2019-S2\\bill.npy")
#Pour DC et SB
heat_trans=np.load("C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\PIR\\16-05-2019-S2\\16-05-2019-S2\\heat_transactions.npy")
#Pour tous les acteurs
load=np.load("C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\PIR\\16-05-2019-S2\\16-05-2019-S2\\load.npy")
#Pour tous les acteurs sauf DC
stock=np.load("C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\PIR\\16-05-2019-S2\\16-05-2019-S2\\stock.npy")
#Buy prices
buy_prices=np.load("C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\PIR\\16-05-2019-S2\\16-05-2019-S2\\buy_prices.npy")
#Sell prices
sell_prices=np.load("C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\PIR\\16-05-2019-S2\\16-05-2019-S2\\sell_prices.npy")
#Grid prices
grid_prices=np.load("C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\PIR\\16-05-2019-S2\\16-05-2019-S2\\grid_prices.npy")
"""
"""
### Explotation des fichers (affichages et valeurs)

## Facture Par Joueur
#print(plotDetailedData(bill[0,:,:],bill[1,:,:],bill[2,:,:],bill[3,:,:],bill[4,:,:],"bill","€","C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Detailled bill"))

## Transactions de chaleur
#plotDetailedData1(heat_trans[0,1,:],heat_trans[1,1,:],"C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Detailled heat transactions")

## Charge par joueur
##print(plotDetailedData(load[0,:,:],load[1,:,:],load[2,:,:],load[3,:,:],load[4,:,:],"load","kWh","C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Detailled load"))

## Stock par joueur
#print(plotDetailedData2(stock[0,:,:],stock[1,:,:],stock[2,:,:],stock[3,:,:],"stock","kWh","C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Detailled stock"))

## Facture et charge totale
#PlotTotalAverage(bill,load,"C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Total bill and load")

## Prix de vente et d'achat
#PlotAveragePrices(grid_prices,"C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Prices")

## Prix d'achat
#print(PlotPrices(buy_prices,"C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Detailled buying prices"))

## Prix de vente
#print(PlotPrices(sell_prices,"C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Detailled selling prices"))
"""
