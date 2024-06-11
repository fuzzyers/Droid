int directionPin = 12;
int pwmPin = 3;
int brakePin = 9;

//uncomment if using channel B, and remove above definitions
int directionPin1 = 13;
int pwmPin1 = 11;
int brakePin1 = 8;

//boolean to switch direction
bool directionState;

void setup() {
  
//define pins
pinMode(directionPin, OUTPUT);
pinMode(pwmPin, OUTPUT);
pinMode(brakePin, OUTPUT);
pinMode(directionPin1, OUTPUT);
pinMode(pwmPin1, OUTPUT);
pinMode(brakePin1, OUTPUT);
}

void loop() {

//change direction every loop()
directionState = !directionState;

//write a low state to the direction pin (13)
if(directionState == false){
  digitalWrite(directionPin, LOW);
  digitalWrite(directionPin1, LOW);
}

//write a high state to the direction pin (13)
else{
  digitalWrite(directionPin, HIGH);
  digitalWrite(directionPin1, HIGH);
}

//release breaks
digitalWrite(brakePin, LOW);
digitalWrite(brakePin1, LOW);

//set work duty for the motor
analogWrite(pwmPin, 100);
analogWrite(pwmPin1, 100);

delay(2000);

//activate breaks
digitalWrite(brakePin, HIGH);
digitalWrite(brakePin1, HIGH);

//set work duty for the motor to 0 (off)
analogWrite(pwmPin, 0);
analogWrite(pwmPin1, 0);

delay(2000);
}