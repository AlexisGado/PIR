import numpy as np
import os
from numpy.random import randint
from charging_station import ChargingStation

charging_station = ChargingStation()

t = 0
for t in range(48):
    load = charging_station.compute_load(t)
    charging_station.observe(t,0,0)
    charging_station.penality(t)
    print (load)

print("tests passed !")