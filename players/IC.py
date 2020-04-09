import numpy as np
import os
from numpy.random import randint

## IndustrialConsumer

class IndustrialConsumer :

    def __init__(self,demand,cost_elec_market):
        self.dt = 0.5
        self.demand = demand
        self.cost_elec_market = cost_elec_market
        self.efficiency = 0.95
        self.battery_max_power = 10
        self.battery_capacity = 100
        self.battery_load = np.zeros(48)
        self.battery = np.zeros(48)
        self.electricity_purchases = np.zeros(48)
        self.load_profile = np.zeros(48)
        self.bill = np.zeros(48)
        self.battery[-1] = 50

#Choice of the quantity of electricity from your battery you want to use to fulfill the demand over the time span [t,t+dt]
    def set_battery_load(self,t,battery_load):

        #If the battery isn't full enough to provide such amount of electricity, the latter is set to the maximum amount the battery can provide.
        if ((battery_load/self.efficiency) > self.battery[int((t-1)*2)]):
            print("Battery_shortage, battery load set to ",self.efficiency*self.battery[int((t-1)*2)])
            battery_load = self.efficiency*self.battery[int((t-1)*2)]

        #If the battery isn't enough powerful, the battery load is set to the battery maximum power.
        if (battery_load > self.battery_max_power):
            print("Insufficient battery power, battery load set to battery max power = ",self.battery_max_power)
            battery_load = self.battery_max_power

        #If all rules are respected, the amount of electricity from the battery used to meet the demand and the battery level are updated.
        self.battery_load[int(t*2)] = -battery_load
        self.battery[int(t*2)] = self.battery[int((t-1)*2)] - battery_load
        return(True)


#Choice of the quantity of electricity you want to buy at time t (a part of the energy is lost because of a non-perfect battery efficiency
    def buy_electricity(self,t,Quantity):

        #If the player doesn't buy enough electricity to meet the demand, just enough electricity to do so is purchased.
        if ((Quantity - self.battery_load[int(t*2)]) < self.demand[int(t*2)]):
            print("You don't meet the demand, quantity set so that you do : Q = ",self.demand[int(t*2)] + self.battery_load[int(t*2)])
            Quantity = self.demand[int(t*2)] + self.battery_load[int(t*2)]

        #If the amount of electricity purchased outgrows the maximum battery capacity, enough electricity to fill up the battery is purchased.
        if ((Quantity - self.demand[int(t*2)])*self.efficiency + self.battery[int(t*2)] > self.battery_capacity):
            print("Batterie insuffisante, quantity set to fully fill up your battery : Quantity = ",(self.battery_capacity - self.battery[int(t*2)])/self.efficiency + self.demand[int(t*2)])
            Quantity = (self.battery_capacity - self.battery[int(t*2)])/self.efficiency + self.demand[int(t*2)]

        #Update of the battery level and of the electricity purchases.
        self.battery[int(t*2)] += (Quantity - self.demand[int(t*2)])*self.efficiency
        self.electricity_purchases[int(t*2)] = Quantity
        return(True)

#Compute the total load over the time span [t,t+dt].
    def compute_load(self,t):
        self.load_profile[int(t*2)] = self.battery_load[int(t*2)] + self.demand[int(t*2)]

#Compute the current bill.
    # def update_bill(self,t):
    #     self.bill[int(t*2)] = self.cost_elec_market[int(t*2)]*self.electricity_purchases[int(t*2)]









