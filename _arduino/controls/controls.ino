//Import the library required
#include <Wire.h>
#include <Adafruit_NeoPixel.h>

//Slave Address for the Communication
#define LED_PIN 5
#define FAN_PIN 9
#define IR_PIN 8
#define NUM_LEDS 83
#define BRIGHTNESS 50
#define QUARTER NUM_LEDS/4
#define SLAVE_ADDRESS 0x08
#define COMMANDSIZE 7

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRBW + NEO_KHZ800);

char data[50];
int commands[COMMANDSIZE];

//Code Initialization
void setup() {
  // initialize i2c as slave
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  //  Wire.onRequest(sendData);

  strip.setBrightness(BRIGHTNESS);
  strip.begin();
  strip.show();

  //  colorWipe(strip.Color(100, 50, 50, 50), 0);
  //  colorWipe(strip.Color(50, 100, 50, 50), 0);
  //  colorWipe(strip.Color(50, 50, 100, 50), 0);
  //  colorWipe(strip.Color(50, 50, 50, 100), 0);

  startup();
  colorWipe(strip.Color(0, 0, 0, 0), 1);

  pinMode(IR_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  digitalWrite(FAN_PIN, HIGH);
  delay(500);
  digitalWrite(FAN_PIN, LOW);


}

void loop() {

  disco(10);

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

void exeCMD() {
  if (commands[0] == 1)
  {
    stripUpdate();
    strip.show();
  }

  if (commands[0] == 2)
  {
    brightnessUpdate();
  }

  if (commands[0] == 3)
  {

    digitalWrite(IR_PIN, !digitalRead(IR_PIN));
  }

  if (commands[0] == 4)
  {
    stripUpdate();
  }

  if (commands[0] == 5)
  {
    stripShow();
  }

  if (commands[0] == 6)
  {
    if (!digitalRead(IR_PIN))
    {
      digitalWrite(IR_PIN, !digitalRead(IR_PIN));
      delay(4000);
      digitalWrite(IR_PIN, !digitalRead(IR_PIN));
    }
  }

  if (commands[0] == 7)
  {
    void(* resetFunc) (void) = 0;
    resetFunc(); //call reset
  }

  if (commands[0] == 8)
  {
    digitalWrite(FAN_PIN, HIGH);
  }

  if (commands[0] == 9)
  {
    digitalWrite(FAN_PIN, LOW);
  }
}

void colorWipe(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

void stripUpdate() {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    if (i >= commands[1] && i < commands[2]) {
      strip.setPixelColor(i, int(commands[3] * 2.55), int(commands[4] * 2.55), int(commands[5] * 2.55), int(commands[6] * 2.55));
    }
  }

}

void stripShow() {
  strip.show();
}

void brightnessUpdate() {
  strip.setBrightness(int(commands[1] * 2.55));
  strip.show();
}

// Rainbow cycle along whole strip. Pass delay time (in ms) between frames.
void rainbow(int wait) {
  // Hue of first pixel runs 5 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
  // means we'll make 5*65536/256 = 1280 passes through this outer loop:
  for (long firstPixelHue = 0; firstPixelHue < 65536; firstPixelHue += 256) {
    for (int i = 0; i < strip.numPixels() && commands[0] == 6; i++) { // For each pixel in strip...
      // Offset pixel hue by an amount to make one full revolution of the
      // color wheel (range of 65536) along the length of the strip
      // (strip.numPixels() steps):
      int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
      // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
      // optionally add saturation and value (brightness) (each 0 to 255).
      // Here we're using just the single-argument hue variant. The result
      // is passed through strip.gamma32() to provide 'truer' colors
      // before assigning to each pixel:
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
    }
    strip.show(); // Update strip with new contents
    delay(wait);  // Pause for a moment
  }
}

void startup() {
  // Hue of first pixel runs 5 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
  // means we'll make 5*65536/256 = 1280 passes through this outer loop:
  for (long firstPixelHue = 0; firstPixelHue < 65536; firstPixelHue += 256) {
    for (int i = 0; i < strip.numPixels(); i++) { // For each pixel in strip...
      // Offset pixel hue by an amount to make one full revolution of the
      // color wheel (range of 65536) along the length of the strip
      // (strip.numPixels() steps):
      int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
      // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
      // optionally add saturation and value (brightness) (each 0 to 255).
      // Here we're using just the single-argument hue variant. The result
      // is passed through strip.gamma32() to provide 'truer' colors
      // before assigning to each pixel:
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
    }
    strip.show(); // Update strip with new contents
  }
}

void disco(int wait) {

  int firstPixelHue = 0;     // First pixel starts at red (hue 0)
  for (int a = 0; a < 30 && commands[0] == 7; a++) { // Repeat 30 times...
    for (int b = 0; b < 3 && commands[0] == 7; b++) { //  'b' counts from 0 to 2...
      strip.clear();         //   Set all pixels in RAM to 0 (off)
      // 'c' counts up from 'b' to end of strip in increments of 3...
      for (int c = b; c < strip.numPixels() && commands[0] == 7; c += 3) {
        // hue of pixel 'c' is offset by an amount to make one full
        // revolution of the color wheel (range 65536) along the length
        // of the strip (strip.numPixels() steps):
        int      hue   = firstPixelHue + c * 65536L / strip.numPixels();
        uint32_t color = strip.gamma32(strip.ColorHSV(hue)); // hue -> RGB
        strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
      }
      strip.show();                // Update strip with new contents
      delay(wait);                 // Pause for a moment
      firstPixelHue += 65536 / 90; // One cycle of color wheel over 90 frames
    }
  }

}
