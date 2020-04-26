import numpy as np
import os
from numpy.random import randint
from solar_farm import SolarFarm
capacity = 100
max_load = 70
solar_farm = SolarFarm()
for t in range(48):
    load = solar_farm.compute_load(t)
print(solar_farm.load)
print(solar_farm.battery_stock)
print('test passed')