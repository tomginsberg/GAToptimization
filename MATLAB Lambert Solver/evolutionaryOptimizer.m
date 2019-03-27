%%Define planets
Mercury = Planet(6.556591516975463e7, 2439.75, 87.96926, 22031.405043200, pi/2) ;
Venus = Planet(1.0880283855320331e8, 6051.855, 224.70080, 324848.8306, 3 * pi/4); 
Earth = Planet(1.4923686920307517e8, 6371.0087, 365.25636, 398589.31232288, 0); 
Mars = Planet(2.3360709224817526e8, 3389.55, 686.97959, 42827.104, pi +.7); 
Jupiter = Planet(7.964720406084917e8, 69911.5, 4332.8201, 1.266827e8, pi/4 + .38);

planets = [Mercury, Venus, Earth, Mars, Jupiter];
kstoauyear = 0.210805;
%%
%%Starting planet 
startPlanet = 3;
%%Ending planet
endPlanet = 5;

%%Number of gravity assists during the trajectory
assistRange = [2,7];

%%Generate a random number of assists
assists = randi(assistRange);
%%Pick 100 random trajectories
trajs = randi(5,100,assists);

%Time range
timeRange = [10, 1000];

%Pick 100 random transfer times 
times = randi(5,100,assists);

%%Calculate fitness



