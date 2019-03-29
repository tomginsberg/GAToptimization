import numpy as np
from numpy.linalg import norm
from numpy import dot
import lambert_solver_fast
import pykep as pk


class gprob:
    '''
    Gravity assist problem:
    A class to be used with pygmo to optimize the gravity assist problem.

    goal: Take in a list of planets and a list of times to visit the planets and compute
        the trajectory that minimizes our fitness function for velocity.
    '''

    def __init__(self, planets, tmins, tmaxs, mu=39.42, enctr=0):
        '''
        - planets: a list of the planets created by planet class in lambert_solver
        - tmins: a list of times when to launch/arrive at each planet, this should be the minimum time
        - tmaxs: a list of times when to launch/arrive at each planet, this should be the max time
        - enctr: the number of planets to visit not including initial planet, before going for final planet in seq
                must be less than or equal to #planets - 2
        '''
        self.planets = planets
        self.times = tmins
        self.trange = tmaxs
        self.mu = mu
        self.seq_len = len(self.planets)
        self.min_enctr = enctr

    def get_bounds(self):
        '''
        The bounds for the time
        '''  # the list of times plus the minimum departure time and minimum visits as well as the index of the choices multiplied by 10
        lb = list(map(lambda x: x, self.times)) + [10] * (self.seq_len - 2) + [self.min_enctr]
        # the list of times plus the maximum departure time and max visits as well as the index of the choices multiplied by 10
        ub = list(map(lambda x: x, self.trange)) + [(self.seq_len - 2) * 10] * (self.seq_len - 2) + [self.seq_len - 2]

        return (lb, ub)  # needs to be of this form for pygmo

    def fitness(self, x):
        '''
        compute the fitness
        '''
        vlam, v, total_time = self.get_v(x)

        dirVal = 0
        thrust = 0
        dirVal += dot(vlam[0][0] / norm(vlam[0][0]), v[0] / norm(v[0]))
        thrust += norm((vlam[0][0] - v[0]) / norm(v[0]))

        for i in range(len(vlam) - 1):
            dirVal += (dot(vlam[i][1] / norm(vlam[i][1]), v[i + 1] / norm(v[i + 1])) + dot(vlam[i + 1][0] / norm(vlam[i + 1][0]), v[i + 1] / norm(v[i + 1]))) / 2
            thrust += norm(vlam[i + 1][0] - v[i]) / norm(vlam[i][1] - v[i])

        timeScore = np.exp(-total_time)  # best time is if we had zero time -> 1
        thrust = 1 - abs(1 - thrust)
        score = thrust + 2 * dirVal + 10 * timeScore

        return (-1.0 * score, )  # needs to be of this form for pygmo

    def get_v(self, x, soln=False):
        '''
        x contains the decision vector, the times when we reach each planet, the initial velocities
        '''
        # 0. mission time and number of GAs
        et, GAps, enctrs = np.array(x[:len(self.times)]), x[len(self.times):-1], x[-1]  # [t0,t1,t2, ... ], [i0,i1,i2,...], [ectrs]
        visits = int(enctrs) + 2
        GAps = np.array(GAps, dtype=int)[:visits - 2] // 10
        ts = np.zeros_like(self.planets[:visits])
        ts[0] = et[0]
        ts[-1] = et[-1]
        if(visits - 2 > 0):
            ts[1:-1] = et[GAps]  # find the times that correspond to the times for each gravity assist
        et = np.cumsum(ts)

        # 1. find the pos and velocities of the planets
        r = np.zeros_like(self.planets[:visits])
        v = np.zeros_like(self.planets[:visits])

        r[0], v[0] = [self.planets[0].get_pos(et[0]), self.planets[0].get_vel(et[0])]  # find the position and velocity of start planet
        r[-1], v[-1] = [self.planets[-1].get_pos(et[-1]), self.planets[-1].get_vel(et[-1])]  # find the position and velocity of end planet

        if(visits - 2 > 0):
            choices = np.array(self.planets)[GAps]
            for i, plts in enumerate(choices):
                r[i + 1], v[i + 1] = [plts.get_pos(et[i + 1]), plts.get_vel(et[i + 1])]

        # 2. find path between each planet
        paths = []
        for i in range(visits - 1):
            paths.append(pk.lambert_problem(r[i], r[i + 1], et[i + 1] - et[i], self.mu))

        # 3. calc fitness
        vlam = [[np.array(p.get_v1()[0]), np.array(p.get_v2()[0])] for p in paths]  # contains the initial and final velocities for each path. Every velocity is a triple (v_x,v_y,v_z)
        if(not soln):
            return (vlam, v, et[-1])
        return (vlam, v, r, et, GAps, enctrs)

    def get_soln(self, x, pretty=False):
        '''
        returns the solution trajectory, based on the decision vector x
        '''
        vlam, v, r, et, GAps, enctrs = self.get_v(x, soln=True)

        # get the planets we visited
        plnts = []
        plnts.append(self.planets[0])
        if(enctrs > 0):
            choices = np.array(self.planets)[GAps]
            [plnts.append(p) for p in choices]
        plnts.append(self.planets[-1])

        ivs = [vel[0] for vel in vlam]
        if(not pretty):
            return (r, et, ivs)  # return the position of all the planets at the arrival times including the start time as well as the initial velocities at each planet
        return(r, et, ivs, len(plnts))

    def pretty(self, x):
        '''
        returns the solution trajectory, based on the decision vector x
        but also just prints some extra info

        '''
        r, et, ivs, plnts = self.get_soln(x, pretty=True)
        print("Start time: {} Years from now, arrive in {} Years".format(et[0], et[-1]))
        print("We made {} gravity assists".format(plnts - 2))
        print("\n\n")
        return (r, et, ivs)
