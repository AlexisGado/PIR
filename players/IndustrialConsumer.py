import numpy as np
import os
from numpy.random import randint

## Conditions de marché

demand = np.zeros(48)
for i in range(48):
    demand[i] = 10
    #demand[i] = randint(1,51)

cost_elec_market = np.zeros(48)
for i in range(48):
    cost_elec_market[i] = 0
    #cost_elec_market[i] = randint(30,51)

## Consommateur Industriel

class IndustrialConsumer :

    def __init__(self):
        self.dt = 0.5
        self.efficiency = 0.95
        self.max_power_battery = 10
        self.battery_capacity = 100
        self.battery_load = np.zeros(48)
        self.battery = np.zeros(48)
        self.electricity_purchases = np.zeros(48)
        self.load_profile = np.zeros(48)
        self.bill = np.zeros(48)
        self.battery[-1] = 50

#Choice of the quantity of electricity from your battery you want to use to fulfill the demand over the time span [t,t+dt]
    def set_battery_load(self,t,battery_load):

        #Si la batterie n'est pas assez remplie, le joueur modifie ses décisions
        while ((battery_load/self.efficiency) > self.battery[int((t-1)*2)]):
            print("Battery_shortage, please modify your decisions")
            print ("Select a new battery_load : ")
            battery_load = int(input())

        #Si la batterie n'est pas assez puissante, le joueur modifie ses décisions
        while (battery_load > self.max_power_battery):
            print("Insufficient battery power, please modify your decisions")
            print ("Select a new battery_load : ")
            battery_load = int(input())

        #Si tout est conforme aux règles, on actualise la quantité d'électricité de la batterie utilisée pour satisfaire la demande et la quantité d'électricité restant dans la batterie
        self.battery_load[int(t*2)] = -battery_load
        self.battery[int(t*2)] = self.battery[int((t-1)*2)] - battery_load
        return(True)


#Choice of the quantity of electricity you want to buy at time t (a part of the energy is lost because of a non-perfect battery efficiency
    def buy_electricity(self,t,Quantity):

        #Si le joueur n'achète pas assez d'électricité pour satisfaire la demande, il modifie ses décisions
        while ((Quantity - self.battery_load[int(t*2)]) < demand[int(t*2)]):
            print("You don't meet the demand, please modify your decisions")
            print ("Select a new quantity of electricity to buy : ")
            Quantity = int(input())

        #Si le surplus d'électricité achetée excède la capacité totale de la batterie, le joueur modifie ses décisions
        while ((Quantity - demand[int(t*2)])*self.efficiency + self.battery[int(t*2)] > self.battery_capacity):
            print("Insufficient battery capacity, please modify your decisions")
            print ("Select a new quantity of electricity to buy : ")
            Quantity = int(input())

        self.battery[int(t*2)] += (Quantity - demand[int(t*2)])*self.efficiency
        self.electricity_purchases[int(t*2)] = Quantity
        return(True)

#Compute the total load over the time span [t,t+dt]
    def compute_load(self,t):
        self.load_profile[int(t*2)] = self.battery_load[int(t*2)] + demand[int(t*2)]

#Compute the current bill
    def update_bill(self,t):
        self.bill[int(t*2)] = cost_elec_market[int(t*2)]*self.electricity_purchases[int(t*2)]


## Le Jeu

IC = IndustrialConsumer()
t = 0
while (t < 2):
    IC.set_battery_load(t,0)
    IC.buy_electricity(t,0)
    IC.compute_load(t)
    IC.update_bill(t)
    t += IC.dt

print('Done')








