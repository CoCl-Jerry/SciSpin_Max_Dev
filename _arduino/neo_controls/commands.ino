void exeCMD() {
  printCMD();
  switch (commands[0]) {
    case 0:
      wdt_disable();
      wdt_enable(WDTO_15MS);
      while (1) {}
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
          // statements
          break;
      }
      break;

    default:
      // statements
      break;
  }
}
