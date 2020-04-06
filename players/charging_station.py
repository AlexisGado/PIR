import numpy as np
import os
from numpy.random import randint


## Charging Station

class ChargingStation:

    def __init__(self):
        self.dt = 0.5
        self.efficiency = 0.95
        self.scenario = {}
        self.bill = np.zeros(48) # ou vont etre compté les pénalté puis le cout
        self.load = np.zeros(48) # notre liste l4
        self.load_battery = np.zeros(48)
        self.battery_stock = {"slow" : np.zeros(49), "fast" : np.zeros(49)} # Etat du stock dans les batterie rapides et lentes
        self.nb_fast = 2 # nombres de stations rapides et lentes utilisées
        self.nb_slow = 2
        self.pmax_fast = 22
        self.pmax_slow = 3
        self.cmax = 40*4 ## capacité maximal de notre CS quand 4 postes occupés par des voitures


    # Version naive : on suppose que toutes les voitures sont là 24/24 juste pour voir l'update de leur batteries
    # Donc deux voitures sur le fast et deux sur le slow et comme les voitures ne partent pas on oublie la pénalité de 5e si elle ne sont pas chargées suffisemment
    # Pas de V2G également

    def update_batterie_stock(self,time,load_battery):

        nb = {"slow" : self.nb_slow, "fast" : self.nb_fast}
        p_max = {"slow" : 3*self.nb_slow, "fast" : 22*self.nb_fast}
        c_max = {"slow" : 40*self.nb_slow, "fast" : 40*self.nb_fast}


        for speed in ["slow","fast"] :
            if abs(load_battery[speed]) >= p_max[speed] :
                load_battery[speed] = p_max[speed]*np.sign(load_battery[speed])
            # si on veut charger plus de power que possible on cap à pmax
            new_stock = { "slow" : 0, "fast" : 0 }

            new_stock[slow] = self.battery_stock["slow"][time] + (self.efficiency*max(0,load_battery["slow"])+min(0,load_battery["slow"])/self.efficiency)*self.dt + soc

            new_stock[fast]=self.battery_stock["fast"][time] + (self.efficiency*max(0,load_battery["fast"])+min(0,load_battery["fast"])/self.efficiency)*self.dt
            # on calcul le nouveau stock

            speed="fast"

            if nb[speed]*10 > new_stock[speed] :
                load_battery[speed]=nb[speed]*22
                new_stock[speed]+= 22*nb[speed]*self.dt


        for speed in ["slow","fast"] :
            if new_stock[speed] < 0:
                load_battery[speed] = -(self.battery_stock[speed][time]  + soc)/(self.efficiency*self.dt)
                new_stock[speed] = 0
            # on ne peut pas décharger en dessous de 0

            elif new_stock[speed] > c_max[speed]:
                load_battery[speed] = (c_max[speed] - self.battery_stock[speed][time] ) / (self.efficiency*self.dt)

                new_stock[speed] = c_max[speed]
            # on ne peut pas charger les batteries plus que leur capacité

        for speed in ["slow","fast"] :
            if abs(load_battery[speed]) >= p_max[speed] :
                load_battery[speed] = p_max[speed]*np.sign(load_battery[speed])

        for speed in ["slow","fast"] :
            self.battery_stock[speed][time+1]=new_stock[speed]
            # on met à jour le stock des batteries

        return load_battery



    def compute_load(self,time):

        load_battery = self.load_battery(time)
        load = self.update_batterie_stock(time, load_battery)
        self.load[time] = load["slow"] + load["fast"]

##

CS = ChargingStation
t = 0
load_battery = np.zeros(48)
load_battery = CS.update_batterie_stock(t,load_battery)