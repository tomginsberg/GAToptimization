classdef Planet
    properties
        planet_radius
        orbit_radius
        period
        name
        mass
        phase
    end
    methods
        function [x, y] = get_pos(obj, time)
            x = obj.orbit_radius * cos(obj.phase + 1/obj.period * 2*pi * time);
            y = obj.orbit_radius * sin(obj.phase + 1/obj.period * 2*pi * time);
        end
        
    end
end