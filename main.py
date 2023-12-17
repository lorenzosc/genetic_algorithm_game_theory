import sys

import numpy as np

from generation import Generation

pop_size = int(sys.argv[1])
n_gen = int(sys.argv[2])
d_fname = sys.argv[3]
distributions = []

with open(d_fname) as df:
    for line in df.readlines():
        for wr in map(float, line.split(",")):
            distributions.append(wr)

n_dist = round(len(distributions) ** 0.5)
distributions = np.array(distributions).reshape((n_dist, -1))

gen = Generation(pop_size, distributions)
gen.evolve(n_gen)
