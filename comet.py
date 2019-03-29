from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

x = np.array([2., 2.09074, 2.15889, 2.19662, 2.19294, 2.13267, 1.99608, 1.76133, \
1.41377, 0.96056, 0.435381, -0.11853, -0.668145, -1.19566, -1.69404, \
-2.16195, -2.60062, -3.01218, -3.39902, -3.76342, -4.10747, -4.43302, \
-4.7417, -5.03494, -5.314, -5.57997, -5.83383, -6.07643, -6.30855, \
-6.53084, -6.74393, -6.94836, -7.14462, -7.33316, -7.51438, -7.68865, \
-7.85631, -8.01767, -8.173, -8.32257, -8.46663, -8.60539, -8.73906, \
-8.86784, -8.99191, -9.11143, -9.22655, -9.33743, -9.44421, -9.547, \
-9.64594, -9.74114, -9.83271, -9.92075, -10.0053, -10.0866, -10.1646, \
-10.2394, -10.3112, -10.3799, -10.4456, -10.5085, -10.5686, -10.6258, \
-10.6804, -10.7324, -10.7818, -10.8286, -10.8729, -10.9148, -10.9543, \
-10.9914, -11.0262, -11.0588, -11.0891, -11.1172, -11.1432, -11.167, \
-11.1887, -11.2084, -11.226, -11.2416, -11.2553, -11.2669, -11.2767, \
-11.2846, -11.2906, -11.2948, -11.2971, -11.2976, -11.2964, -11.2933, \
-11.2886, -11.2821, -11.2739, -11.264, -11.2525, -11.2393, -11.2245, \
-11.2081, -11.19, -11.1704, -11.1492, -11.1265, -11.1022, -11.0763, \
-11.049, -11.0201, -10.9898, -10.958, -10.9247, -10.8899, -10.8537, \
-10.8161, -10.777, -10.7365, -10.6946, -10.6513, -10.6066, -10.5605, \
-10.5131, -10.4642, -10.4141, -10.3625, -10.3097, -10.2555, -10.1999, \
-10.143, -10.0849, -10.0254, -9.96457, -9.90247, -9.83907, -9.77438, \
-9.70841, -9.64116, -9.57264, -9.50284, -9.43178, -9.35946, -9.28588, \
-9.21104, -9.13495, -9.05762, -8.97904, -8.89922, -8.81816, -8.73587, \
-8.65234, -8.56758, -8.4816, -8.39439, -8.30595, -8.21629, -8.12542, \
-8.03332, -7.94001, -7.84548, -7.74974, -7.65278, -7.55461, -7.45523, \
-7.35463, -7.25283, -7.14982, -7.0456, -6.94017, -6.83353, -6.72568, \
-6.61663, -6.50636, -6.39489, -6.28221, -6.16832, -6.05322, -5.93692, \
-5.8194, -5.70068, -5.58074, -5.4596, -5.33724, -5.21368, -5.08891, \
-4.96292, -4.83573, -4.70733, -4.57772, -4.4469, -4.31488, -4.18166, \
-4.04723, -3.9116, -3.77477, -3.63675, -3.49754, -3.35715, -3.21558, \
-3.07284, -2.92893, -2.78388, -2.63768, -2.49035, -2.34191, -2.19237, \
-2.04175, -1.89009, -1.7374, -1.58372, -1.42908, -1.27353, -1.11712, \
-0.959901, -0.801945, -0.64333, -0.484149, -0.324508, -0.164536, \
-0.00438238, 0.155773, 0.315719, 0.475198, 0.633904, 0.791463, \
0.947419, 1.10121, 1.25214, 1.39933, 1.54167, 1.67774, 1.80568, \
1.92306, 2.02659])

y = np.array([3., 2.58697, 2.14625, 1.67561, 1.17385, 0.642513, 0.0891947, \
-0.467128, -0.992037, -1.44207, -1.7854, -2.01711, -2.15284, \
-2.21419, -2.22037, -2.18602, -2.12178, -2.03524, -1.93188, -1.81569, \
-1.68963, -1.55593, -1.41627, -1.27199, -1.12412, -0.973459, \
-0.820679, -0.66631, -0.510784, -0.354459, -0.197631, -0.0405458, \
0.11659, 0.273602, 0.430343, 0.586687, 0.742529, 0.897775, 1.05235, \
1.20618, 1.35922, 1.5114, 1.66269, 1.81306, 1.96245, 2.11086, \
2.25825, 2.4046, 2.54989, 2.69411, 2.83725, 2.97928, 3.1202, 3.26, \
3.39867, 3.53621, 3.67261, 3.80786, 3.94195, 4.0749, 4.20668, 4.3373, \
4.46676, 4.59506, 4.72218, 4.84814, 4.97293, 5.09654, 5.21899, \
5.34026, 5.46035, 5.57928, 5.69703, 5.8136, 5.929, 6.04323, 6.15628, \
6.26815, 6.37884, 6.48836, 6.5967, 6.70387, 6.80985, 6.91466, \
7.01828, 7.12073, 7.22199, 7.32207, 7.42097, 7.51868, 7.61521, \
7.71055, 7.8047, 7.89766, 7.98943, 8.08, 8.16938, 8.25757, 8.34455, \
8.43033, 8.5149, 8.59827, 8.68043, 8.76137, 8.8411, 8.91961, 8.99689, \
9.07296, 9.14779, 9.22138, 9.29374, 9.36486, 9.43473, 9.50336, \
9.57072, 9.63683, 9.70167, 9.76524, 9.82754, 9.88855, 9.94828, \
10.0067, 10.0638, 10.1197, 10.1742, 10.2274, 10.2793, 10.3298, \
10.379, 10.4268, 10.4733, 10.5184, 10.5622, 10.6045, 10.6455, 10.685, \
10.7232, 10.7599, 10.7952, 10.8291, 10.8614, 10.8924, 10.9218, \
10.9498, 10.9762, 11.0011, 11.0245, 11.0464, 11.0667, 11.0854, \
11.1025, 11.1181, 11.132, 11.1443, 11.1549, 11.1638, 11.1711, \
11.1766, 11.1804, 11.1825, 11.1827, 11.1812, 11.1779, 11.1728, \
11.1657, 11.1568, 11.146, 11.1332, 11.1185, 11.1017, 11.083, 11.0622, \
11.0392, 11.0142, 10.987, 10.9576, 10.926, 10.8921, 10.8559, 10.8173, \
10.7764, 10.733, 10.6871, 10.6387, 10.5877, 10.534, 10.4776, 10.4185, \
10.3565, 10.2917, 10.2239, 10.153, 10.0791, 10.002, 9.92155, 9.83779, \
9.75057, 9.65979, 9.56537, 9.46717, 9.36509, 9.259, 9.14877, 9.03426, \
8.91531, 8.79177, 8.66347, 8.53021, 8.3918, 8.24803, 8.09866, \
7.94345, 7.78212, 7.61438, 7.43992, 7.25837, 7.06936, 6.87247, \
6.66722, 6.45312, 6.22957, 5.99594, 5.75153, 5.49552, 5.22701, \
4.94497, 4.64823, 4.33546, 4.00512, 3.65548, 3.28457, 2.89015])

t = np.array([0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1., 1.1, 1.2, 1.3, \
1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2., 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, \
2.8, 2.9, 3., 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4., 4.1, \
4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5., 5.1, 5.2, 5.3, 5.4, 5.5, \
5.6, 5.7, 5.8, 5.9, 6., 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, \
7., 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8., 8.1, 8.2, 8.3, \
8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9., 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, \
9.8, 9.9, 10., 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, \
11., 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9, 12., 12.1, \
12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9, 13., 13.1, 13.2, \
13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9, 14., 14.1, 14.2, 14.3, \
14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 15., 15.1, 15.2, 15.3, 15.4, \
15.5, 15.6, 15.7, 15.8, 15.9, 16., 16.1, 16.2, 16.3, 16.4, 16.5, \
16.6, 16.7, 16.8, 16.9, 17., 17.1, 17.2, 17.3, 17.4, 17.5, 17.6, \
17.7, 17.8, 17.9, 18., 18.1, 18.2, 18.3, 18.4, 18.5, 18.6, 18.7, \
18.8, 18.9, 19., 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7, 19.8, \
19.9, 20., 20.1, 20.2, 20.3, 20.4, 20.5, 20.6, 20.7, 20.8, 20.9, 21., \
21.1, 21.2, 21.3, 21.4, 21.5, 21.6, 21.7, 21.8, 21.9, 22., 22.1, \
22.2, 22.3, 22.4, 22.5, 22.6, 22.7, 22.8, 22.9, 23., 23.1])

tnew = np.linspace(0,23.1,200)
xoft = interp1d(t, x)
yoft = interp1d(t, y)

class Comet:
    def get_pos(self,t):
        return np.array([xoft(t%23.1),yoft(t%23.1),0])