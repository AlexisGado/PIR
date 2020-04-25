#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:02:00 2020

@author: corentinguery
"""

import matplotlib.pyplot as plt
import numpy as np
import random as rd

 
    
def plot_1(Tab,unite,titre, labl,joueur, path):
    """ 
    Tab is a (N,T) vector. Each line correspond to a scenario and each column to a time t.
    This function plots a grouped bar diagram with the average values of the vector for each t.
    For the path_to_folder, mind putting '\\' instead of '/'.
    """
    
    """
    Pour loads; bills; batterie IC SF; scenario IC_SF 
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
    plt.title(titre+ " "+joueur)
    plt.grid(True)
    
    plt.show()
    
    plt.savefig(path)

def plot_1bis(Tab,unite,titre, labl,joueur,cars, path):
    
    """
    Pour batterie_CS
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
    plt.title(titre + " "+joueur +" et pour la voiture " + cars)
    plt.grid(True)
    
    plt.show()
    
    plt.savefig(path)
    
 


def plot_2(Tab,unite,titre,path):
    
    "Pour grid_load et imbalances"
    
    T=48
    N=int(Tab['demand'].size/T)
    demand=np.zeros(T)
    supply=np.zeros(T)
    Edemand=np.zeros(T)
    Esupply=np.zeros(T)
    
    for t in range(T):
        demand[t]=np.mean(Tab['demand'][:,t])
        supply[t]=np.mean(Tab['supply'][:,t])
        Edemand[t]=np.std(Tab['demand'][:,t])
        Esupply[t]=np.std(Tab['supply'][:,t])
        
        
    ind=np.arange(T)
    width=0.5

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, demand, width, label='demand',yerr=Edemand, color='r')
    rects2 = ax.bar(ind + width/2, supply, width, label='supply',yerr=Esupply, color='b')

    
    ax.set_ylabel(unite)
    ax.set_title(titre)
    ax.legend()

    fig.tight_layout()

    plt.show()
    
    plt.savefig(path)

def plottotal(dico, unite, titre, labl, path_to_data):
    for cle,objet in dico.items():
        plot_1(objet,unite,titre,labl,cle,path_to_data)



def plotCS(dico,unite,titre,labl,path_to_data):
    h=['1','2','3','4']
    for cle,objet in dico.items():
        for cars in range (4):
            plot_1bis(dico[cle][:,cars,:],unite,titre,labl,cle,h[cars],path_to_data)
        


###################################################################################
  ###Données :

# All npy files are dictionaries (inside a 1 length array)

##Données par joueurs

loads=np.load("data_visualize/load_simulation.npy",allow_pickle=True) 
# keys : players  -- objects : nb_simul*nb_time_steps en MW

bills=np.load("data_visualize/bill_simulation.npy",allow_pickle=True) 
# keys : players  -- objects : nb_simul*nb_time_steps en €

batteries_IC_SF=np.load("data_visualize/battery_stock_simulation_IC_SF.npy",allow_pickle=True) 
# keys : players (except CS)  -- objects : nb_simul*(nb_time_steps+1) en MWh

batteries_CS=np.load("data_visualize/battery_stock_simulation_CS.npy",allow_pickle=True) 
# keys : players (only CS) -- objects : nb_simul*nb_cars*(nb_time_steps+1) en MWh

scenarios_IC_SF=np.load("data_visualize/scenario_simulation_IC_SF.npy",allow_pickle=True) 
# keys : players (except CS)  -- objects : nb_simul*nb_time_steps en MW

scenarios_CS=np.load("data_visualize/scenario_simulation_CS.npy",allow_pickle=True) 
# keys : players (only CS)  -- objects : nb_simul*2(departures/arrivals)*nb_cars en MW


##Données communes

imbalances=np.load("data_visualize/imbalance_simulation.npy",allow_pickle=True)
# keys : demand/supply  -- objects : nb_simul*nb_time_steps en pourcentage

grid_load=np.load("data_visualize/grid_load_simulation.npy",allow_pickle=True)
# keys : demand/supply  -- objects : nb_simul*nb_time_steps en MW

prices=np.load("data_visualize/price_simulation.npy",allow_pickle=True)
# keys : internal/external_purchase/external_sale  -- objects : nb_simul*nb_time_steps
#en €/MWh  
    
####################################################################################


###Affichage des graphes :

"affichage chargement"

plottotal(loads[0],'MW','Chargement pour le joueur','Chargement','/Users/corentinguery/Documents/PIR-master/figure')

"affichage facture"

plottotal(bills[0],'€','Facture pour le joueur','Facture','/Users/corentinguery/Documents/PIR-master/figure')

"affichage batterie IC, SF"

plottotal(batteries_IC_SF[0],'MWh','Niveau de la batterie pour le joueur','Niveau','/Users/corentinguery/Documents/PIR-master/figure')

"affichage batterie CS"

plotCS(batteries_CS[0],'MWh','Niveau de la batterie pour le joueur','Niveau', '/Users/corentinguery/Documents/PIR-master/figure')

"affichage scenario IC_SF"

plottotal(scenarios_IC_SF[0],'MW','Paramètre du joueur','Ensoleillement/Production','/Users/corentinguery/Documents/PIR-master/figure')

"affichage imbalances"

plot_2(imbalances[0],'%','Balance économique achat/vente','/Users/corentinguery/Documents/PIR-master/figure')

"affichage grid_load"

plot_2(grid_load[0],'€','Balance économique achat/vente','/Users/corentinguery/Documents/PIR-master/figure')

"affichage prices"

plottotal(prices[0],'€/MWh',"Prix de l'électricité : ",'Prix','/Users/corentinguery/Documents/PIR-master/figure')

