function render(path, planets, dt)
    %Render the planets'/spacecraft's movement and save list of discrete
    %positions of each object in .csv file for rendering with other program
    
    %Create vector for one orbital period of each planet
    for i = 1:9
        t = linspace(0,planets(i).period,5000);
        for j = 1:numel(t)
            [orb(j,1) orb(j,2)] = planets(i).pos(t(j));
            orbits{i} = orb;
        end
        
    end
    
    %Create vector of actual planet positions at time t
    t = dt:dt:size(path,2)*dt;
    for i = 1:numel(t)
        for j = 1:9
            [px(i,j), py(i,j)] = planets(j).pos(t(i));
        end
    end
    
    %Find sizes of planet dots for rendering
    for j = 1:9
        sz(j) = planets(j).planet_radius / 10;
    end
    
    %Plot
    for i = 1:100
        %Plot sun and planet paths
        scatter(0,0,200,'y.')
        hold on
        for j = 1:9
            orb = orbits{j};
            plot(orb(:,1), orb(:,2), '--')
        end
        %Plot spacecraft and its path
        plot(path(1,1:i), path(2,1:i))
        scatter(path(1,i), path(2,i), 'b.')
        %Plot planets
        scatter(px(i,:), py(i,:), sz, 'r.');
        
        xlim([min(path(1,i)*2, -path(1,i)*2) max(path(1,i)*2, -path(1,i)*2)])
        ylim([min(path(2,i)*2, -path(2,i)*2) max(path(2,i)*2, -path(2,i)*2)])
        hold off
        
        if i < 21
            startPoint = i;
        else
            startPoint = i - 20;
        end

        M(i) = getframe;
    end
    
    %Write data to csv in following format:
    %        x positions                                y positions
    % ship, mercury, venus, earth,..., pluto, ship, mercury, venus, earth,..., pluto
    out = [path(1,:)' px path(2,:)' py];
    csvwrite('output.csv',out);
    
    close all
    movie(M);
end