function val = fitness(ship_velocity_out, ship_velocity_in, planet_velocity)
    % The idea behind this:
    
    % thrust - Minimize how much we have to speed up during the assist, which is
    % proportional to how much fuel we use 
    
    % dirVal - Try to come into a planet as close as possible to the
    % planet's direction to increase the efficiency of the assist. Also
    % bias toward assists that end with the ship leaving in the direction
    % as close as possible to the direction of the planet.
    
    % In calculation of dirVal, the velocities are normed so the output is
    % between 0 and 1
    
    % If no ship_vel_in or planet_vel are given, assume this is the start
    % planet and calculate fitness based only on how much thrust is
    % required for exiting velocity
    
    if isempty(ship_velocity_out) && isempty(planet_velocity)
        val = norm(ship_velocity_out) / 10; % TODO - What is the magnitude of this? Should we divide by larger number?
    else
        dirVal = (dot(ship_velocity_in/norm(ship_velocity_in), planet_velocity/norm(planet_velocity)) + dot(ship_velocity_out/norm(ship_velocity_out), planet_velocity/norm(planet_velocity)))/2;
        thrust = norm(ship_velocity_out - planet_velocity) / norm(ship_velocity_in - planet_velocity);
        thrust = 1-abs(1-thrust);
        val = dirVal + thrust;
    end
end