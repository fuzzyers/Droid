#include <Servo.h>

// Create a Servo object
Servo myServo;

// Define the pin for the servo
int servoPin = 9;

void setup() {
  // Attach the servo to the pin
  myServo.attach(servoPin);
}

void loop() {
  // Move the servo to 0 degrees
  myServo.write(0);
  delay(2000); // Wait for 2 seconds

  // Move the servo to 90 degrees
  myServo.write(90);
  delay(2000); // Wait for 2 seconds

  // Move the servo to 180 degrees
  myServo.write(180);
  delay(2000); // Wait for 2 seconds
}
