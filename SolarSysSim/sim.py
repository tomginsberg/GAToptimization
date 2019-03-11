from p5 import *
from solar_sys_parameters import *

def setup():
    size(1000, 800)
    no_stroke()

def draw():
    background(0,0,0,100)
    with push_matrix():
        translate(width/2, height/2)
        fill(253, 184, 19)
        circle((0, 0), sun.s)
        fill(255,255,255)
        for planet in planets:
            circle(planet.update_and_get_pos(), planet.s)

if __name__ == "__main__":
    run()
