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

void setDir(bool dirc, bool mot)
{
  if (mot)
    digitalWrite(DIR_PIN_2, dirc);
  else
    digitalWrite(DIR_PIN_1, dirc);
}
