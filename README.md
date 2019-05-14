
# Gravity Assisted Trajectory Optimization
![](https://i.imgur.com/dMWAUWp.jpg)

## Background
This was a project created for Applications of Classical Mechanics. The aim was to explore the problem of determining the optimal trajectory from Earth to a different point in the solar system using gravitational assists from other planets to minmize fuel consumption.

A big piece of inspiration was the [Rossetta Lander](https://www.youtube.com/watch?time_continue=26&v=iEQuE5N3rwQ&t=8s).

More information can be found in the [project report](https://www.overleaf.com/read/ywpzdwdppbmm).

## Requirments
### Demo Version: *View Sample Trajectories*
Your in luck all you need is [Processing](https://processing.org/download/).
### Full Version: *Create New Trajectories!*
The full version will only run on windows operating systems
* [python 3.x](https://www.python.org/ftp/python/3.7.3/python-3.7.3-macosx10.9.pkg)
* [pygmo](https://esa.github.io/pygmo/)
* [pykep](https://esa.github.io/pykep/)
* [Mathematica](https://www.wolfram.com/mathematica/trial/)
* [Processing](https://processing.org/download/) 
## Setup and Run
```
git clone "this repo"
cd GAToptimization/solarsys/main 
processing-java --sketch=$dir --run
```
### Usage 
Opening screen. Destinations can be selected using butttons.

![](https://i.imgur.com/wIrjGyH.jpg)

**Demo Version will ONLY function with sample inputs**
---
Sample screenshot. Mouse controls allow for full 3D panning, arrow keys allow for speed control. The eneter key can be pushed at any tiem to restart the current trajectory. The application must be restarted to return to the opening screen.

![](https://i.imgur.com/RmCkc0j.png)

If you would like to run manually open main.pde in the processing IDE and click run sketch
## Presentation
View the presentation slides [here](https://www.overleaf.com/read/wnvjcghqtsmn
).
## Project Report
View the project report [here](https://www.overleaf.com/read/ywpzdwdppbmm
).

###### tags: `Space` `Optimization` `Physics`
