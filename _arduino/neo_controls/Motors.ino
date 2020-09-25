void enableMotor1() {
  digitalWrite(EN_PIN_1, LOW); 
}

void enableMotor2() {
  digitalWrite(EN_PIN_2, LOW); 
}

void disableMotor1() {
  digitalWrite(EN_PIN_1, HIGH); 
}

void disableMotor2() {
  digitalWrite(EN_PIN_2, HIGH); 
}
