// Define pins
#define STEP_PIN  3 // Step on rising edge
#define EN_PIN    9  // LOW: Driver enabled. HIGH: Driver disabled
#define DIR_PIN   2
#define RX_PIN    5  // SoftwareSerial pins
#define TX_PIN    6

#define MOTORSTEPS 2820

//Slave Address for the Communication
#define SLAVE_ADDRESS 0x09        //frame
//#define SLAVE_ADDRESS 0x10          //core
#define COMMANDSIZE 5

//Import the library required
#include <Wire.h>
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

int speedMatrix[15][10] = { {826, 400, 261, 187, 150, 122, 101, 85, 75, 64},//1-10
  { 57, 52, 46, 43, 36, 85, 80, 76, 68, 65
  },//11-20
  { 61, 56, 54, 52, 116, 109, 104, 100, 96, 93
  },//21-30
  { 90, 86, 83, 80, 76, 74, 72, 70, 68, 65
  },//31-40
  { 63, 61, 60, 59, 56, 125, 122, 121, 119, 115
  },//41-50
  { 112, 110, 106, 105, 104, 102, 99, 97, 95, 93
  },//51-60
  { 91, 90, 88, 87, 85, 183, 181, 178, 176, 174
  },//61-70
  { 171, 167, 166, 164, 160, 159, 157, 154, 150, 149
  },//71-80
  { 148, 305, 302, 299, 296, 292, 288, 284, 280, 277
  },//81-90
  { 273, 269, 265, 268, 261, 258, 255, 252, 249, 246
  },//91-100
  { 244, 242, 240, 236, 234, 233, 230, 228, 227, 223
  },//101-110
  { 221, 220, 217, 215, 213, 211, 210, 209, 207, 204
  },//111-120
  { 417, 416, 414, 411, 408, 404, 402, 400, 394, 391
  },//121-130
  { 388, 384, 381, 378, 375, 374, 372, 369, 366, 364
  },//131-140
  { 360, 357, 353, 350, 348, 347, 344, 342, 340, 335
  } //141-150
};


//Code Initialization
void setup() {

  //  //debug
  //  Serial.begin(9600);
  //  //debug

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
  if (micros() - NextTime > interval) {
    digitalWrite(STEP_PIN, !digitalRead(STEP_PIN));
    NextTime = micros();         // reset for next pulse
  }
}

void getInterval() {
  if (MotorSpeed <= 15)
  {
    driver.microsteps(256);
  }

  else if (MotorSpeed <= 24)
  {
    driver.microsteps(128);
  }

  else if (MotorSpeed <= 45)
  {
    driver.microsteps(64);
  }

  else if (MotorSpeed <= 65)
  {
    driver.microsteps(32);
  }

  else if (MotorSpeed <= 81)
  {
    driver.microsteps(16);
  }

  else if (MotorSpeed <= 120)
  {
    driver.microsteps(8);
  }

  else
  {
    driver.microsteps(4);
  }

  interval = speedMatrix[MotorSpeed / 10][MotorSpeed % 10 - 1];
  NextTime = micros();

  //debug
  //interval = MotorSpeed;
  //    Serial.println(MotorSpeed/10);
  //    Serial.println(MotorSpeed%10);
  //Serial.println(interval);
  //debug




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
    void(* resetFunc) (void) = 0;
    resetFunc(); //call reset
  }
}
