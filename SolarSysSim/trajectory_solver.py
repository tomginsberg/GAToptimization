from solar_sys_parameters import *
import numpy as np
from astropy import units as u
from poliastro.bodies import Sun
from poliastro.iod import lambert

k = Sun.k

def compute_total_thrust(soltuion):
    for i in range(soltuion):
        #need to implmeent solution object
        r0 = soltuion[i].r * u.km
        r = soltuion[i+1].r * u.km
        tof = soltuion[i].time * u.min
        lambert_sol = lambert(k.to(u.km ** 3 / u.s ** 2).value,
                r0.value, r.value,
                tof.to(u.s).value)