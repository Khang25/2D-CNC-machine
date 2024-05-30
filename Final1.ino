
#include <AccelStepper.h>
#include <MultiStepper.h>

// Define Pin for motor
const int stepPinX = 2;
const int dirPinX = 3;
const int enablePinX = 13;

const int stepPinY1 = 4;
const int dirPinY1 = 5;
const int stepPinY2 = 6;
const int dirPinY2 = 7;
const int enablePinY = 14;

const int stepPinZ = 8;
const int dirPinZ = 9;
const int enablePinZ = 15;

const int enableAllPin = 16;

// Define Pin for Limit Switch
const int limitSwitchX = 10;
const int limitSwitchY = 11;
const int limitSwitchZ = 12;

int Accel_X = 300;
int Accel_Y = 300;


int High_Step = 0;
int common_Step = 0;

char Serial_Read();
void Reset_All();
void Move_by_Distance(float Distance[]);

int dirPin[4] = {dirPinX, dirPinY1, dirPinY2, dirPinZ};
int stepPin[4] = {stepPinX, stepPinY1, stepPinY2, stepPinZ};

AccelStepper x_axis(AccelStepper::DRIVER, stepPin[0], dirPin[0]);
AccelStepper y1_axis(AccelStepper::DRIVER, stepPin[1], dirPin[1]);
AccelStepper y2_axis(AccelStepper::DRIVER, stepPin[2], dirPin[2]);
AccelStepper z_axis(AccelStepper::DRIVER, stepPin[3], dirPin[3]);
MultiStepper steppers;

float Home_X = 0;
float Home_Y1 = 0;
float Home_Y2 = 0;
float Home_Z = 0;

float Current_Pos_X;
float Current_Pos_Y1;
float Current_Pos_Y2;
float Current_Pos_Z;

unsigned int E_X; // out of working area
unsigned int E_Y1;
unsigned int E_Y2;
unsigned int E_Z;

float Dist_To_Move[3];
long Stp_To_Move[4];
unsigned int M_Direction[3] = {0, 0, 0}; // moving direction

//---------Declaration Flag-------//
//-------------------------------//

int S_Flag = 0; // Serial flag
int D_Flag = 0;
int M_Flag = 0; // moving flag
int M_All = 0;
String inData;
char K;

void setup() {
  Serial.begin(115200);
  pinMode(17, OUTPUT);
  digitalWrite(17, 0);

  x_axis.setCurrentPosition(0);
  y1_axis.setCurrentPosition(0);
  y2_axis.setCurrentPosition(0);
  z_axis.setCurrentPosition(0);
  
  x_axis.setMaxSpeed(900);
  y1_axis.setMaxSpeed(900);
  y2_axis.setMaxSpeed(900);
  z_axis.setMaxSpeed(50);

  steppers.addStepper(x_axis);
  steppers.addStepper(y1_axis);
  steppers.addStepper(y2_axis);
  steppers.addStepper(z_axis); 
}
void loop() {
  char function;
  String receivedString;
  while(!S_Flag)
  {
    K = Serial_Read();
  }
  if(K == 'G')
  {
    Stp_To_Move[0] = Dist_To_Move[0] * (200 / 2); // Assuming 200 steps per revolution and 2 mm per revolution for X
    Stp_To_Move[1] = Dist_To_Move[1] * (200 / 8); // Assuming 200 steps per revolution and 8 mm per revolution for Y1
    Stp_To_Move[2] = Dist_To_Move[1] * (200 / 8); // Assuming 200 steps per revolution and 8 mm per revolution for Y2
    Stp_To_Move[3] = Dist_To_Move[2] * (200 / 8); // Assuming 200 steps per revolution and  mm per revolution for Z
    if(Stp_To_Move[0] == 0 && Stp_To_Move[1] == 0 && Stp_To_Move[2] == 0 && Stp_To_Move[3] == 0)
    {
      delay(1000);
      Serial.println("Ok");
    }
    else{ 
    Move_by_Distance(Stp_To_Move);
    Serial.println("Ok");
    }
  }
  Reset_All();
}
char Serial_Read() 
{
  char function;
  String receivedString;
  while(Serial.available())
  {
    S_Flag = 1;
    receivedString = Serial.readString().until;
    function = receivedString[0];
    if(function == 'G')
    {
      receivedString[0] = ' ';
      int X_pos = receivedString.indexOf('X');
      int Y_pos = receivedString.indexOf('Y');
      int Z_pos = receivedString.indexOf('Z');
      Dist_To_Move[0] = receivedString.substring(X_pos + 1, Y_pos).toInt();
      Dist_To_Move[1] = receivedString.substring(Y_pos + 1, Z_pos).toInt();
      Dist_To_Move[2] = receivedString.substring(Z_pos + 1).toInt();
      return function;
    }
    else if (function == 'C') 
    {
      // Calibrate logic here
      return function;
    }
    else if (function == 'S')
    {
      // Set home logic here
      return function;
    }
    break;
  }
}
void Move_by_Distance(long int Step[])
{
  steppers.moveTo(Step);
  steppers.runSpeedToPosition();
}

void Reset_All()
{
  S_Flag = 0;// reset serial Flag
  D_Flag = 0; // reset direction
  // Reset Dir array
  common_Step = 0; // reset commm set
  High_Step = -1;// reset highstep variable
  
  x_axis.setCurrentPosition(0);
  y1_axis.setCurrentPosition(0);
  y2_axis.setCurrentPosition(0);
  z_axis.setCurrentPosition(0);
}
