void motorStatus() {
  digitalWrite(EN_PIN_1, commands[2]);
  digitalWrite(EN_PIN_2, commands[3]);
}

void dirUpdate() {
  digitalWrite(DIR_PIN_1, commands[2]);
  digitalWrite(DIR_PIN_2, commands[3]);
}

void setDir(bool mot) {
  if (mot)
    digitalWrite(DIR_PIN_2, commands[2]);
  else
    digitalWrite(DIR_PIN_1, commands[2]);
}

void setMotor(bool mot) {
  if (mot) {
    microstep_2 = commands[2];
    interval_2 = commands[3];
    ms_change_2 = true;
  }


  else {
    microstep_1 = commands[2];
    interval_1 = commands[3];
    ms_change_1 = true;
  }
}
