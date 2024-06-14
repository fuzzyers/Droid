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
  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for the serial port to connect
  }
  pinMode(LED_BUILTIN, OUTPUT); // Set the built-in LED pin as output


  // Define pins
  pinMode(directionPin, OUTPUT);
  pinMode(pwmPin, OUTPUT);
  pinMode(brakePin, OUTPUT);
  pinMode(directionPin1, OUTPUT);
  pinMode(pwmPin1, OUTPUT);
  pinMode(brakePin1, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char received = Serial.read(); // Read the incoming byte
    Serial.print("Received: ");
    Serial.println(received); // Print the received byte

    controller(received);
  }
  
  delay(100);
}

void controller(char received) {
if (received == 'F') {
      moveMotorForward(100);
      delay(2000);
      stopMotor();
      delay(2000);
    }
    if (received == 'L') {
      turnMotorLeft(100);
      delay(2000);
      stopMotor();
      delay(2000);
    }
    if (received == 'R') {
      turnMotorRight(100);
      delay(2000);
      stopMotor();
      delay(2000);
    }
    if (received == 'B') {
      moveMotorReverse(100);
      delay(2000);
      stopMotor();
      delay(2000);
    }

}

void moveMotor(int speed) {
  // Write direction

  digitalWrite(directionPin, HIGH);
  digitalWrite(directionPin1, HIGH);
  

  // Release brakes
  digitalWrite(brakePin, LOW);
  digitalWrite(brakePin1, LOW);

  // Set work duty for the motor
  analogWrite(pwmPin, speed);
  analogWrite(pwmPin1, speed);
}

void moveMotorReverse(int speed) {
  digitalWrite(directionPin, LOW);
  digitalWrite(directionPin1, LOW);
  digitalWrite(brakePin, LOW);
  digitalWrite(brakePin1, LOW);
  analogWrite(pwmPin, speed);
  analogWrite(pwmPin1, speed);
}

// Function to turn motor left
void turnMotorLeft(int speed) {
  digitalWrite(directionPin, LOW);  // Left motor reverse
  digitalWrite(directionPin1, HIGH); // Right motor forward
  digitalWrite(brakePin, LOW);
  digitalWrite(brakePin1, LOW);
  analogWrite(pwmPin, speed);
  analogWrite(pwmPin1, speed);
}

// Function to turn motor right
void turnMotorRight(int speed) {
  digitalWrite(directionPin, HIGH);  // Left motor forward
  digitalWrite(directionPin1, LOW);  // Right motor reverse
  digitalWrite(brakePin, LOW);
  digitalWrite(brakePin1, LOW);
  analogWrite(pwmPin, speed);
  analogWrite(pwmPin1, speed);
}

void strafeRight(int speed) {
  digitalWrite(directionPin, HIGH);  // Left motor forward
  digitalWrite(directionPin1, HIGH);  // Right motor reverse
  digitalWrite(brakePin, LOW);
  digitalWrite(brakePin1, LOW);
  analogWrite(pwmPin, speed);
  analogWrite(pwmPin1, speed/2);
}

void strafeLeft(int speed) {
  digitalWrite(directionPin, HIGH);  // Left motor forward
  digitalWrite(directionPin1, HIGH);  // Right motor reverse
  digitalWrite(brakePin, LOW);
  digitalWrite(brakePin1, LOW);
  analogWrite(pwmPin, speed);
  analogWrite(pwmPin1, speed/2);
}

// Function to stop the motor
void stopMotor() {
  digitalWrite(brakePin, HIGH);
  digitalWrite(brakePin1, HIGH);
  analogWrite(pwmPin, 0);
  analogWrite(pwmPin1, 0);
}


void brakeMotor() {
  // Activate brakes
  digitalWrite(brakePin, HIGH);
  digitalWrite(brakePin1, HIGH);

  // Set work duty for the motor to 0 (off)
  analogWrite(pwmPin, 0);
  analogWrite(pwmPin1, 0);
}

