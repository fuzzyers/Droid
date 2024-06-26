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

const int speaker = 21;

const int directionPin1 = 12;
const int pwmPin1 = 3;
const int brakePin1 = 9;

const int directionPin2 = 13;
const int pwmPin2 = 11;
const int brakePin2 = 8;

const int buttonPin =10;
int buttonState = 0;

int scriptStarted = 0;

Servo myServo;
Stepper myStepper = Stepper(stepsPerRevolution, motorPin1, motorPin3, motorPin2, motorPin4);

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

  pinMode(buttonPin, INPUT);
  pinMode(speaker, OUTPUT);

  initialize();

}

void loop() {
  if (Serial.available() > 0){
    char incomingByte = Serial.read();
    Serial.println(incomingByte);
    // Turns Head Left
    if (incomingByte == 'q'){
      moveServoTo(0, 1000);  
    } 
    // Turns Head Right
    if (incomingByte == 'e'){
      moveServoTo(180, 1000); 
    } 
    // Reset head to face forward
    if (incomingByte == 'r'){
      moveServoTo(90, 1000); 
    } 
    // Unlocks Stepper motor for grabbing an item after it has been seen or locks when its no longer seen.
    if (incomingByte == 'u'){
      stepperLock = false;
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
}


void closeHand(){
  unsigned long startTime = millis();
  myStepper.setSpeed(30);

  int steps = -stepsPerRevolution;  
  while (millis() - startTime < 2000) {
    myStepper.step(steps);
  }
}

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
  long distance = duration * 0.034 / 2; // Converts to cm

  return distance;
}


//Direction Pins will also be affected by polarisation
void controlMotor(bool direction1, int speed1, int duration, bool direction2, int speed2) {
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

void makeR2D2Noise() {
  int frequencies[] = {800, 600, 1000, 700, 1200, 500, 900, 1100, 1300};
  int durations[] = {100, 150, 80, 120, 100, 90, 110, 70, 130};

  for (int i = 0; i < 9; i++) {
    tone(speaker, frequencies[i], durations[i]);
    delay(durations[i] + 20); 
  }

  // Turn off the sound
  noTone(speaker);
}

void initialize(){
  
  moveServoTo(0, 1000);  
  moveServoTo(90, 1000);    
  moveServoTo(180, 1000);
  moveServoTo(90, 1000);
  makeR2D2Noise(); //Startup sound
  // controlMotor(false, 100, 1000, true, 70); // For testing motors are working on initialization
  //Run Script
  // while (true){
  //     long distance = readUltrasonicDistance(trigPin, echoPin);
  // Serial.print("Distance: ");
  // Serial.print(distance);
  // Serial.println(" cm");
  //   if (scriptStarted == 0){
  //     buttonState = digitalRead(buttonPin);
  //   }

  //   if (buttonState == HIGH) {
  //     Serial.println("RUN_SCRIPT");
  //     scriptStarted == 1;
  //     buttonState == LOW;
  //     break;
  //   }
  //   delay(100);
  // }
}
