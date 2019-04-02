from planet import Planet 
import numpy as np

#Sun = 39.42

Earth = Planet(1, 1, 0)
Mercury = Planet(0.374496, 0.241, np.pi / 2)
Mars = Planet(1.5458, 1.8821, np.pi + .7)
Venus = Planet(0.726088, 0.6156, 3 * np.pi/4 )
Jupiter = Planet(5.328, 11.87, np.pi / 2 + .38 )
Saturn = Planet(9.5497, 29.446986, 0)
Uranus = Planet(19.2099281, 84.01538, 0)
Neptune = Planet(30.0658708, 164.78845, 0)