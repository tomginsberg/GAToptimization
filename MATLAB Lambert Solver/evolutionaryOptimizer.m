%%Define planets
% Mercury = Planet(6.556591516975463e7, 2439.75, 87.96926, 22031.405043200, pi/2) ;
% Venus = Planet(1.0880283855320331e8, 6051.855, 224.70080, 324848.8306, 3 * pi/4); 
% Earth = Planet(1.4923686920307517e8, 6371.0087, 365.25636, 398589.31232288, 0); 
% Mars = Planet(2.3360709224817526e8, 3389.55, 686.97959, 42827.104, pi +.7); 
% Jupiter = Planet(7.964720406084917e8, 69911.5, 4332.8201, 1.266827e8, pi/4 + .38);
% 
% planets = [Mercury, Venus, Earth, Mars, Jupiter];

%Initialize planets
planets = initPlanets();

%Some important parameters
kstoauyear = 0.210805;
sgp = 1.327124e11; %Sun gravitational parameter in km^3/s^2
AU =  149597870; % astronomical unit in km

%%Starting planet 
startPlanet = 3;
%%Ending planet
endPlanet = 5;
%%Number of trajectories to test
numTrajectories = 100;

%%Number of gravity assists during the trajectory
assistRange = [0,7];

%%Generate a random number of assists
assists = randi(assistRange);

%%Pick numTrajectories random trajectories starting at startPlanet and ending at
%%endPlanet

%Limit possible planets on trajectory to reasonable bounds
minPlanet = min(startPlanet, endPlanet) - 3;
if (minPlanet < 0); minPlanet = 0; end
maxPlanet = max(startPlanet, endPlanet) + 2;
if (maxPlanet > 9); maxPlanet = 9; end

%Generate the random trajectories within the given limits
trajs(:,2:assists+1) = randi(maxPlanet,numTrajectories,assists) + minPlanet;
trajs(:,1) = startPlanet;
trajs(:,assists+2) = endPlanet;

%Look for repeated values in a row and replace with different value
for i = 1:numTrajectories 
    for j = 2:assists+1
        if trajs(i,j) == trajs(i,j-1) || trajs(i,j) == trajs(i,j+1)
            num = randi(9,1);
            while trajs(i,j-1) == num || trajs(i,j+1) == num
                num = randi(9,1);
            end
            trajs(i,j) = num;
        end
    end
    %trajs(i,2:assists+1) = randperm(9,assists); %A way to create trajectories that only visit each planet once
end

%Time range
timeRange = [10, 1000];

%Pick numTrajectories random transfer times
times(:,2:assists+1) = randi(6,numTrajectories,assists) * 30;
times(:,1) = 0;

%%Calculate fitness
numGenerations = 1000;
for g = 1:numGenerations
    vOut = zeros(numTrajectories,assists+1,3);
    vIn = zeros(numTrajectories,assists+1,3);
    fit = zeros(numTrajectories,assists+1);
    fitnessVal = zeros(numTrajectories);
    
    for i = 1:numTrajectories
        for a = 1:assists+1
            %%%Calculate in/out velocities from planets based on Lambert solutions
            %Find current position of current planet
            [pos1x, pos1y] = planets(trajs(a)).pos(sum(times(i,1:a-1)));
            
            %Find position of destination planet at selected eta
            [pos2x, pos2y] = planets(trajs(a+1)).pos(sum(times(i,1:a)));
            
            %Set up variables for Lambert problem
            r1 = [pos1x*AU pos1y*AU 0.0];
            r2 = [pos2x*AU pos2y*AU 0.0];
            t = times(a);
            numOrbits = 0; %TODO - Is this optimal??
            
            %Solve Lambert problem -- TODO only returns NaN at the moment...
            [vOut(i,a,:), vIn(i,a,:), ~] = lambert(r1*AU, r2*AU, t, numOrbits, sgp);
        end
    end
    
    %Calculate fitnesses of each interaction
    for i = 1:numTrajectories
        %Calculate fitness of velocity leaving start planet
        fit(i,1) = fitness(vOut(i,1,:),[],[]);
        
        %Start at a=2 because leaving startPlanet there is no incoming velocity
        %Don't calculate a fitness value for the final planet either
        for a = 2:assists+1 
            %Calculate fitness of each interaction based on velocities
            fit(i,a) = fitness(vOut(i,a,:), vIn(i,a-1,:), planets(a).vel(times(i,sum(1:a))));
        end
        
        %Find total fitness along entire trajectory
        fitnessVal(i) = sum(fit(i,:));
        
        %Kill bad trajectories by keeping only those with highest fitness
        k = 2; % TODO what proportion to kill??
        [~,idx] = maxk(fitnessVal, numTrajectories / k);
        numTrajectories = numTrajectories / k;
        trajs(idx,:,:) = [];
        times(idx,:,:) = [];
        
        %Mutate good trajectories
        [trajs, times] = mutate(trajs, times);
    end
end