import numpy as np

class Planet:
    def __init__(self, name, mass, orbital_radius, period, theta_0, dt, planet_radius):
        self.name = name
        self.m = mass
        self.r = orbital_radius
        self.p = period
        self.t = theta_0
        self.pos = self.get_pos()
        self.dt = dt
        self.w = 2*np.pi/period
        self.s = planet_radius
    def get_pos(self):
        self.pos = (self.r*np.cos(self.t),self.r*np.sin(self.t))
        return self.pos
    def time_step(self):
        self.t = (self.t + self.w * self.dt)
    def update_and_get_pos(self):
        self.time_step()
        return self.get_pos()
    def get_future_pos(self, time):
        return (self.r*np.cos(self.t + self.w * time),self.r*np.sin(self.t + self.w * time))

class Sun:
    def __init__(self, mass, size):
        self.m = mass
        self.s = size