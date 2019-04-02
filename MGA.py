import numpy as np
from poliastro.core.iod import izzo as izzo_fast
import pykep as pk
from Utils.to_mathematica import convert
from gat import gprob
import pygmo as pg
import time
from comet import Comet
import Utils.logger as logger
import matplotlib.pyplot as plt
from astro_objects import *


def optimize(log_output=False):
    # AU
    earth_radius = 0.00004258756
    # AU^3/year^2
    earth_attractor = 0.0001184
    num_gens = 1
    num_evolutions = 1000
    pop_size = 1000

    cometX = Comet()

    planets = [Earth, Earth, Venus, Mercury, Mars, Jupiter, Saturn, Neptune, Uranus, cometX]
    max_enctrs = len(planets) - 2
    times = [0] + [0.1] * (max_enctrs + 1)
    max_times = [5] * (max_enctrs + 2)

    # optimize
    udp = gprob(planets, times, max_times, max_enctr=max_enctrs)
    uda = pg.algorithm(pg.sade(gen=num_gens, memory=True))
    t0 = time.time()
    if(not log_output):  # this avoids the persistent looping to get the fitness data
        archi = pg.archipelago(algo=uda, prob=udp, n=8, pop_size=pop_size)
        archi.evolve(num_evolutions)
        archi.wait()
    else:  # this is where we loop and evolve and get the fitness data for each island
        archi = pg.archipelago(algo=uda, prob=udp, n=8, pop_size=pop_size)
        islands = []
        for i in range(num_evolutions):
            archi.evolve()
            archi.wait()
            avgFit = [-1.0 * np.average(island.get_population().get_f()) for island in archi]
            islands.append(np.array(avgFit))
            # islands.append(np.array(archi.get_champions_f()))  # get the best scores from each island after each stage

        showlog(np.array(islands), 8, num_evolutions)
    t1 = time.time()
    sols = archi.get_champions_f()
    idx = sols.index(min(sols))
    print("index: {}, Scores:  ".format(idx) + str(sols) + "\n\n")
    mission = udp.pretty(archi.get_champions_x()[idx])

    # [print(str(l) + "\n") for l in mission]
    convert(mission[0], mission[1], mission[2])

    print("\n\nTime for soln: {} sec\n\n".format(t1 - t0))


def showlog(fitness_data, num_islands, num_evolutions):
    island_fits = fitness_data.reshape(num_islands, num_evolutions)  # extracts all the best fits at each log output
    plt.grid(True)
    plt.title("Best Fitness as a Function of Evolution Stage: Comet")
    plt.xlabel("Stage")
    plt.ylabel("Fitness")
    for i, island in enumerate(island_fits):
        plt.plot(island, label="Island {}".format(i))
    plt.legend(loc=0)
    plt.show()

if __name__ == '__main__':
    optimize(True)
