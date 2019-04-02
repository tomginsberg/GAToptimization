import numpy as np

class Planet:
    # AU     AU   Years  Rads  GM (AU^3/Year^2)
    def __init__(self, orbit, period, phi):
        self.orbit = orbit
        self.period = period
        self.omega = 2 * np.pi / period
        self.phi = phi
        self.angular_vel = self.omega * self.orbit

    def get_pos(self, t):
        return np.array([self.orbit * np.cos(self.omega * t + self.phi), self.orbit * np.sin(self.omega * t + self.phi), 0])

    def get_vel(self, t):
        return np.array([-self.angular_vel * np.sin(self.omega * t + self.phi), self.angular_vel * np.cos(self.omega * t + self.phi), 0])