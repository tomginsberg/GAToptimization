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
[planets, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto] = initPlanets();
px = [];
py = [];
n = 10000;
t = linspace(1,pluto.period,n);
sz = ones(1,9);
for i = 1:n
    for j = 1:9
        [px(i,j) py(i,j)] = planets(j).pos(t(i));
        sz(j) = planets(j).planet_radius / 100;
    end
end

f = figure;
f.set('visible','off')
for i = 1:1000
    plot(px, py, '--')
    hold on
    scatter(px(i,:), py(i,:), sz, 'r.');
    xlim([-33 48])
    ylim([-33 48])

    hold off
    if i < 21
        startPoint = i;
    else
        startPoint = i - 20;
    end
    
    %plot(px(startPoint:i,:),py(startPoint:i,:));
    M(i) = getframe;
end

movie(M);