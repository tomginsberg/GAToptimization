%%Define planets
Mercury = Planet(6.556591516975463e7, 2439.75, 87.96926, 22031.405043200, pi/2) ;
Venus = Planet(1.0880283855320331e8, 6051.855, 224.70080, 324848.8306, 3 * pi/4); 
Earth = Planet(1.4923686920307517e8, 6371.0087, 365.25636, 398589.31232288, 0); 
Mars = Planet(2.3360709224817526e8, 3389.55, 686.97959, 42827.104, pi +.7); 
Jupiter = Planet(7.964720406084917e8, 69911.5, 4332.8201, 1.266827e8, pi/4 + .38);

planets = [Mercury, Venus, Earth, Mars, Jupiter];

%planets = initPlanets(); % More realistic planets...

kstoauyear = 0.210805;
muC = 1.327124e11; %Sun gravitational parameter in km^3/s^2
AU =  149597870; % astronomical unit in km
%%
%%Starting planet 
startPlanet = 3;
%%Ending planet
endPlanet = 5;
%%Number of trajectories to test
numTrajectories = 100;

%%Number of gravity assists during the trajectory
assistRange = [2,7];

%%Generate a random number of assists
assists = randi(assistRange);

%%Pick 100 random trajectories starting at startPlanet and ending at
%%endPlanet
trajs(2:assists+1,:) = randi(5,numTrajectories,assists);
trajs(1,:) = startPlanet;
trajs(assists+2,:) = endPlanet;

%Time range
timeRange = [10, 1000];

%Pick 100 random transfer times
times(2:assists+1,:) = randi(5,numTrajectories,assists+1) * 30;
for i = 1:assits+1
times(1,:) = 0;

%%Calculate fitness
numGenerations = 1000;
for g = 1:numGenerations
    %Calculate in/out velocities from planets based on Lambert solutions
    for i = 1:numTrajectories
        for a = 1:assists+1
            [pos1x, pos1y] = Planets(trajs(a)).pos(times(a));
            [pos2x, pos2y] = Planets(trajs(a+1)).pos(times(a+1));
            r1 = [pos1x pos1y 0];
            r2 = [];
        end
    end
    %Calculate fitness of each interaction based on velocities
    %Find total fitness along entire trajectory
    %Kill bad trajectories
    %Mutate good trajectories
end