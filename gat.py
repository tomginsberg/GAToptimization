import numpy as np
import lambert_solver_fast
import pykep as pk


class gprob:
    '''
    Gravity assist problem:
    A class to be used with pygmo to optimize the gravity assist problem.

    goal: Take in a list of planets and a list of times to visit the planets and compute
        the trajectory that minimizes our fitness function for velocity.
    '''

    def __init__(self, planets, times, ivrange, trange, mu=39.42):
        '''
        - planets: a list of the planets created by planet class in lambert_solver
        - times: a list of times when to arrive at each planet
        - ivrange: 2 item list of initial velocity range i.e [v_min,v_max]
        - trange: a 2 item list of launch window i.e [t_min, t_max]
        '''
        self.planets = planets
        self.times = times
        self.ivrange = ivrange
        self.trange = trange
        self.mu = mu
        self.seq_len = len(self.planets)

    def get_bounds(self):
        '''
        The bounds for the time
        '''
        lb = list(map(lambda x: x + self.trange[0], self.times))  # the list of times plus the minimum departure time
        ub = list(map(lambda x: x + self.trange[1], self.times))  # the list of times plus the maximum departure time

        return (lb, ub)  # needs to be of this form for pygmo

    def fitness(self, x):
        '''
        compute the fitness
        '''
        score = 0.0  # a float
        vlam, v = self.get_v(x)

        return np.array(score)  # needs to be of this form for pygmo

    def get_v(self, x):
        '''
        x contains the decision vector, the times when we reach each planet, the initial velocities
        '''
        # 0. mission time
        et = np.cumsum(x)  # [t0,t1,t2, ... ]

        # 1. find the pos and velocities of the planets
        r = np.zeros_like(self.planets)
        v = np.zeros_like(self.planets)

        for i in range(self.seq_len):
            r[i], v[i] = self.planets[i].get_pos(et[i])

        # 2. find path between each planet
        paths = []
        for i in range(self.seq_len - 1):
            paths.append(pk.lambert_problem(r[i], r[i + 1], et[i + 1] - et[i], self.mu))

        # 3. calc fitness
        vlam = [[p.get_v1()[0], p.get_v2()[0]] for p in paths]  # contains the initial and final velocities for each path. Every velocity is a triple (v_x,v_y,v_z)
        return (vlam, v)
