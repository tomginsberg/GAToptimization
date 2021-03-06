import numpy as np
from poliastro.core.iod import izzo as izzo_fast
import pykep as pk
from Utils.to_mathematica import convert

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


times = [0, .6, 1.7, 2.5, 5]
planets = [Earth, Venus, Earth, Mars, Jupiter]
items = len(times)  # should also equal length of planets
pos = [planets[i].get_pos(times[i]) for i in range(items-1)]
pos.append(np.array([-9.64594, 2.83725]))

trajectory = [(pos[i], pos[i + 1], times[i + 1] - times[i]) for i in range(items - 1)]

# Solve Lamberts problem with every element of solution
def solve_trajectory():
    ivs = [pk.lambert_problem(*leg, Sun).get_v1()[0] for leg in trajectory]
    print(convert(pos,times,ivs))
    print(trajectory)
    print('')
    print(ivs)
