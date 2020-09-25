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
      digitalWrite(IR_PIN, HIGH);
      delay(4000);
      digitalWrite(IR_PIN, LOW);
    }
  }

  if (commands[0] == 7)
  {
    void(* resetFunc) (void) = 0;
    resetFunc(); //call reset
  }
  digitalWrite(BUZZER_PIN, HIGH);
  delay(100);
  digitalWrite(BUZZER_PIN, LOW);

}
