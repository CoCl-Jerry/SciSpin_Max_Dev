void stripUpdate() {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    if (i >= commands[2] && i < commands[3]) {
      strip.setPixelColor(i, int(commands[4] * 2.55), int(commands[5] * 2.55), int(commands[6] * 2.55), int(commands[7] * 2.55));
    }
  }
  strip.setBrightness(int(commands[8] * 1.7));

}

void brightnessUpdate() {
  strip.setBrightness(int(commands[2] * 1.7));
}

void stripClear() {
  strip.clear();
}

void stripShow() {
  strip.show();
}
