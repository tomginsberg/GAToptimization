from p5 import *
from solar_sys_parameters import *
from random import randint
import numpy as np

def setup():
    global trajectory
    size(1000, 800)
    no_stroke()    
    # trajectory = PShape(visible=True, stroke_color=(255,255,255), attribs="path")
    # trajectory.add_vertex((100,100))
    # trajectory.add_vertex((300,300))


def to_cart(r,t):
    return (r*np.cos(t),r*np.sin(t))

t_x = 200
t_y = 0
traj_max = 200
trajectory = [(0,0) for _ in range(traj_max)]
traj_index = 0
trajectory[traj_index] = to_cart(t_x,t_y)
traj_index += 1

#def compute_lambert_arc(r0,rf,t):


def draw():
    global trajectory, t_x, t_y, traj_index, traj_max
    background(0,0,0)
    t_y += 2*np.pi/200
    t_x -= 0.5
    trajectory[traj_index % traj_max] = to_cart(t_x,t_y)
    traj_index += 1
    with push_matrix():
        translate(width/2, height/2)
        fill(255,255,255)
        for p in trajectory:
            circle(p,2)
        fill(253, 184, 19)
        circle((0, 0), sun.s)
        fill(255,255,255)
        for planet in planets:
            circle(planet.update_and_get_pos(), planet.s)

if __name__ == "__main__":
    run()
