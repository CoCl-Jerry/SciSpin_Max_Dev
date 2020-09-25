//Import the library required
#include <Wire.h>
#include <Adafruit_NeoPixel.h>
#include <TMC2208Stepper.h>

//Slave Address for the Communication
#define BUZZER_PIN A8
#define IR_PIN A0

#define LED_PIN 6
#define FAN_PIN 8

#define NUM_LEDS 86
#define BRIGHTNESS 50
#define SLAVE_ADDRESS 0x08

#define COMMANDSIZE 7

//Frame Motor
#define DIR_PIN_1   3
#define STEP_PIN_1  4 // Step on rising edge
#define EN_PIN_1    5  // LOW: Driver enabled. HIGH: Driver disabled

//Core Motor
#define DIR_PIN_2   10
#define STEP_PIN_2  11 // Step on rising edge
#define EN_PIN_2    12  // LOW: Driver enabled. HIGH: Driver disabled

TMC2208Stepper Frame_driver = TMC2208Stepper(&Serial1);
TMC2208Stepper Core_driver = TMC2208Stepper(&Serial2);

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRBW + NEO_KHZ800);

char data[50];
int commands[COMMANDSIZE];

int microStep_1 = 256;
int MotorSpeed_1 = 10;
int interval_1 = 8000;
int currentLimit_1 = 500;
boolean dir_1 = true;

int microStep_2 = 256;
int MotorSpeed_2 = 10;
int interval_2 = 8000;
int currentLimit_2 = 500;
boolean dir_2 = true;

unsigned long NextTime_1 = 0;
unsigned long NextTime_2 = 0;

//Code Initialization
void setup() {
  pinMode(IR_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // initialize i2c as slave
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);

  strip.setBrightness(BRIGHTNESS);
  strip.begin();
  strip.show();

  Serial1.begin(115200);
  Frame_driver.push();
  Serial2.begin(115200);
  Core_driver.push();

  pinMode(DIR_PIN_1, OUTPUT);
  pinMode(STEP_PIN_1, OUTPUT);
  pinMode(EN_PIN_1, OUTPUT);

  pinMode(DIR_PIN_2, OUTPUT);
  pinMode(STEP_PIN_2, OUTPUT);
  pinMode(EN_PIN_2, OUTPUT);


  Frame_driver.pdn_disable(true);     // Use PDN/UART pin for communication
  Frame_driver.I_scale_analog(false); // Use internal voltage reference
  Frame_driver.rms_current(currentLimit_1);      // Set driver current 500mA
  Frame_driver.toff(2);               // Enable driver in software
  Frame_driver.mstep_reg_select(true);
  Frame_driver.microsteps(8);
  Frame_driver.intpol(true);
  Frame_driver.dedge(true);

  Core_driver.pdn_disable(true);     // Use PDN/UART pin for communication
  Core_driver.I_scale_analog(false); // Use internal voltage reference
  Core_driver.rms_current(currentLimit_2);      // Set driver current 500mA
  Core_driver.toff(2);               // Enable driver in software
  Core_driver.mstep_reg_select(true);
  Core_driver.microsteps();
  Core_driver.intpol(true);
  Core_driver.dedge(true);

  startup();
  colorWipe(strip.Color(0, 0, 0, 0), 1);
  analogWrite(FAN_PIN, 100);
}

void loop() {
  //  if (micros() < NextTime_1)
  //    NextTime_1 = micros();
  //  if (micros() < NextTime_2)
  //    NextTime_2 = micros();
  //
  //  if (micros() - NextTime_1 > interval_1) {
  //    digitalWrite(STEP_PIN_1, !digitalRead(STEP_PIN_1));
  //    NextTime_1 = micros();         // reset for next pulse
  //  }
  //
  //  if (micros() - NextTime_2 > interval_2) {
  //    digitalWrite(STEP_PIN_2, !digitalRead(STEP_PIN_2));
  //    NextTime_2 = micros();         // reset for next pulse
  //  }
  digitalWrite(STEP_PIN_1, !digitalRead(STEP_PIN_1));
  digitalWrite(STEP_PIN_2, !digitalRead(STEP_PIN_2));
  delayMicroseconds(4000);
}

// callback for received data
void receiveData(int byteCount) {
  int i = 0;
  if (Wire.read() == '^')
  {
    while (Wire.available()) {
      data[i] = Wire.read();
      i++;
    }
    data[i] = '\0';
    Serial.println(data);
    processCMD();
    exeCMD();
  }
}  // end while

void processCMD() {
  clearCMD();
  int current = 0;
  char *p = data;
  char *str;
  while ((str = strtok_r(p, "~", &p)) != NULL)
  {
    int temp;
    temp = atoi(str);
    commands[current] = temp;
    current++;
  }
}

void clearCMD() {
  for (int i = 0; i < COMMANDSIZE; i++)
  {
    commands[i] = 0;
  }
}

void printCMD() {
  for (int i = 0; i < COMMANDSIZE; i++)
  {
    Serial.println(commands[i]);
  }
}
