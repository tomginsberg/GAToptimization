import peasy.*;
import interfascia.*;
import java.io.*;

//Interesting parameters
String fullPath = "..\\Desktop\\galaxy\\GAToptimization\\";
int numPlanets = 8;
float earthRadius = 3;
float earthDist = 60;
float earthPeriod = 150;

//Non-Interesting parameters (Do not touch)
GUIController c;
IFButton[] buttons = new IFButton[8];
String dest = "Comet";
String[] planets = {"Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Comet"};
PShader nebula;
PFont cmu;
int programState = 0;

Planet sun;
Planet galaxy;
PeasyCam cam;

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
float dxT = 0;
float dyT = 0;

Table logData;

float[] phases = {0,0,0,0,0,0,0,0};

void setup() {
  fullScreen(P3D);
  //pixelDensity(2);
  sunTexture = loadImage("sun.jpg");
  textures[0] = loadImage("mercury.jpg");
  textures[1] = loadImage("venus.jpg");
  textures[2] = loadImage("earth.jpg");
  textures[3] = loadImage("mars.jpg");
  textures[4] = loadImage("jupiter.jpg");
  textures[5] = loadImage("saturn.jpg");
  textures[6] = loadImage("uranus.jpg");
  textures[7] = loadImage("neptune.jpg");
  
  c = new GUIController (this);

  nebula = loadShader("nebula2.glsl");
  nebula.set("resolution", float(width), float(height));

  
  int bWidth = 80;
  int bHeight = 30;
  int xB = 20;
  int yB = 90;

  for(int i = 0; i < planets.length; i++){
      buttons[i] = new IFButton (planets[i], xB+(bWidth+10)*i, yB, bWidth, bHeight);
      buttons[i].addActionListener(this);
      c.add(buttons[i]);
  }
  cmu = loadFont("CMUSerif-Bold-48.vlw");
}

void draw() {
  if(programState == 0){
    background(0);
    nebula.set("time", millis() / 500.0);  
    shader(nebula); 
    rect(0, 0, width, height);
    resetShader();
    fill(255);
    textFont(cmu);
    textSize(36);
    text("fps: " + round(frameRate), 1000, 50);
    text("MGA Trajectory Optimizer: Choose a Destination",20,50);
    textSize(16);
    text("By David Black, Tom Ginsberg, Bereket Guta, Calum Macdonald, and Jeremy Wong",20,70);
    textSize(26);
    text("Selected "+dest+". Press Enter to Generate Trajectory", 20, 150);
    
  }else if(programState == 1){  
    textSize(26);
    text("Please wait while we evolve towards the optimal trajectory...", 20, 180);
    programState = 2;
    
  }else if (programState == 2){
    String s = null;
    try {
        
        Process p = Runtime.getRuntime().exec("python "+fullPath+"MGA.py " + dest);
        
        BufferedReader stdInput = new BufferedReader(new 
             InputStreamReader(p.getInputStream()));

        BufferedReader stdError = new BufferedReader(new 
             InputStreamReader(p.getErrorStream()));

        // read the output from the command
        System.out.println("Here is the standard output of the command:\n");
        while ((s = stdInput.readLine()) != null) {
            System.out.println(s);
        }
        
        // read any errors from the attempted command
        System.out.println("Here is the standard error of the command (if any):\n");
        while ((s = stdError.readLine()) != null) {
            System.out.println(s);
        }
        
    }
    catch (IOException e) {
        System.out.println("exception happened - here's what I know: ");
        e.printStackTrace();
        System.exit(-1);
    }
    programState = 3;
  }else if(programState ==3){
    for(IFButton b : buttons){
      c.remove(b);
    }
    cam = new PeasyCam(this,500);
    cam.rotateX(PI / 2);
    cam.setWheelScale(1);

    logData = loadTable("log.csv", "header");
    startTime = logData.getFloat(1,0);
    endTime = logData.getFloat(1,1);
    for(int i = 0; i < numPlanets; i++){
      phases[i] += wp[i] * startTime * earthPeriod - PI/2 + logData.getFloat(3, i);
    }

    
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
    programState = 4;

    
  }else if(programState == 4){
    if (time < startTime + 2/earthPeriod){
     delay(1000);
    }else{ frameRate(30);}
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
      
      dxT = (table.getFloat(trajIndex + 1,1) - table.getFloat(trajIndex,1))*(trajIndexF - trajIndex);
      dyT = (table.getFloat(trajIndex + 1,0) - table.getFloat(trajIndex,0))*(trajIndexF - trajIndex);
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
}
void keyPressed(){
  if (keyCode == ENTER && programState == 0){
    programState = 1; 
  }
}
void actionPerformed (GUIEvent e) {
  for(int i = 0; i < planets.length; i++){
    if (e.getSource() == buttons[i]) {
        dest = planets[i];
    }
  }
}
