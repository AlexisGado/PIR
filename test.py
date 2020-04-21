import numpy as np
from simulate import Manager


manager = Manager("data/players.json","data/prices.csv","data/pv.csv","data/load.csv","data/t_dep_arr.csv")
manager.simulate(10)

loads=np.load("data_visualize/load simulation.npy")
bills=np.load("data_visualize/bill simulation.npy")
prices=np.load("data_visualize/price simulation.npy")
batteries1=np.load("data_visualize/battery stock simulation IC SF.npy")
batteries2=np.load("data_visualize/battery stock simulation CS.npy")
scenarios=np.load("data_visualize/scenario simulation.npy")
imbalances=np.load("data_visualize/imbalance simulation.npy")
grid_load=np.load("data_visualize/grid load simulation.npy")
