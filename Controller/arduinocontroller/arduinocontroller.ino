#include <Servo.h>
#include <Stepper.h>

const int servoPin = 7;
const int value = 3;
const int stepsPerRevolution = 64;

const int motorPin1 = 8;
const int motorPin2 = 9;
const int motorPin3 = 10;
const int motorPin4 = 11;

const int trigPin = 20;
const int echoPin = 19;

// int directionPin1 = 12;
// int pwmPin1 = 3;
// int brakePin1 = 9;

// // uncomment if using channel B, and remove above definitions
// int directionPin2 = 13;
// int pwmPin2 = 11;
// int brakePin2 = 8;


Servo myServo;
Stepper myStepper = Stepper(stepsPerRevolution, motorPin1, motorPin3, motorPin2, motorPin4);

boolean stepperLock = true;

void setup() {
  myServo.attach(servoPin);

  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // pinMode(directionPin1, OUTPUT);
  // pinMode(pwmPin1, OUTPUT);
  // pinMode(brakePin1, OUTPUT);

  // pinMode(directionPin2, OUTPUT);
  // pinMode(pwmPin2, OUTPUT);
  // pinMode(brakePin2, OUTPUT);

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

void controlMotor(bool direction, int speed, int duration) {
  // Set the direction
  if (direction == false) {
    //digitalWrite(directionPin, LOW);
  } else {
    //digitalWrite(directionPin, HIGH);
  }

  //digitalWrite(brakePin, LOW);
  //analogWrite(pwmPin, speed);
  delay(duration);
  //digitalWrite(brakePin, HIGH);
  //analogWrite(pwmPin, 0);
  delay(200);
}

void initialize(){
  moveServoTo(0, 1000);  
  openHand();
}
