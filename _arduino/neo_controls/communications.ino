void receiveData(int byteCount) {
  int i = 0;
  if (Wire.read() == '^')
  {
    digitalWrite(BUZZER_PIN, HIGH);
    while (Wire.available()) {
      data[i] = Wire.read();
      i++;
    }
    data[i] = '\0';
    Serial.println(data);
    processCMD();
    exeCMD();
  }
  digitalWrite(BUZZER_PIN, LOW);
}

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
