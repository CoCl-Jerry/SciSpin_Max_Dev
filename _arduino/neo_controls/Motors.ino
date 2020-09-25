void enableMotor(bool mot) {
  if (mot)
    digitalWrite(EN_PIN_2, LOW);
  else
    digitalWrite(EN_PIN_1, LOW);
}

void disableMotor(bool mot) {
  if (mot)
    digitalWrite(EN_PIN_2, HIGH);
  else
    digitalWrite(EN_PIN_1, HIGH);
}

void setDir(bool mot) {
  if (mot)
    digitalWrite(DIR_PIN_2, commands[2]);
  else
    digitalWrite(DIR_PIN_1, commands[2]);
}

void setMotor(bool mot) {
  if (mot) {
    Motor_2.microsteps(int(commands[2]));
    interval_2 = commands[3];
  }
  
  else {
    Motor_1.microsteps(int(commands[2]));
    interval_1 = commands[3];
  }
}
