import numpy as np
import os
from numpy.random import randint

class Player:
    def __init__(self):
        self.dt = 0.5
        self.efficiency=0.95
        self.demand=[]
        self.bill = np.zeros(48) # prix de vente de l'électricité
        self.load= np.zeros(48) # chargement de la batterie (li)
        self.battery_stock = np.zeros(49) #a(t)
        self.capacity = 100
        self.max_load = 50
        self.prices = {"internal" : [],"external_purchase" : [],"external_sale" : []}
        self.imbalance=[]

    def update_battery_stock(self,time,load):
        
#If the battery isn't enough powerful, the battery load is set to the battery maximum power.

            if abs(load) > self.max_load:
                load = self.max_load*np.sign(load) 
            new_stock = self.battery_stock[time] + (self.efficiency*max(0,load) - 1/self.efficiency * max(0,-load))*self.dt
            
#If the battery isn't full enough to provide such amount of electricity, the latter is set to the maximum amount the battery can provide, the load is adjusted.
            
            if new_stock < 0: 
                load = - self.battery_stock[time] / (self.efficiency*self.dt)
                new_stock = 0
    
 #If the amount of electricity purchased outgrows the maximum battery capacity, enough electricity to fill up the battery is purchased, the load is adjusted.   
    
            elif new_stock > self.capacity:
                load = (self.capacity - self.battery_stock[time]) / (self.efficiency*self.dt)
                new_stock = self.capacity
    
            self.battery_stock[time+1] = new_stock
            
            
            return load
    
    def take_decision(self,time):
            # implement your policy here
            return 0
        
    def compute_load(self,time,data_scenario):
        load_player = self.take_decision(time)
        load_battery=self.update_battery_stock(time,load_player)
<<<<<<< HEAD:players/industrial_consumer2.py
        self.load[time]=load_battery #+self.demand[time]
=======
        self.load[time]=load_battery + data_scenario["demand"]
>>>>>>> 1b1380734019e54c72eb8d552e871289e01857e4:players/industrial_consumer_1/player.py
        
        return self.load[time]
    
    def observe(self, t, data, price, imbalance):
        self.demand.append(data["demand"])
        if (t > 0):
            self.prices["internal"].append(price["internal"])
            self.prices["external_sale"].append(price["external_sale"])
            self.prices["external_purchase"].append(price["external_purchase"])
            
            self.imbalance.append(imbalance)
        
    
    def reset(self):
        self.load= np.zeros(48)
        self.bill = np.zeros(48)
        self.battery_stock = np.zeros(49)
        self.demand=[]
        self.prices = {"internal" : [],"external_purchase" : [],"external_sale" : []}
        self.imbalance=[]
    
