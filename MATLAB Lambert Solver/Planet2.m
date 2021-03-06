classdef Planet2
    properties
        a
        aDot
        e
        eDot
        long
        longDot
        long_peri
        long_periDot
        long_asc
        long_ascDot
        E
        planet_radius
        mass
        period
    end
    methods
        function obj = Planet2(a,aDot,e,eDot,long,longDot,long_peri,long_periDot,long_asc,long_ascDot,planet_radius,mass,period)
            obj.a = a;
            obj.aDot = aDot;
            obj.e = e;
            obj.eDot = eDot;
            obj.long = long;
            obj.longDot = longDot;
            obj.long_peri = long_peri;
            obj.long_periDot = long_periDot;
            obj.long_asc = long_asc;
            obj.long_ascDot = long_ascDot;
            obj.planet_radius = planet_radius;
            obj.mass = mass;
            obj.E = NaN;
            obj.period = period;
        end
        
        %Time 0 is at J2000. Enter time in days after
        %Returns velocity in km/sec
        function v = vel(obj, t, dt)
            AU= 149597870;
            [x1, y1] = obj.pos(t);
            [x2, y2] = obj.pos(t+dt);
            v = [(x2-x1)*AU/(dt * 3600 * 24) (y2-y1)*AU/(dt * 3600 * 24)];
        end
        
        %Returns velocity in AU/day
        function v = velAU(obj, t, dt)
            [x1, y1] = obj.pos(t);
            [x2, y2] = obj.pos(t+dt);
            v = [(x2-x1)/dt (y2-y1)/dt];
        end
        
        %Time 0 is at J2000. Enter time in days after
        %Returns x and y position in sun frame in AU
        function [x, y] = pos(obj, t)
            time = t / (365*100);
            
            Lmean = obj.long + obj.longDot * time;
            Lperi = obj.long_peri + obj.long_periDot * time;
            Lasc = obj.long_asc + obj.long_ascDot * time;
            e = obj.e + obj.eDot * time;
            a = obj.a + obj.aDot * time;

            %Find Eccentric Anomaly
            M = Lmean - Lperi;
            w = Lperi - Lasc;

            %Use Newton's Method to solve Kepler's Equation for Mean Anomaly
            %Seed E as M or as the last calculated E
            if isnan(obj.E)
                E = M;
            else
                E = obj.E;
            end
            %Newton's Method
            while (true) 
                dE = (E - e * sin(E) - M)/(1 - e * cos(E));
                E = E - dE;
                if (abs(dE) < 1e-6)
                    break;
                end
            end
            %Save the last calculated E for next time
            obj.E = E;

            %Find position in some arbitrary basis with P pointing towards periapsis
            P = a * (cos(E) - e);
            Q = a * sin(E) * sqrt(1 - e^2);

            %Rotate by argument of periapsis
            x = cos(w) * P - sin(w) * Q;
            y = sin(w) * P + cos(w) * Q;
            %rotate by longitude of ascending node
            xtemp = x;
            x = cos(Lasc) * xtemp - sin(Lasc) * y;
            y = sin(Lasc) * xtemp + cos(Lasc) * y;
        end
    end
end