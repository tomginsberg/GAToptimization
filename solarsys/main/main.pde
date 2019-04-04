import peasy.*;
import interfascia.*;
import java.io.*;

//Interesting parameters
String fullPath = "..\\Desktop\\galaxy\\GAToptimization\\";
int numPlanets = 8;
float earthRadius = 3;
float earthDist = 60;
float earthPeriod = 250;
float alpha = 1;
//Non-Interesting parameters (Do not touch)
GUIController c;
IFButton[] buttons = new IFButton[8];
IFButton deadButton = new IFButton(".",0,0,0,0);
IFButton[] sampleButtons = new IFButton[8];
String[] samples = {"Sample 1","Sample 2","Sample 3","Sample 4","Sample 5","Sample 6","Sample 7","Sample 8"};
int velocity;
String logFile;
String dataFile;
float elapsed;
boolean leftCoded = false;
boolean rightCoded = false;

String dest = "Comet";
String[] planets = {"Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Comet"};
PShader nebula;
PFont cmu;
int programState = 0;
boolean choseSample = false;
int sampleNum = 0;

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
      buttons[i] = new IFButton(planets[i], xB+(bWidth+10)*i, yB, bWidth, bHeight);
      buttons[i].addActionListener(this);
      c.add(buttons[i]);
  }

  for(int i = 0; i < samples.length; i++){
      sampleButtons[i] = new IFButton(samples[i], xB+(bWidth+10)*i, yB + bHeight + 10, bWidth, bHeight);
      sampleButtons[i].addActionListener(this);
      c.add(sampleButtons[i]);
  }
  deadButton.addActionListener(this);
  c.add(deadButton);

  cmu = loadFont("CMUSerif-Bold-48.vlw");
}


void draw() {
  if(programState == 0){
    background(0);
    nebula.set("time", (millis() / 1000.0)%146  );  
    shader(nebula); 
    rect(0, 0, width, height);
    resetShader();
    fill(255);
    textFont(cmu);
    textSize(36);
    text("MGA Trajectory Optimizer: Choose a Destination",20,50);
    textSize(16);
    text("By David Black, Tom Ginsberg, Bereket Guta, Calum Macdonald, and Jeremy Wong",20,70);
    textSize(26);
    if (choseSample){
        text("Selected Sample "+sampleNum+". Press Enter to View", 20, 190);
    }else{
      text("Selected "+dest+". Press Enter to Generate Trajectory", 20, 190);
    }
    
  }else if(programState == 1){  
    textSize(26);
    if (choseSample){
        text("Loading Sample...", 20, 215);
    }else{
      text("Please wait while we evolve towards the optimal trajectory...", 20, 215);
    }

    if (choseSample){
        programState = 3;
    }else{
      programState = 2;
    }
    for(IFButton b : buttons){
      c.remove(b);
    }
    for(IFButton b : sampleButtons){
      c.remove(b);
    }
    c.remove(deadButton);
    
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
    
    cam = new PeasyCam(this,500);
    cam.rotateX(PI / 2);
    cam.setWheelScale(1);
    
    logData = loadTable(logFile, "header");
    startTime = logData.getFloat(1,0);
    endTime = logData.getFloat(1,1);
    programState = 4;
  }else if(programState == 4){

    for(int i = 0; i < numPlanets; i++){
      phases[i] += wp[i] * startTime * earthPeriod - PI/2 + logData.getFloat(3, i);
    }
    
    sun = new Planet(4 * earthRadius, 0, 0, sunTexture, new PVector(0,0,0), 0);
    galaxy = new Planet(4000, 0, 0, loadImage("galaxy.png"), new PVector(0,0,0), 0);
    sun.spawnMoons();
    
    comet = createShape(SPHERE, earthRadius);
    comet.setTexture(loadImage("comet.jpg"));
    points = cometX.length;
    table = loadTable(dataFile, "header");
    solL = table.getRowCount();
    
    time = startTime;
    totalTime = endTime-startTime;
    programState = 5;
    
  }else if(programState == 5){
    if (leftCoded && alpha > -1){
      alpha -= .01;
    }else if(rightCoded && alpha < 4){
      alpha += .01;
    }
    if (time < startTime + 1/earthPeriod){
      if (time < startTime){
        time = startTime;
      }
      delay(1000);
    }
    translate( -earthDist * (table.getFloat(trajIndex,1) + dxT), 0, -earthDist * (table.getFloat(trajIndex,0) + dyT));
    
    background(0);
    ambientLight(255,255,255);
    pointLight(255, 255, 255, 0, 0, 0);
    galaxy.show();
    sun.show();
    fill(255);
    elapsed = time - startTime;
    text("Years: "+elapsed,-300,-100,-300);
    noFill();
    stroke(255,255,255);
    rotateX(PI/2);
    for(int i = 0; i < dp.length; i ++){
        if ((i == 5 && (sampleNum == 2 || sampleNum == 4 )) || (i == 4 && sampleNum ==3) || (i == 6 && sampleNum == 7) || (i == 7 && sampleNum == 6 ) ){
          stroke(255, 0, 0);
        }else{
          stroke(255,255,255);
        }
        ellipse(0,0,2*dp[i],2*dp[i]);
    }
    smooth();
    beginShape();
      if ((!choseSample && dest == "Comet") || (choseSample && (sampleNum == 1 || sampleNum == 8 || sampleNum == 5))){
        stroke(255, 0, 0);
      }
      curveVertex(earthDist*cometX[0], earthDist*cometY[0]); 
      for (int i = 0; i < points ; i++){
        curveVertex(earthDist*cometX[i], earthDist*cometY[i]); 
      }
      curveVertex(earthDist*cometX[0], earthDist*cometY[0]); 
      curveVertex(earthDist*cometX[0], earthDist*cometY[0]); 
    endShape();
    stroke(244, 161, 66);
    if (trajIndex < solL - 2){
      
      cometIndexF = points * (time % cometPeriod)/cometPeriod;
      cometIndex = floor(cometIndexF);
      dxCom = (cometX[(cometIndex + 1) % points] - cometX[cometIndex])*(cometIndexF - cometIndex);
      dyCom = (cometY[(cometIndex + 1) % points] - cometY[cometIndex])*(cometIndexF - cometIndex);
      
      
      trajIndexF = solL * (time-startTime)/(totalTime);
      trajIndex = floor(trajIndexF);
      
      dxT = (table.getFloat(trajIndex + 1,1) - table.getFloat(trajIndex,1))*(trajIndexF - trajIndex);
      dyT = (table.getFloat(trajIndex + 1,0) - table.getFloat(trajIndex,0))*(trajIndexF - trajIndex);
      sun.orbit(alpha);
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
    if (time < endTime){
      time = time + 1/earthPeriod * alpha;
    }

    
  }
}

void keyPressed(){
  if (keyCode == ENTER){
    if (programState==0){
      programState = 1; 
    }else if(programState==5){
      time = startTime;
      trajIndex = 0;
      sun.spawnMoons();
    }
  }else if(keyCode == RIGHT){
    rightCoded = true;
  }
  else if(keyCode == LEFT){
    leftCoded = true;
  }
}
void keyReleased(){
  if(keyCode == RIGHT){
    rightCoded = false;
  }
  else if(keyCode == LEFT){
    leftCoded = false;
  }
}
void actionPerformed (GUIEvent e) {
  if (programState == 0){
    for(int i = 0; i < planets.length; i++){
      if (e.getSource() == buttons[i]) {
          dest = planets[i];
          choseSample = false;
          logFile = "log.csv";
          dataFile = "data.csv";
          println("Data "+dataFile+", Log "+logFile);
      }
    }
    for(int i = 0; i < samples.length; i++){
      if (e.getSource() == sampleButtons[i]) {
          sampleNum = i + 1;
          choseSample = true;
          logFile = "log_sample"+sampleNum+".csv";
          dataFile = "data_sample"+sampleNum+".csv";
          println("Data "+dataFile+", Log "+logFile);
      }
    }
  }
}
