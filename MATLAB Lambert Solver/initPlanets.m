function [planets, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto] = initPlanets()
M = csvread('keplerElements.csv',1,1);
a = M(1,:);
aDot = M(2,:);
e = M(3,:);
eDot = M(4,:);
long = M(7,:) * pi/180;
longDot = M(8,:) * pi/180;
long_peri = M(9,:) * pi/180;
long_periDot = M(10,:) * pi/180;
long_asc = M(11,:) * pi/180;
long_ascDot = M(12,:) * pi/180;
mass = M(13,:);
radius = M(14,:) / 2;
period = M(15,:);

i=1;
mercury = Planet2(a(i),aDot(i),e(i),eDot(i),long(i),longDot(i),long_peri(i),long_periDot(i),long_asc(i),long_ascDot(i),radius(i),mass(i),period(i));
i = i + 1;
venus = Planet2(a(i),aDot(i),e(i),eDot(i),long(i),longDot(i),long_peri(i),long_periDot(i),long_asc(i),long_ascDot(i),radius(i),mass(i),period(i));
i = i + 1;
earth = Planet2(a(i),aDot(i),e(i),eDot(i),long(i),longDot(i),long_peri(i),long_periDot(i),long_asc(i),long_ascDot(i),radius(i),mass(i),period(i));
i = i + 1;
mars = Planet2(a(i),aDot(i),e(i),eDot(i),long(i),longDot(i),long_peri(i),long_periDot(i),long_asc(i),long_ascDot(i),radius(i),mass(i),period(i));
i = i + 1;
jupiter = Planet2(a(i),aDot(i),e(i),eDot(i),long(i),longDot(i),long_peri(i),long_periDot(i),long_asc(i),long_ascDot(i),radius(i),mass(i),period(i));
i = i + 1;
saturn = Planet2(a(i),aDot(i),e(i),eDot(i),long(i),longDot(i),long_peri(i),long_periDot(i),long_asc(i),long_ascDot(i),radius(i),mass(i),period(i));
i = i + 1;
uranus = Planet2(a(i),aDot(i),e(i),eDot(i),long(i),longDot(i),long_peri(i),long_periDot(i),long_asc(i),long_ascDot(i),radius(i),mass(i),period(i));
i = i + 1;
neptune = Planet2(a(i),aDot(i),e(i),eDot(i),long(i),longDot(i),long_peri(i),long_periDot(i),long_asc(i),long_ascDot(i),radius(i),mass(i),period(i));
i = i + 1;
pluto = Planet2(a(i),aDot(i),e(i),eDot(i),long(i),longDot(i),long_peri(i),long_periDot(i),long_asc(i),long_ascDot(i),radius(i),mass(i),period(i));

planets = [mercury venus mars earth jupiter saturn uranus neptune pluto];
end