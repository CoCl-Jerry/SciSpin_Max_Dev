// Define pins
#define STEP_PIN  3 // Step on rising edge
#define EN_PIN    9  // LOW: Driver enabled. HIGH: Driver disabled
#define DIR_PIN   2
#define RX_PIN    5  // SoftwareSerial pins
#define TX_PIN    6

#define MOTORSTEPS 2820

//Slave Address for the Communication
//#define SLAVE_ADDRESS 0x09
#define SLAVE_ADDRESS 0x10
#define COMMANDSIZE 5

//Import the library required
#include <Wire.h>
#include <avr/wdt.h> 
#include <TMC2208Stepper.h>

TMC2208Stepper driver = TMC2208Stepper(RX_PIN, TX_PIN);  // Create driver and use

char data[50];
int commands[COMMANDSIZE];

int microStep = 256;
int MotorSpeed = 10;
int interval = 0;
int currentLimit = 200;

boolean dir = true;
boolean sysRunning = false;

unsigned long NextTime = 0;


//Code Initialization
void setup() {


  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  driver.beginSerial(115200);
  driver.push();                // Reset registers

  // Prepare pins
  pinMode(EN_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);



  driver.pdn_disable(true);     // Use PDN/UART pin for communication
  driver.I_scale_analog(false); // Use internal voltage reference
  driver.rms_current(currentLimit);      // Set driver current 500mA
  driver.toff(2);               // Enable driver in software
  driver.mstep_reg_select(true);
  driver.microsteps(microStep);
  driver.intpol(true);
  driver.dedge(true);

  digitalWrite(EN_PIN, HIGH);   // Disable driver in hardware

  uint32_t data = 0;
  driver.DRV_STATUS(&data);
  getInterval();
}

void loop() {
  if (micros() > NextTime) {
    digitalWrite(STEP_PIN, !digitalRead(STEP_PIN));
    NextTime += interval;         // reset for next pulse
  }
}

void getInterval() {
  if (MotorSpeed <= 20)
  {
    driver.microsteps(256);
    microStep = 256;
  }

  else if (MotorSpeed <= 45)
  {
    driver.microsteps(128);
    microStep = 128;
  }

  else if (MotorSpeed <= 60)
  {
    driver.microsteps(64);
    microStep = 64;
  }

  else if (MotorSpeed <= 80)
  {
    driver.microsteps(32);
    microStep = 32;
  }

  else if (MotorSpeed <= 100)
  {
    driver.microsteps(16);
    microStep = 16;
  }

  else if (MotorSpeed <= 120)
  {
    driver.microsteps(8);
    microStep = 8;
  }

  else if (MotorSpeed <= 140)
  {
    driver.microsteps(4);
    microStep = 4;
  }

  else
  {
    driver.microsteps(2);
    microStep = 2;
  }




  interval = (600000000 / ((long)MOTORSTEPS * (long)microStep * MotorSpeed));

  NextTime = micros();

}

// Writes a high or low value to the direction pin to specify
// what direction to turn the motor.
void setDirection(bool dir)
{
  // The NXT/STEP pin must not change for at least 0.5
  // microseconds before and after changing the DIR pin.
  delayMicroseconds(1);
  digitalWrite(DIR_PIN, dir);
  delayMicroseconds(1);
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

void exeCMD() {
  if (commands[0] == 1)
  {
    if (!sysRunning)
    {
      digitalWrite(EN_PIN, LOW);
      setDirection(dir);
    }
    else
    {
      digitalWrite(EN_PIN, HIGH);
    }

    sysRunning = !sysRunning;
  }

  if (commands[0] == 2)
  {
    MotorSpeed = commands[1];
    getInterval();
  }

  if (commands[0] == 3)
  {
    setDirection(commands[1]);
  }
  if (commands[0] == 4)
  {
    driver.rms_current(currentLimit + commands[1]);
    interval = commands[3];
    driver.microsteps(commands[4]);
  }
  if (commands[0] == 5)
  {
    wdt_disable();
    wdt_enable(WDTO_15MS);
    while (1) {}
  }
}
