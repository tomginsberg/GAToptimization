import numpy as np 
from poliastro.core.iod import izzo as izzo_fast


class Planet:
    #################  AU     AU   Years  Rads  GM (AU^3/Year^2)
    def __init__(self,orbit, size, period, phi, attractor):
        self.orbit = orbit
        self.period = period
        self.omega = 2 * np.pi / period
        self.size = size
        self.phi = phi
    def get_pos(self,t):
        return np.array([self.orbit * np.cos(self.omega * t + self.phi), self.orbit * np.sin(self.omega * t + self.phi), 0])
        

##AU
earth_radius = 0.00004258756
##AU^3/year^2
earth_attractor = 0.0001184

#The sun only has one parameter of interest, it's attractor 
Sun = 39.42

Earth = Planet(1, earth_radius, 1, 0, earth_attractor)
Mercury = Planet(0.374496, earth_radius * 0.38, 0.241, np.pi/2, 0.0552734 * earth_attractor)
Mars = Planet(1.5458, earth_radius * 0.53, 1.8821, np.pi + .7, 0.107447 * earth_attractor)
Venus = Planet(0.726088, earth_radius * 0.95, 0.6156, 3 * np.pi/4, 0.814996 * earth_attractor)
Jupiter = Planet(5.328, earth_radius * 3, 11.87, np.pi / 4 + .38, 317.828 * earth_attractor)

lambert_sol = izzo_fast(Sun, Earth.get_pos(0), Earth.get_pos(1/4), 1/4, M=0, numiter=10, rtol=1e-2)
for v0, v in lambert_sol:
    print("V0: {}, Vf: {}".format(v0[:2], v[:2]))