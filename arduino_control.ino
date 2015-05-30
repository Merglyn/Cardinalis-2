/*
ECEN2830 position control
*/

// define pins
const int pinON = 6;
const int pinCC_Right = 8;
const int pinCW_Right = 9;
const int pinSpeed_Right = 7;
const int pinCW_Left = 10;
const int pinCC_Left = 11;
const int pinSpeed_Left = 12;

// define vars
volatile unsigned int enc_left = 0;
volatile unsigned int enc_right = 0;


// setup pins and initial values
void setup() {
  pinMode(pinON,INPUT);
  pinMode(pinCW_Left,OUTPUT);
  pinMode(pinCC_Left,OUTPUT);
  pinMode(pinSpeed_Left,OUTPUT);
  pinMode(pinCW_Right,OUTPUT);
  pinMode(pinCC_Right,OUTPUT);
  pinMode(pinSpeed_Right,OUTPUT);
  pinMode(13,OUTPUT);
  stop();
 
  Serial.begin(9600);
 
  attachInterrupt(1, count_Left, RISING);
  attachInterrupt(0, count_Right, RISING);
}

void loop() {
  stop();
  //do {} while (digitalRead(pinON) == LOW);
  delay(3000);
  forward(24, 200);
  right(180, 200);
  forward(24, 200);
  left(180, 200);
}

void stop() {
  digitalWrite(13,LOW);
  digitalWrite(pinCW_Left, LOW);
  digitalWrite(pinCC_Left, LOW);
  digitalWrite(pinSpeed_Left, LOW);
  digitalWrite(pinCW_Right, LOW);
  digitalWrite(pinCC_Right, LOW);
  digitalWrite(pinSpeed_Right, LOW);
}

void count_Left(){
  enc_left++;
}

void count_Right(){
  enc_right++;
}

void forward(unsigned int distance, int spd){
  Serial.print("Forward: ");
  go(true, false, distance*75/2, spd);
}

void backward(unsigned int distance, int spd){
  Serial.print("Backward: ");
  go(false, true, distance*75/2, spd);
}

void left(unsigned int distance, int spd){
  Serial.print("Left: ");
  go(false, false, distance*34/9, spd);
}

void right(unsigned int distance, int spd){
  Serial.print("Right: ");
  go(true, true, distance*34/9, spd);
}

void go(boolean LCC, boolean RCC, unsigned int distance, int spd){
  //make sure speed is less than or equal to 1023 so that we can compensate
  stop();
  enc_left = 0;
  enc_right = 0;

  set_LCC(LCC);
  set_RCC(RCC);
  
  analogWrite(pinSpeed_Right, spd);
  analogWrite(pinSpeed_Left, spd);
 
  do{compensate(spd);} while((enc_left < distance)&&(enc_right < distance));
  stop();
 
  Serial.print(" Left: ");
  Serial.print(enc_left);
  Serial.print(" Right: ");
  Serial.print(enc_right);
  Serial.print(" Diff: ");
  Serial.print(diff());
  Serial.println(' ');

  //reset encoders
  enc_left = 0;
  enc_right = 0;
  return;
}

void compensate(int spd){
  int comp_speed = spd + (diff())^2;
  if (comp_speed >= 255){
    comp_speed = 255;
  } 
  if (enc_left > enc_right){
    analogWrite(pinSpeed_Left, spd);
    analogWrite(pinSpeed_Right, comp_speed);
  }
  if (enc_right > enc_left){
    analogWrite(pinSpeed_Right, spd);
    analogWrite(pinSpeed_Left, comp_speed);
  }
  if (enc_right == enc_left){
    analogWrite(pinSpeed_Left, spd);
    analogWrite(pinSpeed_Right, spd);
  }
}

void set_LCC(boolean LCC){
  if (LCC){
    digitalWrite(pinCC_Left, HIGH);
  }
  else{
    digitalWrite(pinCW_Left, HIGH);
  }
}

void set_RCC(boolean RCC){
  if (RCC){
    digitalWrite(pinCC_Right, HIGH);
  }
  else{
    digitalWrite(pinCW_Right, HIGH);
  }
}

int diff(){
  if (enc_left >= enc_right){
    return (enc_left - enc_right);
  }
  else{
    return (enc_right - enc_left);
  }
}

