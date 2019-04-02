import numpy as np
from poliastro.core.iod import izzo as izzo_fast
from comet import Comet

class Planet:
    # AU     AU   Years  Rads  GM (AU^3/Year^2)
    def __init__(self, orbit, period, phi):
        self.orbit = orbit
        self.period = period
        self.omega = 2 * np.pi / period
        self.size = size
        self.phi = phi

    def get_pos(self, t):
        return np.array([self.orbit * np.cos(self.omega * t + self.phi), self.orbit * np.sin(self.omega * t + self.phi), 0])
        

# AU
earth_radius = 0.00004258756
# AU^3/year^2
earth_attractor = 0.0001184

# The sun only has one parameter of interest, it's attractor
Sun = 39.42

Earth = Planet(1, 1, 0)
Mercury = Planet(0.374496, 0.241, np.pi / 2)
Mars = Planet(1.5458, 1.8821, np.pi + .7)
Venus = Planet(0.726088, 0.6156, 3 * np.pi/4 )
Jupiter = Planet(5.328, 11.87, np.pi / 2 + .38 )

Saturn = Planet(9.5497, 29.446986, 0)
Uranus = Planet(19.2099281, 84.01538, 0)
Neptune = Planet(30.0658708, 164.78845, 0)

# lambert_sol = izzo_fast(Sun, Earth.get_pos(0), np.array([-6.74393, -0.197631,0]), 3, M=0, numiter=10, rtol=1e-2)
# for v0, v in lambert_sol:
#     print("V0: {}, Vf: {}".format(v0[:2], v[:2]))

Comet = Comet()
print(Comet.get_pos(0))
for i in range(100):
    print(Comet.get_pos(i))