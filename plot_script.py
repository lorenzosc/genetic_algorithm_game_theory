import sys

from plotter import Plotter


pltr = Plotter(sys.argv[1])

pltr.plot_winrate()
pltr.plot_winrate_vs_points()
pltr.plot_playrate_vs_points()