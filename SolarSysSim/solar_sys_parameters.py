from celestialbodies import Sun, Planet

sun = Sun(333000,40)
dt = 0.75
orbit_scale = 40/25
mars = Planet("mars",mass=0.642,orbital_radius=227.9 * orbit_scale,period=687.0,theta_0=0,dt=dt,planet_radius=6.8)
earth = Planet("earth",mass=5.97,orbital_radius=149.6 * orbit_scale,period=365.2,theta_0=0,dt=dt,planet_radius=12)
venus = Planet("venus",mass=4.87,orbital_radius=108.2 * orbit_scale,period=224.7,theta_0=0,dt=dt,planet_radius=12)
mercury = Planet("mercury",mass=0.330,orbital_radius=57.9 * orbit_scale,period=88.0,theta_0=0,dt=dt,planet_radius=4.8)

planets = [earth,venus,mercury,mars]