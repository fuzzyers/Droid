#include <Servo.h>
#include <Stepper.h>

const int servoPin = 7;
const int stepsPerRevolution = 64;

const int motorPin1 = 2;
const int motorPin2 = 4;
const int motorPin3 = 5;
const int motorPin4 = 6;

const int trigPin = 20;
const int echoPin = 19;

int directionPin1 = 12;
int pwmPin1 = 3;
int brakePin1 = 9;

// uncomment if using channel B, and remove above definitions
int directionPin2 = 13;
int pwmPin2 = 11;
int brakePin2 = 8;


Servo myServo;
Stepper myStepper = Stepper(stepsPerRevolution, motorPin1, motorPin2, motorPin3, motorPin4);

boolean stepperLock = true;

void setup() {
  myServo.attach(servoPin);

  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(directionPin1, OUTPUT);
  pinMode(pwmPin1, OUTPUT);
  pinMode(brakePin1, OUTPUT);

  pinMode(directionPin2, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(brakePin2, OUTPUT);

  initialize();

}

void loop() {
  if (Serial.available() > 0){
    char incomingByte = Serial.read();

    // Turns Head Left
    if (incomingByte == 'q'){
      moveServoTo(90, 1000);  
    } 
    // Turns Head Right
    if (incomingByte == 'e'){
      moveServoTo(270, 1000); 
    } 
    // Reset head to face forward
    if (incomingByte == 'r'){
      moveServoTo(0, 1000); 
    } 
    // Unlocks Stepper motor for grabbing an item after it has been seen or locks when its no longer seen.
    if (incomingByte == 'u'){
      stepperLock = !stepperLock;
    }
    
    if (incomingByte == 'o'){
      openHand();
    }

    //Move Forwards
    if (incomingByte == 'w'){
      controlMotor(false, 100, 1000, true, 100);
    }

    //Strafe Left
    if (incomingByte == 'a'){
      controlMotor(false, 100, 1000, true, 70);
    }

    //Strafe Right
    if (incomingByte == 'd'){
      controlMotor(false, 70, 1000, true, 100);
    }

    if (incomingByte == 'z'){
      controlMotor(false, 100, 1000, false, 100);
    }

    if (incomingByte == 'z'){
      controlMotor(false, 100, 1000, false, 100);
    }
  }

  if (stepperLock == false){
    long distance = readUltrasonicDistance(trigPin, echoPin);
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");
    
    if (distance < 4){
      closeHand();
    }
  }
  delay(1000);  
}


void closeHand(){
  unsigned long startTime = millis();
  myStepper.setSpeed(30);

  int steps = stepsPerRevolution;  
  while (millis() - startTime < 2000) {
    myStepper.step(-steps);
  }}

void openHand(){
  unsigned long startTime = millis();
  myStepper.setSpeed(30);

  int steps = stepsPerRevolution;  
  while (millis() - startTime < 2000) {
    myStepper.step(steps);
  }
}

void moveServoTo(int angle, int delayTime) {
  myServo.write(angle);   
  delay(delayTime);       
}

long readUltrasonicDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  long distance = duration * 0.034 / 2; // Convert to cm

  return distance;
}


//Direction Pins will also be affected by polarisation
void controlMotor(bool direction1, int speed1, int duration, bool direction2, int speed2) {
  // Set the direction
  if (direction1 == false) {
    digitalWrite(directionPin1, LOW);
  } else {
    digitalWrite(directionPin1, HIGH);
  }
  if (direction2 == false) {
    digitalWrite(directionPin2, LOW);
  } else {
    digitalWrite(directionPin2, HIGH);
  }

  digitalWrite(brakePin1, LOW);
  digitalWrite(brakePin2, LOW);
  analogWrite(pwmPin1, speed1);
  analogWrite(pwmPin2, speed2);
  delay(duration);
  digitalWrite(brakePin1, HIGH);
  digitalWrite(brakePin2, HIGH);
  analogWrite(pwmPin1, 0);
  analogWrite(pwmPin2, 0);
  delay(200);
}

void initialize(){
  moveServoTo(0, 1000);  
  // openHand();
  controlMotor(false, 100, 1000, true, 70);
  closeHand();
}
