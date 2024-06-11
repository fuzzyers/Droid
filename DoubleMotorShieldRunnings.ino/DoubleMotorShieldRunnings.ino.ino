#include <Wire.h>

#define SLAVE_ADDRESS 0x04

int directionPin = 12;
int pwmPin = 3;
int brakePin = 9;

int directionPin1 = 13;
int pwmPin1 = 11;
int brakePin1 = 8;

bool directionState;

void setup() {
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent); // register event
  Serial.begin(9600);
  Serial.println("I2C Slave Initialized");

  // Define pins
  pinMode(directionPin, OUTPUT);
  pinMode(pwmPin, OUTPUT);
  pinMode(brakePin, OUTPUT);
  pinMode(directionPin1, OUTPUT);
  pinMode(pwmPin1, OUTPUT);
  pinMode(brakePin1, OUTPUT);
}

void loop() {
  // Change direction every loop()
  // directionState = !directionState;

  // moveMotor(directionState, 100);
  // delay(2000);

  // brakeMotor();
  // delay(2000);
  delay(100);
}

void moveMotor(bool direction, int speed) {
  // Write direction
  if (direction == false) {
    digitalWrite(directionPin, LOW);
    digitalWrite(directionPin1, LOW);
  } else {
    digitalWrite(directionPin, HIGH);
    digitalWrite(directionPin1, HIGH);
  }

  // Release brakes
  digitalWrite(brakePin, LOW);
  digitalWrite(brakePin1, LOW);

  // Set work duty for the motor
  analogWrite(pwmPin, speed);
  analogWrite(pwmPin1, speed);
}

void brakeMotor() {
  // Activate brakes
  digitalWrite(brakePin, HIGH);
  digitalWrite(brakePin1, HIGH);

  // Set work duty for the motor to 0 (off)
  analogWrite(pwmPin, 0);
  analogWrite(pwmPin1, 0);
}

void receiveEvent(int howMany) {
  if (Wire.available() >= 2) { // ensure there are at least 2 bytes
    char command = Wire.read();
    int value = Wire.read(); // read the second byte
    
    if (command == 'M') { // Move command
      bool direction = value & 1; // assuming direction is in the LSB
      int speed = value >> 1; // remaining bits represent speed
      moveMotor(direction, speed);
    } else if (command == 'B') { // Brake command
      brakeMotor();
    }
  }
}

void requestEvent() {
  Wire.write("Hello from Arduino"); // respond with message
}
