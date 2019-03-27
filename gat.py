import numpy as np


class gprob:
    '''
    Gravity assist problem:
    A class to be used with pygmo to optimize the gravity assist problem.

    goal: Take in a list of planets and a list of times to visit the planets and compute
        the trajectory that minimizes our fitness function for velocity.
    '''

    def __init__(self, planets, times, ivrange, trange, mu=39.42):
        '''
        - planets: a list of the planets created by planet class
        - times: a list of times when to arrive at each planet
        - ivrange: 2 item list of initial velocity range i.e [v_min,v_max]
        - trange: a 2 item list of launch window i.e [t_min, t_max]
        '''
        self.planets = planets
        self.times = times
        self.ivrange = ivrange
        self.trange = trange
        self.mu = mu

    def get_bounds(self):
        '''
        The bounds for the time
        '''
        lb = list(map(lambda x: x + self.trange[0], self.times))  # the list of times plus the minimum departure time
        ub = list(map(lambda x: x + self.trange[1], self.times))  # the list of times plus the maximum departure time

        return (lb, ub)

    def fitness(self, x):
        '''
        compute the fitness
        '''
