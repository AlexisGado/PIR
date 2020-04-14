import numpy 
import random


# import the different players

from players.solarfarm import SolarFarm
from players.IC import IndustrialConsumer
from players.charging_station import ChargingStation

## Data
prices=numpy.loadtxt("prices_class_1.csv") #internal prices, external purchase prices, external sale prices

pv_scenarios=numpy.loadtxt("pv.csv") #photovoltaic production per slot, 100 scenarios
ldem_scenarios=numpy.loadtxt("load.csv")  #industrial needs per slot, 100 scenarios
planning_scenarios=numpy.genfromtxt("t_dep_arr.csv",delimiter= ";") #departure and arrival time of each car, 100 scenarios



class Manager():
    
    def __init__(self): #constructor
        
        self.day = 24
        self.dt = 0.5
        self.horizon = int(self.day/self.dt) #nb of time steps

        self.players = {"charging_station": ChargingStation(), 
            "solar_farm": SolarFarm(),
            "industrial_site": IndustrialConsumer(0,0)}  #To be modified
            
        self.prices = {"internal" : prices[0, :], "external_purchase" : prices[1, :], "external_sale" : prices[2, :]}
        self.imbalance=[]
    
    

           ##Compute the energy balance on a slot
    def energy_balance(self, time):

        demand = 0
        supply = 0

        for name, player in self.players.items():

            player.compute_load(time)
            load = player.load[time]

            if load >= 0: #if the player needs energy
                demand += load
            else:         #if the player supply energy
                supply -= load

        return  demand, supply


    ## Compute the bill of each players 
    def compute_bills(self, time, demand, supply):
        total_load=demand-supply    #total load of the grid
        internal_exchange=min(demand,supply)  #what is going to be exchange on the grid
        external_exchange=abs(total_load)   #the quantity of energy in surplus on the grid
        internal_price=self.prices["internal"][time]
        external_selling_price=self.prices["external_sale"][time]
        external_purchasing_price=self.prices["external_purchase"][time]

        if total_load>=0:  #if there is not enough energy on the grid
            
            proportion_internal_demand=internal_exchange/demand
            proportion_internal_supply=1
            
            self.imbalance.append({"proportion_internal_demand": proportion_internal_demand,"proportion_internal_supply": proportion_internal_supply} )

            for name, player in self.players.items():

                load=player.load[time]

                if load>0: #if the player needs energy

                    cost= (internal_price*(proportion_internal_demand) + external_purchasing_price*(1-proportion_internal_demand))*load*dt
                            #the players pays in proportion on and off the grid for his demand
                    player.bill[time] += cost

                elif load<0: #if the player supply energy

                    revenue=internal_price*load*dt #there is enough demand of engery on the grid
                    player.bill[time] += revenue
                    player.information["proportion_internal_supply"][time]=1

        else :   #if the offer is too consequent on the grid
            
            proportion_internal_demand=1
            proportion_internal_supply=internal_exchange/demand
            self.imbalance.append({"proportion_internal_demand": proportion_internal_demand,"proportion_internal_supply": proportion_internal_supply} )
            
            for name, player in self.players.items():
                
                load=player.load[time]

                if load>0: #if the player needs energy

                    cost=internal_price*load*dt  #there is enough energy produced on the grid
                    player.bill[time] += cost

                elif load<0:  #if the player supply energy

                    revenue= (internal_price*(proportion_internal_supply) + external_selling_price*(1-proportion_internal_supply))*load*dt
                            #the players pays in proportion of his supply
                    player.bill[time] += revenue
    
## Draw a scenario for the day
    
    def draw_random_scenario(self):
        
        pv=pv_scenarios[random.randint(0,len(pv_scenarios)-1)] #sunshine data
        ldem=ldem_scenarios[random.randint(0,len(ldem_scenarios))] #industrial consumer need 
        p=random.randint(0,len(planning_scenarios[0])/2 -1) 
        planning=numpy.array([planning_scenarios[:,2*p], planning_scenarios[:,2*p+1]]) #departure and arrival of each car
        
        return pv,ldem,planning


## Transmit data to the player

    def give_info(t,pv,ldem,planning):
        data_scenario = 
        { "sun_at_t" : pv[t],
        "demand_at_t" : ldem[t],
        "departures_at_t" : planning[0],
        "arrivals_at_t" : planning[1]}
        
        if t>0:
            prices = 
            {"internal_price" : self.prices["internal"][t-1],
            "external_sale_price" : self.prices["external_sale"][t-1],
            "external_purchase_price" : self.prices["external_purchase"][t-1]}
            
            
            
        for name, player in self.players.items():
            
            if t>0:
                player.observe(t,data_scenario,prices,self.imbalance[t-1])
            else:
                player.observe(t,data_scenario,{},{})



## Playing one party 

    def play(self):
        
        pv,ldem,planning=self.draw_random_scenario()
        
        for name, player in self.players.items():
            player.prices=self.prices
            
        for t in range(self.horizon): # main loop
            
            give_info(t,pv,ldem)
            load, demand, supply = self.energy_balance(t)
            self.compute_bills(t, load, demand, supply)
