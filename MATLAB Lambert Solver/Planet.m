classdef Planet
    properties
        orbit_radius
        planet_radius
        period
        attractor
        phase
    end
    methods
        function obj = Planet(orbit_radius, planet_radius,period,attractor,phase)
            obj.orbit_radius = orbit_radius;
            obj.planet_radius = planet_radius;
            obj.period = period;
            obj.attractor = attractor;
            obj.phase = phase;
        end
        
        function [x, y] = get_pos(obj, time)
            x = obj.orbit_radius * cos(obj.phase + 1/obj.period * 2*pi * time);
            y = obj.orbit_radius * sin(obj.phase + 1/obj.period * 2*pi * time);
        end
        
    end
end