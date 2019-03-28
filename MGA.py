import numpy as np
from poliastro.core.iod import izzo as izzo_fast
import pykep as pk
from Utils.to_mathematica import convert
from gat import gprob
import pygmo as pg
import time


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


def optimize():
    # AU
    earth_radius = 0.00004258756
    # AU^3/year^2
    earth_attractor = 0.0001184

    # The sun only has one parameter of interest, it's attractor
    Sun = 39.42

    Earth = Planet(1, earth_radius, 1, 0, earth_attractor)
    Mercury = Planet(0.374496, earth_radius * 0.38, 0.241, np.pi / 2, 0.0552734 * earth_attractor)
    Mars = Planet(1.5458, earth_radius * 0.53, 1.8821, np.pi + .7, 0.107447 * earth_attractor)
    Venus = Planet(0.726088, earth_radius * 0.95, 0.6156, 3 * np.pi / 4, 0.814996 * earth_attractor)
    Jupiter = Planet(5.328, earth_radius * 3, 11.87, np.pi / 2 + 0.38, 317.828 * earth_attractor)

    times = [0, .2, 0.3, 0.6, 5]
    planets = [Earth, Venus, Earth, Mars, Jupiter]
    enctrs = len(planets) - 5

    # optimize the problem
    udp = gprob(planets, times, [0, 1], enctr=enctrs)
    uda = pg.sade(gen=100)
    t0 = time.time()
    archi = pg.archipelago(algo=uda, prob=udp, n=8, pop_size=100)
    archi.evolve(10)
    archi.wait()
    t1 = time.time()
    sols = archi.get_champions_f()
    # print("Scores:  " + str(sols) + "\n")
    idx = sols.index(min(sols))
    mission = udp.pretty(archi.get_champions_x()[idx])

    # [print(str(l) + "\n") for l in mission]
    convert(mission[0], mission[1], mission[2])

    print("\n\nTime for soln: {} sec\n\n".format(t1 - t0))

if __name__ == '__main__':
    optimize()
