void exeCMD() {
  switch (commands[0]) {
    case 0:
      wdt_disable();
      wdt_enable(WDTO_15MS);
      while (1) {}
      break;

    case 1:
      switch (commands[1]) {
        case 0:
          motorStatus();
          break;
        case 1:
          dirUpdate();
          break;
        case 2:
          setMotor();
          break;

        default:
          break;
      }
      break;

    case 3:
      switch (commands[1]) {
        case 0:
          stripClear();
          break;
        case 1:
          stripUpdate();
          stripShow();
          break;
        case 2:
          stripUpdate();
          break;
        case 3:
          stripShow();
          break;
        case 4:
          brightnessUpdate();
          break;
        default:
          break;
      }
      break;

    case 4:
      switch (commands[1]) {
        case 0:
          infraOff();
          break;
        case 1:
          infraOn();
          break;
        default:
          break;
      }
      break;

    default:
      // statements
      break;
  }
}
