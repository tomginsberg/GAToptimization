import math
import csv
import datetime

##Some information from Wikipedia which we may or may not need
sun = {
    "mass" : 1.989e20 #kg
}
#peri = perihelion distance
#apo = aphelion distance
#t = period of orbit
Mercury = { #Ignoring the perihelion procession which is 574.1 arcseconds/century (100x more than other planets)
    "mass" : 3.301e23, #kg
    "peri" : 69.8169e6,  #km
    "apo"  : 46.0012e6,  #km
    "t" : 87.969 #Period in Earth days
}

Venus = {
    "mass" : 4.867e24, #kg
    "peri" : 107.477e6,  #km
    "apo"  : 108.939e6,  #km
    "t" : 224.701 #Period in Earth days
}

Earth = {
    "mass" : 5.972e24, #kg
    "peri" : 147.1e6,  #km
    "apo"  : 152.1e6,  #km
    "t" : 365.256363 #Period in Earth days
}

Mars = {
    "mass" : 6.417e23, #kg
    "peri" : 206.7e6,  #km
    "apo"  : 249.2e6,  #km
    "t" : 686.971 #Period in Earth days
}

Jupiter = {
    "mass" : 1.899e27, #kg
    "peri" : 740.52e6,  #km
    "apo"  : 816.62e6,  #km
    "t" : 4332.59 #Period in Earth days
}

Saturn = {
    "mass" : 5.685e26, #kg
    "peri" : 1352.55e6,  #km
    "apo"  : 1514.5e6,  #km
    "t" : 10759.22 #Period in Earth days
}

Uranus = {
    "mass" : 8.682e25, #kg
    "peri" : 3008e6,  #km
    "apo"  : 2742e6,  #km
    "t" : 30688.5 #Period in Earth days
}

Neptune = {
    "mass" : 1.024e26, #kg
    "peri" : 4460e6,  #km
    "apo"  : 4540e6,  #km
    "t" : 60182 #Period in Earth days
}

Pluto = {
    "mass" : 1.471e22, #kg
    "peri" : 7375.93e6,  #km
    "apo"  : 4436.82e6,  #km
    "t" : 90560 #Period in Earth days
}

#Should we include Ceres, Pallas, Vesta?

##The acutal simulation
sunMass = 1.989e20 #kg
G = 6.67408e-11 #gravitational constant
au = 149.5978707e6 #astronomical unit in km 

class Planet:
    def __init__(self, mass, perihelion, aphelion, period):
        self.m = mass
        self.peri = perihelion
        self.apo = aphelion
        self.t = period
        
        self.a = None #Semimajor axis (au)
        self.aDot = None #Time deriv of semimajor axis
        
        self.e = None #Eccentricity (unitless)
        self.eDot = None
        
        self.incl = None #Inclination (radians)
        self.inclDot = None
        
        self.long = None #Mean longitude (radians)
        self.longDot = None
        
        self.long_peri = None #Longitude of Perihelion (radians)
        self.long_periDot = None
        
        self.long_asc = None #Longitude of Ascending Node (radians)
        self.long_ascDot = None
        
        self.E = None
    
    #Convert date given by datetime.datetime() into centuries since J2000
    def timeSinceJ2000(date):
        return (((((((date.year-2000)*365.25+int(date.strftime("%j")))*24)+date.hour-12)*60+date.minute)*60)+date.second) / (60*60*24*365.25*100)

    #Calculate position of Planet in au
    def pos(self, time):
        time = Planet.timeSinceJ2000(time)
        
        #Update Keplerian Elements
        Lmean = self.long + self.longDot * time
        Lperi = self.long_peri + self.long_periDot * time
        Lasc = self.long_asc + self.long_ascDot * time
        e = self.e + self.eDot * time
        a = self.a + self.aDot * time
        i = self.incl + self.inclDot * time
        
        #Find Eccentric Anomaly
        M = Lmean - Lperi
        w = Lperi - Lasc
        
        ##Use Newton's Method to solve Kepler's Equation for Mean Anomaly
        #Seed E as M or as the last calculated E
        if self.E == None:
            E = M
        else:
            E = self.E
        #Newton's Method
        while( True ): 
            dE = (E - e * math.sin(E) - M)/(1 - e * math.cos(E))
            E -= dE
            if( abs(dE) < 1e-6 ):
                break

        #Save the last calculated E for next time
        self.E = E
        
        #Find position in some arbitrary basis with P pointing towards periapsis
        P = a * (math.cos(E) - e)
        Q = a * math.sin(E) * math.sqrt(1 - math.pow(e, 2))

        ##Rotate into 3d in sun's reference frame
        #Rotate by argument of periapsis
        x = math.cos(w) * P - math.sin(w) * Q
        y = math.sin(w) * P + math.cos(w) * Q
        #Rotate by inclination
        z = math.sin(i) * x
        x = math.cos(i) * x
        #rotate by longitude of ascending node
        xtemp = x
        x = math.cos(Lasc) * xtemp - math.sin(Lasc) * y
        y = math.sin(Lasc) * xtemp + math.cos(Lasc) * y
        
        return [x,y,z]

##Create Planet objects and read in data from JPL
mercury = Planet(Mercury["mass"], Mercury["peri"], Mercury["apo"], Mercury["t"])
venus = Planet(Venus["mass"], Venus["peri"], Venus["apo"], Venus["t"])
earth = Planet(Earth["mass"], Earth["peri"], Earth["apo"], Earth["t"])
mars = Planet(Mars["mass"], Mars["peri"], Mars["apo"], Mars["t"])
jupiter = Planet(Jupiter["mass"], Jupiter["peri"], Jupiter["apo"], Jupiter["t"])
saturn = Planet(Saturn["mass"], Saturn["peri"], Saturn["apo"], Saturn["t"])
uranus = Planet(Uranus["mass"], Uranus["peri"], Uranus["apo"], Uranus["t"])
neptune = Planet(Neptune["mass"], Neptune["peri"], Neptune["apo"],  Neptune["t"])
pluto = Planet(Pluto["mass"], Pluto["peri"], Pluto["apo"], Pluto["t"])

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

#Read in some Keplerian Element data from JPL
with open('keplerElements.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    count = 0
    for row in csv_reader:
        if count != 0:
            pCount = 1
            for p in planets:
                if count == 1:
                    p.a = float(row[pCount])
                elif count == 2:
                    p.aDot = float(row[pCount])
                elif count == 3:
                    p.e = float(row[pCount])
                elif count == 4:
                    p.eDot = float(row[pCount])
                elif count == 5:
                    p.incl = float(row[pCount]) * math.pi / 180
                elif count == 6:
                    p.inclDot = float(row[pCount]) * math.pi / 180
                elif count == 7:
                    p.long = float(row[pCount]) * math.pi / 180
                elif count == 8:
                    p.longDot = float(row[pCount]) * math.pi / 180
                elif count == 9:
                    p.long_peri = float(row[pCount]) * math.pi / 180
                elif count == 10:
                    p.long_periDot = float(row[pCount]) * math.pi / 180
                elif count == 11:
                    p.long_asc = float(row[pCount]) * math.pi / 180
                elif count == 12:
                    p.long_ascDot = float(row[pCount]) * math.pi / 180
                pCount += 1
        count += 1
print("Successfully Obtained Keplerian Element Data")        


##Simulate orbits for some timeframe
i = 0
rme = [[], [], []]
rv = [[], [], []]
re = [[], [], []]
rm = [[], [], []]
rj = [[], [], []]
rs = [[], [], []]
ru = [[], [], []]
rn = [[], [], []]
rp = [[], [], []]
for yr in range(1,248):
    for month in range(1,12):
        for day in range(1,28):
            d = datetime.datetime(2000+yr, month, day, 12, 0, 0)

            R = mercury.pos(d)
            rme[0].append(R[0])
            rme[1].append(R[1])
            rme[2].append(R[2])

            R = venus.pos(d)
            rv[0].append(R[0])
            rv[1].append(R[1])
            rv[2].append(R[2])

            R = earth.pos(d)
            re[0].append(R[0])
            re[1].append(R[1])
            re[2].append(R[2])

            R = mars.pos(d)
            rm[0].append(R[0])
            rm[1].append(R[1])
            rm[2].append(R[2])

            R = jupiter.pos(d)
            rj[0].append(R[0])
            rj[1].append(R[1])
            rj[2].append(R[2])

            R = saturn.pos(d)
            rs[0].append(R[0])
            rs[1].append(R[1])
            rs[2].append(R[2])

            R = uranus.pos(d)
            ru[0].append(R[0])
            ru[1].append(R[1])
            ru[2].append(R[2])

            R = neptune.pos(d)
            rn[0].append(R[0])
            rn[1].append(R[1])
            rn[2].append(R[2])

            R = pluto.pos(d)
            rp[0].append(R[0])
            rp[1].append(R[1])
            rp[2].append(R[2])

            i += 1

##Plot the orbits
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(rme[0],rme[1],rme[2])
ax.plot(rv[0],rv[1],rv[2])
ax.plot(re[0],re[1],re[2])
ax.plot(rm[0],rm[1],rm[2])
ax.plot(rj[0],rj[1],rj[2])
ax.plot(rs[0],rs[1],rs[2])
ax.plot(ru[0],ru[1],ru[2])
ax.plot(rn[0],rn[1],rn[2])
ax.plot(rp[0],rp[1],rp[2])

