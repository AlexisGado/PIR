import numpy as np
import os
from numpy.random import randint

## Market Conditions

scenario = {"demand" : [10]*48}
prices = {"internal" : [25]*48 , "external_purchase" : [30]*48 , "external_sale" : [20]*48}
data_player = {"external_purchase" : [0.5]*48} 

## IndustrialConsumer

class IndustrialConsumer :

    def __init__(self):
        self.dt = 0.5
        self.horizon = int(24/self.dt)
        self.demand = np.zeros(self.horizon)
        self.prices = {"internal" : np.zeros(self.horizon),"external_purchase" : np.zeros(self.horizon),"external_sale" : np.zeros(self.horizon)}
        self.external_purchase = np.zeros(self.horizon)
        self.efficiency = 0.95
        self.battery_max_power = 50
        self.battery_capacity = 100
        self.battery_load = np.zeros(self.horizon)
        self.battery = np.zeros(self.horizon)
        self.electricity_purchases = np.zeros(self.horizon)
        self.load = np.zeros(self.horizon)
        self.bill = np.zeros(self.horizon)
        self.battery[-1] = 0
        self.demand=[]
        self.imbalance=[]

#Choice of the quantity of electricity from your battery you want to use to fulfill the demand over the time span [t,t+dt]
    def set_battery_load(self,t,battery_load):

        #If the battery isn't full enough to provide such amount of electricity, the latter is set to the maximum amount the battery can provide.
        if ((battery_load*self.dt/self.efficiency) > self.battery[t-1]):
            print("Battery_shortage, battery load set to ",self.efficiency*self.battery[t-1])
            battery_load = self.efficiency*self.battery[t-1]/self.dt

        #If the battery isn't enough powerful, the battery load is set to the battery maximum power.
        if (battery_load > self.battery_max_power):
            print("Insufficient battery power, battery load set to battery max power = ",self.battery_max_power)
            battery_load = self.battery_max_power

        #If all rules are respected, the amount of electricity from the battery used to meet the demand and the battery level are updated.
        self.battery_load[t] = -battery_load
        self.battery[t] = self.battery[t-1] - battery_load*self.dt
        
        return battery_load
        


#Choice of the quantity of electricity you want to buy at time t (a part of the energy is lost because of a non-perfect battery efficiency
    def buy_electricity(self,t,Quantity):

        #If the player doesn't buy enough electricity to meet the demand, just enough electricity to do so is purchased.
        if ((Quantity - self.battery_load[t]*self.dt) < self.demand[t]):
            print("You don't meet the demand, quantity set so that you do : Q = ",self.demand[t] + self.battery_load[t])
            Quantity = self.demand[t] + self.battery_load[t]*self.dt

        #If the amount of electricity purchased outgrows the maximum battery capacity, enough electricity to fill up the battery is purchased.
        if ((Quantity - self.demand[t])*self.efficiency + self.battery[t] > self.battery_capacity):
            print("Insufficient battery capacity, quantity set to fully fill up your battery : Quantity = ",(self.battery_capacity - self.battery[t])/self.efficiency + self.demand[t])
            Quantity = (self.battery_capacity - self.battery[t])/self.efficiency + self.demand[t]

        #Update of the battery level and of the electricity purchases.
        self.battery[t] += (Quantity - self.demand[t])*self.efficiency
        self.electricity_purchases[t] = Quantity
       

#Get the current demand and prices of electricity
    def observe(self, t, data, price, imbalance):
        self.demand.append(data["demand"])
        if (t > 0):
            self.prices["internal"].append(price["internal"])
            self.prices["external_sale"].append(price["external_sale"])
            self.prices["external_purchase"].append(price["external_purchase"])
            
            self.imbalance.append(imbalance)
        

#To be completed, describe the player's strategy.
    def take_decision(self,t):
        return -5
        
        

#Compute the total load over the time span [t,t+dt].
    def compute_load(self,t):
        battery_load=self.take_decision(t)
        self.set_battery_load(t,battery_load)
        
        self.load[t] = self.battery_load[t] #+ self.demand[t]
        
        return self.load[t]

#Reset the class
    def reset(self,t):
        self.battery_load = np.zeros(self.horizon)
        self.battery = np.zeros(self.horizon)
        self.electricity_purchases = np.zeros(self.horizon)
        self.load_profile = np.zeros(self.horizon)
        self.bill = np.zeros(self.horizon)
        self.battery[-1] = 0
        self.prices = {"internal" : [],"external_purchase" : [],"external_sale" : []}
        self.demand=[]
        self.imbalance=[]








