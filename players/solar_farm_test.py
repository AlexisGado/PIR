import numpy as np
import os
from numpy.random import randint
from solar_farm import SolarFarm
capacity = 100
max_load = 70
solar_farm = SolarFarm(capacity, max_load)
for t in range(48):
    load = solar_farm.update_battery_stock(t)
    solar_farm.observe(t,0,0)
print('test passed')