import os
import sys
import random


with open(os.path.join("distributions", sys.argv[1]), "w") as df:
    n_arch = int(sys.argv[2])
    max_points = int(sys.argv[3])

    for arch_idx in range(n_arch):
        arch_points = random.randint(1, max_points)

        for opp_idx in range(n_arch):
            if opp_idx != 0:
                df.write(",")

            if opp_idx == arch_idx:
                df.write("0")

            else:
                opp_points = random.randint(0, arch_points)
                arch_points -= opp_points

                df.write(f"{opp_points}")

        df.write("\n")