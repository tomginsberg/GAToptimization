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
import sys
from planet import Planet
import subprocess


def optimize(log_output=False, dest='Mars'):
    # AU
    # earth_radius = 0.00004258756
    # AU^3/year^2
    # earth_attractor = 0.0001184
    phi = [np.random.uniform(0, 2 * np.pi) for i in range(2)] + [0] + [np.random.uniform(0, 2 * np.pi) for i in range(5)]
    Earth = Planet(1, 1, phi[2], "Earth")
    Mercury = Planet(0.374496, 0.241, phi[0], "Mercury")
    Mars = Planet(1.5458, 1.8821, phi[3], "Mars")
    Venus = Planet(0.726088, 0.6156, phi[1], "Venus")
    Jupiter = Planet(5.328, 11.87, phi[4], "Jupiter")
    Saturn = Planet(9.5497, 29.446986, phi[5], "Saturn")
    Uranus = Planet(19.2099281, 84.01538, phi[6], "Uranus")
    Neptune = Planet(30.0658708, 164.78845, phi[7], "Neptune")

    num_gens = 1
    num_evolutions = 75
    pop_size = 30
    cometX = Comet()
    if dest == "Comet":
        planets = [Earth, Earth, Mercury, Mars, Venus, Jupiter, Saturn, Neptune, Uranus, cometX]
    else:
        choices = [Earth, Earth, Mercury, Mars, Venus, Jupiter, Saturn, Neptune, Uranus]
        destination = [x for x in choices if x.get_name() == dest]
        choices.remove(destination[0])
        planets = choices + [destination[0]]
    if dest == "Venus" or dest == "Mercury" or dest == "Mars":
        max_enctrs = 1
    else:
        max_enctrs = len(planets) - 2
        num_gens = 100
        num_evolutions = 2
        pop_size = 20
    times = [0] + [0.1] * (max_enctrs + 1)
    max_times = [5] * (max_enctrs + 2)

    # optimize
    t0 = time.time()
    udp = gprob(planets, times, max_times, max_enctr=max_enctrs)
    uda = pg.algorithm(pg.sade(gen=num_gens, memory=True))
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

        showlog(np.array(islands), 8, num_evolutions, dest)
    t1 = time.time()
    sols = archi.get_champions_f()
    idx = sols.index(min(sols))
    print("index: {}, Scores:  ".format(idx) + str(sols) + "\n\n")
    mission = udp.pretty(archi.get_champions_x()[idx])

    # [print(str(l) + "\n") for l in mission]
    convert(mission[0], mission[1], mission[2])
    logger.log(mission[1][0], mission[1][-1], phi)

    print("\nTime for soln: {} sec\n\n".format(t1 - t0))


def showlog(fitness_data, num_islands, num_evolutions, dest):
    island_fits = fitness_data.reshape(num_evolutions, num_islands)  # extracts all the best fits at each log output
    plt.grid(True)
    plt.title("Average Fitness as a Function of Generation: {}".format(dest))
    plt.xlabel("Generation Number")
    plt.ylabel("Fitness")
    for i in range(num_islands):
        plt.plot(island_fits[:, i], label="Island {}".format(i))
    plt.legend(loc=0)
    plt.show()

if __name__ == '__main__':
    print("Generating Trajectory to {}".format(sys.argv[1]))
    optimize(False, dest=sys.argv[1])
    #..\\Desktop\\galaxy\\GAToptimization\\
    subprocess.call("math -run < ..\\Desktop\\galaxy\\GAToptimization\\integrator.m", shell=True)
    print("Done")
