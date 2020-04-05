#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 12:06:56 2020

@author: corentinguery
"""

import matplotlib.pyplot as plt
import numpy as np
import random as rd

T=48

### Affichage de la facture et de la charge POUR CHAQUE JOUEUR


def plotDetailedData(CS,IS,SF,PRICE,flexible_load,unite):
    """ 
    CS, IS, SF and PRICE are (N,T) vectors. Each vector corresponds to an actor and each line correspond to a scenario and each column to a time t.
    This function plots a grouped bar diagram with the average values of load for each t for each actor.
    For the path_to_folder, mind putting '\\' instead of '/'.
    """
    N=int(CS.size/CS[0].size)
    
    CSL,ISL,SFL,PRICEL=np.zeros(T),np.zeros(T),np.zeros(T),np.zeros(T)#vector with the average loads for each t
    E1,E2,E3,E4=np.zeros(T),np.zeros(T),np.zeros(T),np.zeros(T) #vector with the standard deviations of load for each t
    Total_CS,Total_IS,Total_SF,Total_PRICE=0,0,0,0
    for t in range (T):
        cs,i_s,sf,price=0,0,0,0
        for n in range (N):       
        ##ici je transfere mes tableau dans des listes pour convertir le grand 
        ##nombre de données en une seule (moyenne)
            cs+=CS[n,t]
            i_s+=IS[n,t]
            sf+=SF[n,t]
            price+=PRICE[n,t]
       
        ##moyenne des scenario a chaque fois 
        CSL[t]=cs/N              
        ISL[t]=i_s/N
        SFL[t]=sf/N
        PRICEL[t]=price/N
        
        ##calcule des variance à chaque fois
        E1[t]=np.std(CS[:,t])   
        E2[t]=np.std(IS[:,t])
        E3[t]=np.std(SF[:,t])
        E4[t]=np.std(PRICE[:,t])
        
        ##calcul des charges totale sur 1 journées
        Total_CS+=CSL[t]
        Total_IS+=ISL[t]
        Total_SF+=SFL[t]
        Total_PRICE+=PRICEL[t]
    
    ind=np.arange(T)
    width=0.15

    plt.subplot(5,1,1)
    p1=plt.bar(ind, CSL, 3*width, color='r', bottom=0,label = "CS", yerr=E1)
    plt.ylabel(unite)
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    plt.title('Average '+ flexible_load  +' by actor and by time')
    plt.grid(True)
    
    plt.subplot(5,1,2)
    p2=plt.bar(ind, ISL, 3*width, color='b', bottom=0, label="DC",yerr=E2)
    plt.ylabel(unite)
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    plt.grid(True)
    
    plt.subplot(5,1,3)
    p3=plt.bar(ind, SFL, 3*width, color='g', bottom=0, label="SB",yerr=E3)
    plt.ylabel(unite)
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    plt.grid(True)
    
    plt.subplot(5,1,4)
    p4=plt.bar(ind, PRICEL, 3*width, color='y', bottom=0, label="SF_1",yerr=E4)
    plt.ylabel(unite)
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    plt.grid(True)
        
    plt.show()    
       
    ##plt.savefig(path_to_folder)
    ##return ("CS : "+str(round(A1,3))+", DC : "+str(round(A2,3))+", SB : "+str(round(A3,3))+", SF_1 : "+str(round(A4,3))+", SF_2 : "+str(round(A5,3))+" (en "+unite+")")
    
### Affichage des échanges de chaleur (et de leurs prix) POUR SB ET DC


def plotDetailedData1(A,B,path_to_folder):
    """ 
    
    For the path_to_folder, mind putting '\\' instead of '/'.
    """
    
    ind=np.arange(T)
    width=0.15

    plt.subplot(2,1,1)
    p1=plt.bar(ind, A, 3*width, color='r', bottom=0, label="heat exchanged")
    plt.ylabel("kWh")
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    plt.title('Heat transactions')
    
    plt.subplot(2,1,2)
    p2=plt.bar(ind, B, 3*width, color='b', bottom=0, label="Price of exchange")
    plt.ylabel("€")
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    
    plt.savefig(path_to_folder)
    
    
### Affichage du stock POUR TOUS LES JOUEURS SAUF DC

def plotDetailedData2(A,B,C,D,flexible_load,unite,path_to_folder):
    """ 
    A, B, C and D are (N,T) vectors. Each vector corresponds to an actor and each line correspond to a scenario and each column to a time t.
    This function plots a grouped bar diagram with the average values of load for each t for each actor.
    For the path_to_folder, mind putting '\\' instead of '/'.
    """
    N=int(A.size/A[0].size)
    
    AL1,AL2,AL3,AL4=np.zeros(T),np.zeros(T),np.zeros(T),np.zeros(T) #vector with the average loads for each t
    E1,E2,E3,E4=np.zeros(T),np.zeros(T),np.zeros(T),np.zeros(T) #vector with the standard deviations of load for each t
    A1,A2,A3,A4=0,0,0,0
    for t in range (T):
        a,b,c,d=0,0,0,0
        for n in range (N):
            a+=A[n,t]
            b+=B[n,t]
            c+=C[n,t]
            d+=D[n,t]
        AL1[t]=a/N
        AL2[t]=b/N
        AL3[t]=c/N
        AL4[t]=d/N
        E1[t]=np.std(A[:,t])
        E2[t]=np.std(B[:,t])
        E3[t]=np.std(C[:,t])
        E4[t]=np.std(D[:,t])
        A1+=AL1[t]
        A2+=AL2[t]
        A3+=AL3[t]
        A4+=AL4[t]
    A1,A2,A3,A4=A1/T,A2/T,A3/T,A4/T
    ind=np.arange(T)
    width=0.15

    plt.subplot(4,1,1)
    p1=plt.bar(ind, AL1, 3*width, color='r', bottom=0, label="CS",yerr=E1)
    plt.ylabel(unite)
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    plt.title('Average '+ flexible_load  +' by actor and by time')
    
    plt.subplot(4,1,2)
    p2=plt.bar(ind, AL2, 3*width, color='b', bottom=0, label="SB",yerr=E2)
    plt.ylabel(unite)
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    
    plt.subplot(4,1,3)
    p3=plt.bar(ind, AL3, 3*width, color='g', bottom=0, label="SF_1",yerr=E3)
    plt.ylabel(unite)
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    
    plt.subplot(4,1,4)
    p4=plt.bar(ind, AL4, 3*width, color='y', bottom=0, label="SF_2",yerr=E4)
    plt.ylabel(unite)
    plt.xlim([0,T+5])
    plt.legend(loc='upper right')
    
    plt.savefig(path_to_folder)
    return ("CS : "+str(round(A1,3))+", SB : "+str(round(A2,3))+", SF_1 : "+str(round(A3,3))+", SF_2 : "+str(round(A4,3))+" (en "+unite+")")

### Affichage de la facture et de la charge TOTALE
    
def PlotTotalAverage(Bill,load,path_to_folder):
    N=int(Bill[0].size/Bill[0][0].size)
    
    B=np.zeros(T)
    L=np.zeros(T)
    E1=np.zeros(T)
    E2=np.zeros(T)
    AB=0
    AL=0
    for t in range (T):
        b=0
        l=0
        for n in range (N):
            for acteur in range (5):
                b+=Bill[acteur,n,t]
                l+=load[acteur,n,t]
        B[t]=b/N
        L[t]=l/N
        E1[t]=np.std(Bill[:,:,t])
        E2[t]=np.std(load[:,:,t])
        AB+=B[t]
        AL+=L[t]
    
    ind=np.arange(T)
    width=0.15

    plt.subplot(2,1,1)
    p1=plt.bar(ind, B, 3*width, color='r', bottom=0,yerr=E1)
    plt.ylabel("€")
    plt.xlim([0,T+5])
    plt.title("Average total daily bill ("+str(round(AB,3))+" €)")
    
    plt.subplot(2,1,2)
    p2=plt.bar(ind, L, 3*width, color='b', bottom=0,yerr=E2)
    plt.ylabel("kWh")
    plt.xlim([0,T+5])
    plt.title("Average total daily load ("+str(round(AL,3))+" kWh)")
    
    plt.savefig(path_to_folder)
    
    
### Affichage du prix du kWh
    
def PlotAveragePrices(grid,path_to_folder):
    N=int(grid[0].size/grid[0][0].size)
    
    Sale=np.zeros(T)
    Purchase=np.zeros(T)
    
    for t in range (T):
        p=0
        s=0
        for n in range (N):
            p+=grid[0][n][t]
            s+=grid[1][n][t]
                    
        Sale[t]=s/N
        Purchase[t]=p/N
        
    ind=np.arange(T)
    width=0.15

    plt.subplot(2,1,1)
    p1=plt.bar(ind, Sale, 3*width, color='r', bottom=0)
    plt.ylabel("€")
    plt.xlim([0,T+5])
    plt.title("Sale price")
    
    plt.subplot(2,1,2)
    p2=plt.bar(ind, Purchase, 3*width, color='b', bottom=0)
    plt.ylabel("€")
    plt.xlim([0,T+5])
    plt.title("Purchase price")
    
    plt.savefig(path_to_folder)
    
  
### Affichage des prix d'achat et de vente
    
def PlotPrices(buy,path_to_folder):
    N=int(buy[0].size/buy[0][0].size)
    
    B=np.zeros((5,T))

    for t in range (T):
        
        for acteur in range (5):
            for n in range (N):
                B[acteur,t]+=buy[acteur,n,t]
            B[acteur,t]/=N
        
    barWidth=0.15
    
    r1 = np.arange(T)
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]
    
    plt.bar(r1, B[0], color='r', width=barWidth,  label='CS')
    plt.bar(r2, B[1], color='b', width=barWidth,  label='DC')
    plt.bar(r3, B[2], color='g', width=barWidth,  label='SB')
    plt.bar(r4, B[3], color='y', width=barWidth,  label='SF_1')
    plt.bar(r5, B[4], color='pink', width=barWidth,  label='SF_2')

    plt.xlabel('group', fontweight='bold')
    plt.xticks([r + barWidth for r in range(T)], [t for t in range(T)])
    
    plt.title("Prices")
    plt.legend()
    plt.show()
    
    plt.savefig(path_to_folder)
    


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


### Explotation des fichers (affichages et valeurs)

## Facture Par Joueur
#print(plotDetailedData(bill[0,:,:],bill[1,:,:],bill[2,:,:],bill[3,:,:],bill[4,:,:],"bill","€","C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Detailled bill"))

## Transactions de chaleur
#plotDetailedData1(heat_trans[0,1,:],heat_trans[1,1,:],"C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Detailled heat transactions")

## Charge par joueur
print(plotDetailedData(load[0,:,:],load[1,:,:],load[2,:,:],load[3,:,:],load[4,:,:],"load","kWh","C:\\Users\\Elisabeth\\Documents\\PONTS 2018-2019\\Semestre 2\\Detailled load"))

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

