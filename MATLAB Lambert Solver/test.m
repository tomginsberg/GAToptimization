%% Test Lambert solver
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

%% Test planet creator
clear
[mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto] = initPlanets();
[x,y] = earth.pos(100);
px = [];
py = [];
t = 1;
dt = 100;
for i = 1:1000
    [px(i,1), py(i,1)] = earth.pos(t);
    [px(i,2), py(i,2)] = mercury.pos(t);
    [px(i,3), py(i,3)] = venus.pos(t);
    [px(i,4), py(i,4)] = mars.pos(t);
    [px(i,5), py(i,5)] = jupiter.pos(t);
    [px(i,6), py(i,6)] = saturn.pos(t);
    [px(i,7), py(i,7)] = uranus.pos(t);
    [px(i,8), py(i,8)] = neptune.pos(t);
    [px(i,9), py(i,9)] = pluto.pos(t);
    
    scatter(px(i,:), py(i,:), 'r.');
    if i < 21
        startPoint = i;
    else
        startPoint = i - 20;
    end
    
    plot(px(startPoint:i,:),py(startPoint:i,:));
    xlim([-30 30])
    ylim([-30 30])
    M(i) = getframe;
    t = t + dt;
end
movie(M);