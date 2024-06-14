#include <AccelStepper.h>
#include <MultiStepper.h>

// Define Pin for motor
const int stepPinX = 2;
const int dirPinX = 3;

const int stepPinY1 = 4;
const int dirPinY1 = 5;
const int stepPinY2 = 6;
const int dirPinY2 = 7;

const int stepPinZ = 8;
const int dirPinZ = 9;


// Define Pin for Limit Switch
const int limitSwitchX = 10;
const int limitSwitchY1 = 11;
const int limitSwitchY2 = 12;

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


float Dist_To_Move[3];
long Stp_To_Move[4];
unsigned int M_Direction[3] = {0, 0, 0}; // moving direction

//---------Declaration Flag-------//
//-------------------------------//

int S_Flag = 0; // Serial flag
int D_Flag = 0;
int M_Flag = 0; // moving flag
String inData;

void setup() {
  Serial.begin(115200);
  pinMode(17, OUTPUT);
  pinMode(limitSwitchX, INPUT_PULLUP);
  digitalWrite(17, 0);

  x_axis.setCurrentPosition(0);
  y1_axis.setCurrentPosition(0);
  y2_axis.setCurrentPosition(0);
  z_axis.setCurrentPosition(0);
  
  x_axis.setMaxSpeed(900);
  y1_axis.setMaxSpeed(900);
  y2_axis.setMaxSpeed(900);
  z_axis.setMaxSpeed(900);

  x_axis.setAcceleration(200);

  steppers.addStepper(x_axis);
  steppers.addStepper(y1_axis);
  steppers.addStepper(y2_axis);
  steppers.addStepper(z_axis); 
}
void loop() {
  if (Serial.available() > 0) {
    char received = Serial.read();
    inData += received;
    // Process message when new line character is received
    if (received == '\n') {
      char function = inData[0];
      inData[0] = ' ';
      if (function == 'G') {
        int X_pos = inData.indexOf('X');
        int Y_pos = inData.indexOf('Y');
        int Z_pos = inData.indexOf('Z');
        Stp_To_Move[0] = inData.substring(X_pos + 1, Y_pos).toInt();
        Stp_To_Move[1] = inData.substring(Y_pos + 1, Z_pos).toInt();
        Stp_To_Move[2] = inData.substring(Y_pos + 1, Z_pos).toInt();
        Stp_To_Move[3] = inData.substring(Z_pos + 1).toInt();
        
        if (Stp_To_Move[0] == 0 && Stp_To_Move[1] == 0 && Stp_To_Move[2] == 0 && Stp_To_Move[3] == 0) {
          Serial.println("Ok");
        } else { 
          Move_by_Distance(Stp_To_Move);
          Serial.println("Ok");
        }
      } else if (function == 'C') {
        switch (inData[1]) { 
          case 'X':
            CalibrateX();
            break;
          case 'Y':
            CalibrateY();
            break;
          case 'A':
            CalibrateAll();
            break;
          default:
            delay(1000);
            Serial.println("No");
            break;
        }
      }
      inData = ""; // Clear the input data after processing
      Reset_All();
      delayMicroseconds(1);
    }
  }
}
void Move_by_Distance(long int Step[])
{
  steppers.moveTo(Step);
  steppers.runSpeedToPosition();
}
void CalibrateX() {
  Serial.println("Calibrating X");

  digitalWrite(dirPinX, HIGH); 

  while (digitalRead(limitSwitchX) == HIGH) {
    digitalWrite(stepPinX, HIGH);
    delayMicroseconds(400);
    digitalWrite(stepPinX, LOW);
    delayMicroseconds(400);
  }

  // Double check
  digitalWrite(dirPinX, LOW); 
  for (int x = 0; x < 2000; x++) { 
    digitalWrite(stepPinX, HIGH);
    delayMicroseconds(400);
    digitalWrite(stepPinX, LOW);
    delayMicroseconds(400);
  }
  
  delay(100);
  digitalWrite(dirPinX, HIGH); 
  while (digitalRead(limitSwitchX) == HIGH) {
    digitalWrite(stepPinX, HIGH);
    delayMicroseconds(400);
    digitalWrite(stepPinX, LOW);
    delayMicroseconds(400);
  }

  Serial.println("X axis calibrated.");

  long steps_to_move_x = -205 * (400 / 8); 
  digitalWrite(dirPinX, LOW); 
  
  for (long x = 0; x < abs(steps_to_move_x); x++) {
    digitalWrite(stepPinX, HIGH);
    delayMicroseconds(400);
    digitalWrite(stepPinX, LOW);
    delayMicroseconds(400);
  }

  Serial.println("Done X");
}

void CalibrateY() {
  Serial.println("Calibrating Y1 and Y2");

  digitalWrite(dirPinY1, LOW);
  digitalWrite(dirPinY2, LOW);

  while (digitalRead(limitSwitchY1) == HIGH || digitalRead(limitSwitchY2) == HIGH) {
    if (digitalRead(limitSwitchY1) == HIGH) {
      digitalWrite(stepPinY1, HIGH);
      delayMicroseconds(300);
      digitalWrite(stepPinY1, LOW);
      delayMicroseconds(300);
    }

    if (digitalRead(limitSwitchY2) == HIGH) {
      digitalWrite(stepPinY2, HIGH);
      delayMicroseconds(300);
      digitalWrite(stepPinY2, LOW);
      delayMicroseconds(300);
    }
  }

  // Double check
  digitalWrite(dirPinY1, HIGH);
  digitalWrite(dirPinY2, HIGH);

  for (int x = 0; x < 2000; x++) {
    digitalWrite(stepPinY1, HIGH);
    digitalWrite(stepPinY2, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPinY1, LOW);
    digitalWrite(stepPinY2, LOW);
    delayMicroseconds(500);
  }

  delay(100);

  digitalWrite(dirPinY1, LOW);
  digitalWrite(dirPinY2, LOW);

  while (digitalRead(limitSwitchY1) == HIGH || digitalRead(limitSwitchY2) == HIGH) {
    if (digitalRead(limitSwitchY1) == HIGH) {
      digitalWrite(stepPinY1, HIGH);
      delayMicroseconds(500);
      digitalWrite(stepPinY1, LOW);
      delayMicroseconds(500);
    }

    if (digitalRead(limitSwitchY2) == HIGH) {
      digitalWrite(stepPinY2, HIGH);
      delayMicroseconds(500);
      digitalWrite(stepPinY2, LOW);
      delayMicroseconds(500);
    }
  }

  Serial.println("Y1 and Y2 axes calibrated.");

  long steps_to_move_y = 190 * (400 / 8);

  digitalWrite(dirPinY1, HIGH);
  digitalWrite(dirPinY2, HIGH);

  for (long x = 0; x < abs(steps_to_move_y); x++) {
    digitalWrite(stepPinY1, HIGH);
    digitalWrite(stepPinY2, HIGH);
    delayMicroseconds(500);
    digitalWrite(stepPinY1, LOW);
    digitalWrite(stepPinY2, LOW);
    delayMicroseconds(500);
  }

  Serial.println("Done Y1 and Y2");
}

void CalibrateAll() {
  Serial.println("Starting calibration for all axes");

  CalibrateX();
  CalibrateY();


  Serial.println("Done All");
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
