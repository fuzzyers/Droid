// #include <Servo.h>
// #include <Stepper.h>

// const int servoPin = 7;
// const int value = 3;
// const int stepsPerRevolution = 64;

// const int motorPin1 = 8;
// const int motorPin2 = 9;
// const int motorPin3 = 10;
// const int motorPin4 = 11;

// const int trigPin = 12;
// const int echoPin = 13;


// Servo myServo;
// Stepper myStepper = Stepper(stepsPerRevolution, motorPin1, motorPin3, motorPin2, motorPin4);
// void setup() {
//   myServo.attach(servoPin);

//   Serial.begin(9600);
//   pinMode(trigPin, OUTPUT);
//   pinMode(echoPin, INPUT);

// }

// void loop() {
//   if (value == 1){
//     moveServoTo(0, 1000);  
//     moveServoTo(90, 1000);  
//     moveServoTo(180, 1000); 
//     moveServoTo(90, 1000);  
//   } 
//   else if (value == 2){
//     myStepper.setSpeed(30);
// 	  myStepper.step(-stepsPerRevolution);
// 	  delay(1000);
//     Serial.println("Stepper: Stepping");
//   } else if (value == 3) {
//     long distance = readUltrasonicDistance(trigPin, echoPin);
//     Serial.print("Distance: ");
//     Serial.print(distance);
//     Serial.println(" cm");
//   }

//   delay(1000);  
// }

// void moveServoTo(int angle, int delayTime) {
//   myServo.write(angle);   
//   delay(delayTime);       
// }

// long readUltrasonicDistance(int trigPin, int echoPin) {
//   // Send a 10us pulse to trigger the sensor
//   digitalWrite(trigPin, LOW);
//   delayMicroseconds(2);
//   digitalWrite(trigPin, HIGH);
//   delayMicroseconds(10);
//   digitalWrite(trigPin, LOW);

//   // Read the echo pin and calculate the distance
//   long duration = pulseIn(echoPin, HIGH);
//   long distance = duration * 0.034 / 2; // Convert to cm

//   return distance;
// }

#define D0 -1
#define D1 262
#define D2 293
#define D3 329
#define D4 349
#define D5 392
#define D6 440
#define D7 494
#define M1 523
#define M2 586
#define M3 658
#define M4 697
#define M5 783
#define M6 879
#define M7 987
#define H1 1045
#define H2 1171
#define H3 1316
#define H4 1393
#define H5 1563
#define H6 1755
#define H7 1971
//list out all the frequencies of all the D tune
#define WHOLE 1
#define HALF 0.5
#define QUARTER 0.25
#define EIGHTH 0.25
#define SIXTEENTH 0.625
//list out all the beats
int tune[]=        //list out the tune according to the musical notation
{
  M3,M3,M4,M5,
  M5,M4,M3,M2,
  M1,M1,M2,M3,
  M3,M2,M2,
  M3,M3,M4,M5,
  M5,M4,M3,M2,
  M1,M1,M2,M3,
  M2,M1,M1,
  M2,M2,M3,M1,
  M2,M3,M4,M3,M1,
  M2,M3,M4,M3,M2,
  M1,M2,D5,D0,
  M3,M3,M4,M5,
  M5,M4,M3,M4,M2,
  M1,M1,M2,M3,
  M2,M1,M1
};
float durt[]=       // list out the beats according to the musical notation
{
  1,1,1,1,
  1,1,1,1,
  1,1,1,1,
  1+0.5,0.5,1+1,
  1,1,1,1,
  1,1,1,1,
  1,1,1,1,
  1+0.5,0.5,1+1,
  1,1,1,1,
  1,0.5,0.5,1,1,
  1,0.5,0.5,1,1,
  1,1,1,1,
  1,1,1,1,
  1,1,1,0.5,0.5,
  1,1,1,1,
  1+0.5,0.5,1+1,
};
int length;
int tonepin=1;   // use pin 3
void setup()
{
  pinMode(tonepin,OUTPUT);
  length=sizeof(tune)/sizeof(tune[0]);   // calculate the length
}
void loop()
{
  // for(int x=0;x<length;x++)
  // {
  //   tone(tonepin,tune[x]);
  //   delay(500*durt[x]);   //adjust the delay time according to tone, you can change the index 500 for the music. 
  //   noTone(tonepin);
  // }
  delay(2000);
}