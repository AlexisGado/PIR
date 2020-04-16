import numpy as np
import os
from numpy.random import randint
from industrial_consumer2 import IndustrialConsumer

## The Game

IC = IndustrialConsumer()
for t in range(48):
    IC.compute_load(t)
print(IC.load)
print(IC.battery_stock)
    

print('Done')
