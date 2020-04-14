import numpy as np
import os
from numpy.random import randint
from IndustrialConsumer import IndustrialConsumer

## The Game

IC = IndustrialConsumer(0.5,0.95,50,100)
t = 0

while (t<24):
    print(int(t/IC.dt))
    IC.take_decisions(t)
    t += 0.5

print('Done')
