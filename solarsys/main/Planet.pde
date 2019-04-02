// Daniel Shiffman
// http://codingtra.in
// http://patreon.com/codingtrain
// Code for: https://youtu.be/FGAwi7wpU8c

class Planet {
  float radius;
  float distance;
  Planet[] planets;
  float angle;
  float orbitspeed;
  PVector v;

  PShape globe;

  Planet(float r, float d, float o, PImage img, PVector p, float phi) {

    v = p;
    radius = r;
    distance = d;
    v.mult(distance);
    angle = phi;
    orbitspeed = o;

    noStroke();
    noFill();
    globe = createShape(SPHERE, radius);
    globe.setTexture(img);
  }

  void orbit(float dt) {
    angle = angle + orbitspeed*dt;
    if (planets != null) {
      for (int i = 0; i < planets.length; i++) {
        planets[i].orbit(dt);
      }
    }
  }

  void spawnMoons() {
    planets = new Planet[numPlanets];
    
    for (int i = 0; i < numPlanets; i++) {
      planets[i] = new Planet(rp[i], dp[i], wp[i], textures[i], new PVector(1,0,0),0);
      
    }
  }

  void show() {
    pushMatrix();
    noStroke();
    PVector v2 = new PVector(0, 0, 1);
    PVector p = v2.cross(v);
    rotate(angle, p.x, p.y, p.z);
    stroke(255);
    
    translate(v.x, v.y, v.z);
    noStroke();
    fill(255);
    shape(globe);

    if (planets != null) {
      for (int i = 0; i < planets.length; i++) {
        planets[i].show();
      }
    }
    popMatrix();
  }
}
