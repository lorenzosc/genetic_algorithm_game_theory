import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from generation import Generation


class Plotter:
    winrates: list[np.ndarray]
    playrates: list[np.ndarray]
    avg_winrates: list[float]
    avg_playrates: list[float]

    arch_stats: pd.DataFrame
    
    n_gen: int
    n_arch: int
    pop_size: int

    plot_name: str

    def __init__ (self, plot_name: str) -> None:
        self.plot_name = plot_name
        os.makedirs(os.path.join("output", self.plot_name), exist_ok=True)

        with open(os.path.join("logs", self.plot_name, "sim_info.txt")) as sf:
            sf.readline()
            self.n_gen, self.n_arch, self.pop_size = map(int, sf.readline().split(","))
        
        with open(os.path.join("logs", self.plot_name, "winrate.txt")) as wf:
            self.winrates = [
                np.fromiter(map(float, line.split(",")), dtype=np.float32)
                for line in wf.readlines()
            ]

        with open(os.path.join("logs", self.plot_name, "playrate.txt")) as pf:
            self.playrates = [
                np.fromiter(map(float, line.split(",")), dtype=np.float32)
                for line in pf.readlines()
            ]

        self.avg_winrates = [ np.mean(winrate) for winrate in self.winrates ]
        self.avg_playrates = [ np.mean(playrate) for playrate in self.playrates ] 

        self.arch_stats = pd.read_csv(
            os.path.join("logs", self.plot_name, "arch_stats.csv"), sep=","
        )

    def plot_winrate (self, ax: plt.axes = None) -> None:
        winrates = [ 
            np.mean(winrate * playrate) / avg_playrate
            for winrate, playrate, avg_playrate in zip(self.winrates, self.playrates, self.avg_playrates)
        ]
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.set_title("Winrate Means")
            ax.set_xlabel("Archetype")
            ax.set_ylabel("Winrate %")
            ax.set_ylim(bottom=min(winrates) * 0.8, top=max(winrates) * 1.1)

        arch_idxs = [ arch_idx for arch_idx in range(len(winrates)) ]
        ax.bar(arch_idxs, winrates)
        ax.plot()

        fig.savefig(
            os.path.join("output", self.plot_name, "winrate"), dpi=300, transparent=False
        )

    def plot_playrate ():
        pass

    def plot_podium_top1 ():
        pass

    def plot_winrate_vs_points (plot_name) -> None:
        pass

    def save_simulation (gen: Generation, plot_name: str) -> None:
        os.makedirs(os.path.join("logs", plot_name), exist_ok=True)

        with (
            open(os.path.join("logs", plot_name, "playrate.txt"), "w") as pf,
            open(os.path.join("logs", plot_name, "winrate.txt"), "w") as wf,
            open(os.path.join("logs", plot_name, "arch_stats.csv"), "w") as af,
            open(os.path.join("logs", plot_name, "sim_info.txt"), "w") as sf
        ):
            sf.write("n_gen,pop_size,n_arch\n")
            sf.write(f"{gen.n_gen},{gen.pop_size},{gen.n_arch}\n")

            af.write("points,podium,top1,mn_wr,mx_wr\n")
            for arch_idx in range(gen.n_arch):
                pf.write(",".join(map(lambda x: f"{x:.2f}", gen.playrate[arch_idx])) + "\n")
                wf.write(",".join(map(lambda x: f"{x:.2f}", gen.winrate[arch_idx][ 1 : ])) + "\n")

                pts, pdm, top1, mn_wr, mx_wr = (
                    gen.arch_points[arch_idx],
                    gen.arch_podium[arch_idx] / gen.n_gen,
                    gen.top_podium[arch_idx] / gen.n_gen,
                    gen.mnmx_pr[arch_idx][0],
                    gen.mnmx_pr[arch_idx][1]
                )

                af.write(f"{pts},{pdm:.2f},{top1:.2f},{mn_wr:.2f},{mx_wr:.2f}\n")
