import peasy.*;

Planet sun;
Planet galaxy;
PeasyCam cam;

int numPlanets = 8;
float earthRadius = 3;
float earthDist = 60;

float earthPeriod = 200; // How many frames the whole year should take

PImage sunTexture;
PImage[] textures = new PImage[numPlanets];

float startTime;
float endTime;

float time;
float totalTime;

PShape comet;
int cometIndex;

int points;
int solL;
int cometPeriod = 23;
Table table;

float cometIndexF;
float dxCom;
float dyCom;
int trajIndex;
float trajIndexF;

float dx = 0;
float dy = 0;
float vel = 0;

float dxT = 0;
float dyT = 0;



Table logData;

float[] phases = {0,0,0,0,0,0,0,0};

void setup() {
  fullScreen(P3D);
  sunTexture = loadImage("sun.jpg");
  textures[0] = loadImage("mercury.jpg");
  textures[1] = loadImage("venus.jpg");
  textures[2] = loadImage("earth.jpg");
  textures[3] = loadImage("mars.jpg");
  textures[4] = loadImage("jupiter.jpg");
  textures[5] = loadImage("saturn.jpg");
  textures[6] = loadImage("uranus.jpg");
  textures[7] = loadImage("neptune.jpg");


  logData = loadTable("log.csv", "header");
  startTime = logData.getFloat(0,0);
  endTime = logData.getFloat(0,1);

  for(int i = 0; i < numPlanets; i++){
    phases[i] += wp[i] * startTime * earthPeriod - PI/2 + logData.getFloat(1, i);
  }

  cam = new PeasyCam(this,500);
  cam.rotateX(PI / 2);
  cam.setWheelScale(.01);

  sun = new Planet(4 * earthRadius, 0, 0, sunTexture, new PVector(0,0,0), 0);
  galaxy = new Planet(4000, 0, 0, loadImage("galaxy.png"), new PVector(0,0,0), 0);
  sun.spawnMoons();

  comet = createShape(SPHERE, earthRadius);
  comet.setTexture(loadImage("comet.jpg"));
  points = cometX.length;
  table = loadTable("data.csv", "header");
  solL = table.getRowCount();

  time = startTime;
  totalTime = endTime-startTime;

}

void draw() {
  frameRate(30);

  translate( -earthDist * (table.getFloat(trajIndex,1) + dxT), 0, -earthDist * (table.getFloat(trajIndex,0) + dyT));

  background(0);
  ambientLight(255,255,255);
  pointLight(255, 255, 255, 0, 0, 0);
  galaxy.show();
  sun.show();
  //cam.lookAt( earthDist * (solX[floor(solL * (time % endTime)/endTime)] + dxT), 0, earthDist * (solY[floor(solL * (time % endTime)/endTime)] + dyT) );

  noFill();
  stroke(255,255,255);
  rotateX(PI/2);
  for(int i = 0; i < dp.length; i ++){
      ellipse(0,0,2*dp[i],2*dp[i]);
  }
  smooth();
  noFill();
  stroke(255, 0, 0);
  beginShape();
    curveVertex(earthDist*cometX[0], earthDist*cometY[0]);
    for (int i = 0; i < points ; i++){
      curveVertex(earthDist*cometX[i], earthDist*cometY[i]);
    }
    curveVertex(earthDist*cometX[0], earthDist*cometY[0]);
    curveVertex(earthDist*cometX[0], earthDist*cometY[0]);
  endShape();

  if (trajIndex < solL -2){

    cometIndexF = points * (time % cometPeriod)/cometPeriod;
    cometIndex = floor(cometIndexF);
    dxCom = (cometX[(cometIndex + 1) % points] - cometX[cometIndex])*(cometIndexF - cometIndex);
    dyCom = (cometY[(cometIndex + 1) % points] - cometY[cometIndex])*(cometIndexF - cometIndex);

    stroke(244, 161, 66);
    trajIndexF = solL * (time-startTime)/(totalTime);
    trajIndex = floor(trajIndexF);

    dx = (table.getFloat(trajIndex + 1,1) - table.getFloat(trajIndex,1));
    dy = (table.getFloat(trajIndex + 1,0) - table.getFloat(trajIndex,0));

    vel = pow(pow((dx*1.496*pow(10, 8))/(totalTime/solL * 8760.0)) + pow((dy*1.496*pow(10, 8))/(totalTime/solL * 8760.0)), 0.5);

    text ( "Current Velocity: " + vel, 10, 10);

    dxT = dx*(trajIndexF - trajIndex);
    dyT = dy*(trajIndexF - trajIndex);
    sun.orbit(1);
  }
  shape(comet, earthDist * (cometX[cometIndex] + dxCom), earthDist * (cometY[cometIndex] + dyCom));

  beginShape();
    curveVertex(earthDist * table.getFloat(0,1), earthDist * table.getFloat(0,0));
    for (int i = 0; i < trajIndex ; i++){
      curveVertex(earthDist * table.getFloat(i,1),earthDist * table.getFloat(i,0));
    }



      curveVertex(earthDist * (table.getFloat(trajIndex,1) + dxT), earthDist * (table.getFloat(trajIndex,0) + dyT));
      curveVertex(earthDist * (table.getFloat(trajIndex,1) + dxT), earthDist * (table.getFloat(trajIndex,0) + dyT));

  endShape();


  time = time + 1/earthPeriod;
}
