#include <RedBot.h>
#include <NewPing.h>
#define bhv_drive 0
#define bhv_turnl 1
#define bhv_turnr 2
#define bhv_reverse 3
#define bhv_obstacles 4
#define bhv_reverse_left 5
#define bhv_reverse_right 6
#define ECHO_PIN2 A1
#define TRIGGER_PIN A2
#define TRIGGER_PIN2 A0
#define ECHO_PIN A3
#define LEFT_BUMPER_PIN A4
#define RIGHT_BUMPER_PIN A5
#define LEFT_LIGHT_SENSOR_PIN A6
#define RIGHT_LIGHT_SENSOR_PIN A7
#define TURNING 80 // Turning Speed
#define SPEED 200  // Sets the nominal speed. Set to any number from 0 - 255.
#define MAX_DISTANCE 200 // Echo Sensors Max distance
#define LIGHT_THRESHOLD 250

//Objects
RedBotAccel accel;
RedBotMotors motors;
NewPing sonar1(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
NewPing sonar2(TRIGGER_PIN2, ECHO_PIN2, MAX_DISTANCE);

// Initalised Robot State
int robot_state = bhv_drive;
int light_sensor = LEFT_LIGHT_SENSOR_PIN; 
int light_sensorr = RIGHT_LIGHT_SENSOR_PIN; 
int Lbumper = LEFT_BUMPER_PIN;
int Rbumper = RIGHT_BUMPER_PIN;

void setup() {
 	Serial.begin(9600);
  pinMode(Lbumper, INPUT);
  pinMode(Rbumper, INPUT);
}

/* The loop will run through each test function to decide on the state and will then change 

*/
void loop() {
  robot_state = test_drive(robot_state);
  robot_state = test_turn(robot_state);
  robot_state = test_reverse(robot_state);
  robot_state = test_obstacle(robot_state);
  dothethings(robot_state);
 }

void drive() {
  motors.leftMotor(SPEED);
  motors.rightMotor(SPEED);
}

void turnl (){
    motors.leftMotor(SPEED + TURNING, 100);
    motors.rightMotor(SPEED - TURNING, 100);
}

void turnr (){
    motors.leftMotor(SPEED - TURNING, 100);
    motors.rightMotor(SPEED + TURNING, 100);
}

void reverse() {
  motors.leftMotor(-SPEED);
  motors.rightMotor(-SPEED);
}


int test_drive(int state){
  state = bhv_drive;
  return state;
}

int test_turn(int state){
  if ((analogRead(light_sensor) > LIGHT_THRESHOLD) && (analogRead(light_sensorr) > LIGHT_THRESHOLD)){
    state = bhv_drive;
  }
  else if (analogRead(light_sensor) > LIGHT_THRESHOLD) {
    state = bhv_turnr;
  }
  else if (analogRead(light_sensorr) > LIGHT_THRESHOLD){
    state = bhv_turnl;
  } 
  return state;
}

int test_reverse(int state){
  if (digitalRead(Lbumper) == HIGH){
    state = bhv_reverse_left;
  }
  if (digitalRead(Rbumper) == HIGH) {
    state = bhv_reverse_right;
  }
  return state;
}

void dothethings(int state) {
  switch (state) {
    case bhv_drive:
      drive();
    break;
    case bhv_turnl:
      turnl();
    break;
    case bhv_turnr:
      turnr();
    break;
    case bhv_reverse:
      reverse();
    break;
    case bhv_reverse_left:
      reverse();
      turnl();
    break;
    case bhv_reverse_right:
      reverse();
      turnr();
    break;
  }
}
