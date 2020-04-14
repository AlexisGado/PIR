import numpy as np
import os
from numpy.random import randint

## Market Conditions

scenario = {"demand" : [10]*48}
prices = {"internal" : [25]*48 , "external_purchase" : [30]*48 , "external_sale" : [20]*48}
data_player = {"external_purchase" : [0.5]*48}

## IndustrialConsumer

class IndustrialConsumer :

    def __init__(self,dt,efficiency,battery_max_power,battery_capacity):
        self.dt = dt
        self.horizon = int(24/self.dt)
        self.demand = np.zeros(self.horizon)
        self.prices = {"internal" : np.zeros(self.horizon),"external_purchase" : np.zeros(self.horizon),"external_sale" : np.zeros(self.horizon)}
        self.external_purchase = np.zeros(self.horizon)
        self.efficiency = efficiency
        self.battery_max_power = battery_max_power
        self.battery_capacity = battery_capacity
        self.battery_load = np.zeros(self.horizon)
        self.battery = np.zeros(self.horizon)
        self.electricity_purchases = np.zeros(self.horizon)
        self.load = np.zeros(self.horizon)
        self.bill = np.zeros(self.horizon)
        self.battery[-1] = 0

#Choice of the quantity of electricity from your battery you want to use to fulfill the demand over the time span [t,t+dt]
    def set_battery_load(self,t,battery_load):

        #If the battery isn't full enough to provide such amount of electricity, the latter is set to the maximum amount the battery can provide.
        if ((battery_load/self.efficiency) > self.battery[int(t/self.dt)-1]):
            print("Battery_shortage, battery load set to ",self.efficiency*self.battery[int(t/self.dt)-1])
            battery_load = self.efficiency*self.battery[int(t/self.dt)-1]

        #If the battery isn't enough powerful, the battery load is set to the battery maximum power.
        if (battery_load > self.battery_max_power):
            print("Insufficient battery power, battery load set to battery max power = ",self.battery_max_power)
            battery_load = self.battery_max_power

        #If all rules are respected, the amount of electricity from the battery used to meet the demand and the battery level are updated.
        self.battery_load[int(t/self.dt)] = -battery_load
        self.battery[int(t/self.dt)] = self.battery[int(t/self.dt)-1] - battery_load
        return(True)


#Choice of the quantity of electricity you want to buy at time t (a part of the energy is lost because of a non-perfect battery efficiency
    def buy_electricity(self,t,Quantity):

        #If the player doesn't buy enough electricity to meet the demand, just enough electricity to do so is purchased.
        if ((Quantity - self.battery_load[int(t/self.dt)]) < self.demand[int(t/self.dt)]):
            print("You don't meet the demand, quantity set so that you do : Q = ",self.demand[int(t/self.dt)] + self.battery_load[int(t/self.dt)])
            Quantity = self.demand[int(t/self.dt)] + self.battery_load[int(t/self.dt)]

        #If the amount of electricity purchased outgrows the maximum battery capacity, enough electricity to fill up the battery is purchased.
        if ((Quantity - self.demand[int(t/self.dt)])*self.efficiency + self.battery[int(t/self.dt)] > self.battery_capacity):
            print("Insufficient battery capacity, quantity set to fully fill up your battery : Quantity = ",(self.battery_capacity - self.battery[int(t/self.dt)])/self.efficiency + self.demand[int(t/self.dt)])
            Quantity = (self.battery_capacity - self.battery[int(t/self.dt)])/self.efficiency + self.demand[int(t/self.dt)]

        #Update of the battery level and of the electricity purchases.
        self.battery[int(t/self.dt)] += (Quantity - self.demand[int(t/self.dt)])*self.efficiency
        self.electricity_purchases[int(t/self.dt)] = Quantity
        return(True)

#Get the current demand and prices of electricity
    def observe(self,t,scenario,prices,data_player):
        self.demand[int(t/self.dt)] = scenario["demand"][int(t/self.dt)]
        if (t > 0):
            self.prices["internal"][int(t/self.dt)-1] = prices["internal"][int(t/self.dt)-1]
            self.prices["external_purchase"][int(t/self.dt)-1] = prices["external_purchase"][int(t/self.dt)-1]
            self.prices["external_sale"][int(t/self.dt)-1] = prices["external_sale"][int(t/self.dt)-1]
            self.external_purchase[int(t/self.dt)-1] = data_player["external_purchase"][int(t/self.dt)-1]

#To be completed, describe the player's strategy.
    def take_decisions(self,t):
        print(self.battery[int(t/self.dt)-1])
        self.observe(t,scenario,prices,data_player)
        self.set_battery_load(t,5)
        self.buy_electricity(t,20)
        self.compute_load(t)

#Compute the total load over the time span [t,t+dt].
    def compute_load(self,t):
        self.load[int(t/self.dt)] = self.battery_load[int(t/self.dt)] + self.demand[int(t/self.dt)]

#Reset the class
    def reset(self,t):
        self.battery_load = np.zeros(self.horizon)
        self.battery = np.zeros(self.horizon)
        self.electricity_purchases = np.zeros(self.horizon)
        self.load_profile = np.zeros(self.horizon)
        self.bill = np.zeros(self.horizon)
        self.battery[-1] = 0
        self.prices = {"internal" : np.zeros(self.horizon),"external_purchase" : np.zeros(self.horizon),"external_sale" : np.zeros(self.horizon)}








