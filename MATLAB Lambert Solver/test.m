format long g 
AU= 149597870; % astronomical unit in km 
r1vec= [1.0*AU, 0.0, 0.0]; 
r2vec= [0.0, 1.0*AU, 0.0]; 
tf= 0.25*365; % days 
m= 0.0; % complete nr. of orbits 
muC= 1.327124e11; % Sun grav. parameter in km^3/s^2 
tic
[V1, V2, ~] = lambert(r1vec, r2vec, tf, m, muC); 
toc
V1 = V1 / AU * 365 * 3600 * 24
V2 = V2 / AU * 365 * 3600 * 24