import numpy as np
import os
from numpy.random import randint
from IC import IndustrialConsumer

## Market Conditions

demand = np.zeros(48)
for i in range(48):
    demand[i] = 10
    #demand[i] = randint(1,51)

cost_elec_market = np.zeros(48)
for i in range(48):
    cost_elec_market[i] = 0
    #cost_elec_market[i] = randint(30,51)

## The Game

IC = IndustrialConsumer(demand,cost_elec_market)
t = 0
while (t < 2):
    IC.set_battery_load(t,0)
    IC.buy_electricity(t,0)
    IC.compute_load(t)
    #IC.update_bill(t)
    t += IC.dt

print('Done')
