import numpy as np


class GravAst:
    def __init__(self, pos, vi, planet):
        self.planet = planet
        self.pos = pos
        self.vi = vi
        self.v_f = None 
        self.r_f = None
        self.time = None 
        self.compute_2D()

    def compute_2D(self):
        """
        Computes a two dimensional Gravity Assist using the Labunsky model
        """
        # whoever makes the planet/craft object, please have fields self.pos and self.vel be numpy arrays
        r = self.planet.pos - self.pos
        v = self.planet.vel - self.vi

        r_abs = np.linalg.norm(r)
        v_abs = np.linalg.norm(v)

        gamma = np.pi - np.arccos(np.dot(r,v) / (r_abs * v_abs))
        v_inf_2 = v_abs**2 - 2 * self.planet.mu / r_abs
        Delta = r_abs * np.sin(gamma)
        
        var_phi = 2 * np.arctan(self.planet.mu / (Delta * v_inf_2))
        phi = np.pi + var_phi - 2 * gamma

        c_phi , s_phi = np.cos(phi), np.sin(phi)
        c_var_phi , s_var_phi = np.cos(var_phi), np.sin(var_phi)

        self.r_f = np.dot(np.matrix( [ [c_phi, -s_phi], [s_phi, c_phi] ] ),r) + self.planet.pos
        self.v_f = -np.dot(np.matrix( [ [c_var_phi, -s_var_phi], [s_var_phi, c_var_phi] ] ),v) - self.planet.vel

        # delta = phi / 2
        # a = 1 / ((v_abs**2) / self.planet.mu - 2 / r_abs)
        # H = np.arccosh((1+r_abs / a) * np.sin(delta))
        # self.time = 2 * np.sqrt((a**3) / self.planet.mu) * (np.sinh(H)/np.sin(delta) - H)
