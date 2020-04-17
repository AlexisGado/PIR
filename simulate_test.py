import numpy as np
from simulate import Manager

M=Manager()
M.simulate(100)

loads=np.load("load simulation.npy")
bills=np.load("bill simulation.npy")
prices=np.load("price simulation.npy")
battery=np.load("battery stock simulation.npy")
