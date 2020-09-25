#include <TMC2208Stepper.h>
#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <avr/wdt.h>

#define DIR_PIN_1   3
#define STEP_PIN_1  4
#define EN_PIN_1    5

#define DIR_PIN_2   10
#define STEP_PIN_2  11
#define EN_PIN_2    12

#define LED_PIN 6
#define NUM_LEDS 86

#define BUZZER_PIN A8
#define IR_PIN A0
#define FAN_PIN 8

#define SLAVE_ADDRESS 0x08
#define COMMANDSIZE 10

TMC2208Stepper Frame_driver = TMC2208Stepper(&Serial1);
TMC2208Stepper Core_driver = TMC2208Stepper(&Serial2);
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRBW + NEO_KHZ800);

char data[50];
int commands[COMMANDSIZE];

int microStep_1 = 256;
int MotorSpeed_1 = 10;
int interval_1 = 6428;
int currentLimit_1 = 300;
boolean dir_1 = true;

int microStep_2 = 256;
int MotorSpeed_2 = 10;
int interval_2 = 6428;
int currentLimit_2 = 300;
boolean dir_2 = true;

unsigned long NextTime_1 = 0;
unsigned long NextTime_2 = 0;

void setup() {
  Serial.begin(9600);
  
  Serial1.begin(115200);
  Frame_driver.push();

  Serial2.begin(115200);
  Core_driver.push();

  pinMode(IR_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  pinMode(DIR_PIN_1, OUTPUT);
  pinMode(STEP_PIN_1, OUTPUT);
  pinMode(EN_PIN_1, OUTPUT);

  pinMode(DIR_PIN_2, OUTPUT);
  pinMode(STEP_PIN_2, OUTPUT);
  pinMode(EN_PIN_2, OUTPUT);

  strip.setBrightness(50);
  strip.begin();
  strip.show();

  Frame_driver.pdn_disable(true);     // Use PDN/UART pin for communication
  Frame_driver.I_scale_analog(false); // Use internal voltage reference
  Frame_driver.rms_current(currentLimit_1);      // Set driver current 500mA
  Frame_driver.toff(2);               // Enable driver in software
  Frame_driver.mstep_reg_select(true);
  Frame_driver.microsteps(microStep_1);
  Frame_driver.intpol(true);
  Frame_driver.dedge(true);

  Core_driver.pdn_disable(true);     // Use PDN/UART pin for communication
  Core_driver.I_scale_analog(false); // Use internal voltage reference
  Core_driver.rms_current(currentLimit_2);      // Set driver current 500mA
  Core_driver.toff(2);               // Enable driver in software
  Core_driver.mstep_reg_select(true);
  Core_driver.microsteps(microStep_2);
  Core_driver.intpol(true);
  Core_driver.dedge(true);

  digitalWrite(EN_PIN_1, LOW);   // Disable driver in hardware
  digitalWrite(EN_PIN_2, LOW);   // Disable driver in hardware

  uint32_t data = 0;
  Frame_driver.DRV_STATUS(&data);
  Core_driver.DRV_STATUS(&data);

  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);

  startup();
  analogWrite(FAN_PIN, 100);
}

void loop() {
  if (micros() < NextTime_1)
    NextTime_1 = micros();
  if (micros() < NextTime_2)
    NextTime_2 = micros();

  if (micros() - NextTime_1 > interval_1) {
    digitalWrite(STEP_PIN_1, !digitalRead(STEP_PIN_1));
    NextTime_1 = micros();         // reset for next pulse
  }

  if (micros() - NextTime_2 > interval_2) {
    digitalWrite(STEP_PIN_2, !digitalRead(STEP_PIN_2));
    NextTime_2 = micros();         // reset for next pulse
  }
}
