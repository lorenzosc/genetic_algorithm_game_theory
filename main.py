import os
import sys

import numpy as np

from generation import Generation
from plotter import Plotter

d_fname = sys.argv[1]
pop_size = int(sys.argv[2])
n_gen = int(sys.argv[3])
plot_name = sys.argv[4]
distributions = []

with open(os.path.join("distributions", d_fname), "r") as df:
    for line in df.readlines():
        for wr in map(float, line.split(",")):
            distributions.append(wr)

n_dist = round(len(distributions) ** 0.5)
distributions = np.array(distributions).reshape((n_dist, -1))

gen = Generation(pop_size, distributions)
gen.evolve(n_gen)

Plotter.save_simulation(gen, plot_name)
