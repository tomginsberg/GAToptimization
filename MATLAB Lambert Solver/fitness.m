function val = fitness(ship_velocity_in, ship_velocity_out, planet_velocity)
    % The idea behind this:
    
    % thrust - Minimize how much we have to speed up during the assist, which is
    % proportional to how much fuel we use 
    
    % dirVal - Try to come into a planet as close as possible to the
    % planet's direction to increase the efficiency of the assist. Also
    % bias toward assists that end with the ship leaving in the direction
    % as close as possible to the direction of the planet.
    
    % In calculation of dirVal, take the normed ship velocities so it
    % doesn't bias towards fast ship trajectories


    dirVal = dot(ship_velocity_in/norm(ship_velocity_in), planet_velocity/norm(planet_velocity)) + dot(ship_velocity_out/norm(ship_velocity_out), planet_velocity/norm(planet_velocity));
    thrust = norm(ship_velocity_out - planet_velocity) / norm(ship_velocity_in - planet_velocity);
    thrust = 1-abs(1-thrust);
    
    val = dirVal + thrust;
end