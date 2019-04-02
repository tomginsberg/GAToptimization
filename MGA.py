import numpy as np
from poliastro.core.iod import izzo as izzo_fast
import pykep as pk
from Utils.to_mathematica import convert
from gat import gprob
import pygmo as pg
import time
from comet import Comet
import pandas as pd
import matplotlib.pyplot as plt


class Planet:
    # AU     AU   Years  Rads  GM (AU^3/Year^2)

    def __init__(self, orbit, size, period, phi, attractor):
        self.orbit = orbit
        self.period = period
        self.omega = 2 * np.pi / period
        self.size = size
        self.phi = phi
        self.angular_vel = self.omega * self.orbit

    def get_pos(self, t):
        return np.array([self.orbit * np.cos(self.omega * t + self.phi), self.orbit * np.sin(self.omega * t + self.phi), 0])

    def get_vel(self, t):
        return np.array([-self.angular_vel * np.sin(self.omega * t + self.phi), self.angular_vel * np.cos(self.omega * t + self.phi), 0])


def optimize(log_output=False):
    # AU
    earth_radius = 0.00004258756
    # AU^3/year^2
    earth_attractor = 0.0001184
    num_gens = 100
    num_evolutions = 10
    pop_size = 50

    # The sun only has one parameter of interest, it's attractor
    Sun = 39.42

    Earth = Planet(1, earth_radius, 1, 0, earth_attractor)
    Mercury = Planet(0.374496, earth_radius * 0.38, 0.241, np.pi / 2, 0.0552734 * earth_attractor)
    Mars = Planet(1.5458, earth_radius * 0.53, 1.8821, np.pi + .7, 0.107447 * earth_attractor)
    Venus = Planet(0.726088, earth_radius * 0.95, 0.6156, 3 * np.pi / 4, 0.814996 * earth_attractor)
    Jupiter = Planet(5.328, earth_radius * 3, 11.87, np.pi / 2 + 0.38, 317.828 * earth_attractor)
    cometX = Comet()

    planets = [Earth, Earth, Venus, Mercury, Mars, Jupiter, cometX]
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
            islands.append(np.array(archi.get_champions_f()))  # get the best scores from each island after each stage

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
    plt.title("Best Fitness as a Function of Evolution Stage: Jupiter")
    plt.xlabel("Stage")
    plt.ylabel("Fitness")
    for i, island in enumerate(island_fits):
        plt.plot(-1 * island, label="Island {}".format(i))
    plt.legend(loc=0)
    plt.show()

if __name__ == '__main__':
    optimize()
