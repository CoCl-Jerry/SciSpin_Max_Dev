import Settings
import socket
import UI_Update
import decimal
from time import sleep


def init():
    Settings.sendCMD("0~")


def light_confirm(self):
    curr_cmd = str(self.Start_spinBox.value() - 1) + "~" + str(self.End_spinBox.value() - 1) + "~" + str(self.R_spinBox.value()) + \
        "~" + str(self.G_spinBox.value()) + "~" + \
        str(self.B_spinBox.value()) + "~" + str(self.W_spinBox.value()) + \
        "~" + str(self.BRT_spinBox.value()) + "\n"
    Settings.commands_list.append(curr_cmd)

    Settings.sendCMD("3~1~" + curr_cmd)


def light_reset(self):
    Settings.sendCMD("3~0")
    Settings.sendCMD("3~4~50")

    self.R_spinBox.setValue(50)
    self.G_spinBox.setValue(0)
    self.B_spinBox.setValue(0)
    self.W_spinBox.setValue(0)
    self.Start_spinBox.setValue(1)
    self.End_spinBox.setValue(86)
    self.BRT_spinBox.setValue(50)
    Settings.commands_list.clear()


def clear_lights():
    Settings.sendCMD("3~0")


def IR_toggle(self):
    if not Settings.IR_stat:
        self.IR_pushButton.setText("IR STATUS:ON")
        CMD = "4~1"
    else:
        self.IR_pushButton.setText("IR STATUS:OFF")
        CMD = "4~0"
    Settings.IR_stat = not Settings.IR_stat
    Settings.sendCMD(CMD)


def deploy_lights():
    for x in Settings.commands_list:
        CMD = "3~2~" + x
        Settings.sendCMD(CMD)
        sleep(0.1)
    Settings.sendCMD("3~3")
    Settings.sendCMD("4~" + str(int(Settings.IR_stat)))


def extract_lights():
    Settings.sendCMD("4~0")
    clear_lights()


def motor_toggle(mot, self):
    if not mot:
        if Settings.LINKED and not Settings.frame_enabled:
            Settings.frame_enabled = True
            Settings.core_enabled = True
        elif Settings.LINKED and Settings.frame_enabled:
            Settings.frame_enabled = False
            Settings.core_enabled = False
        elif not Settings.LINKED and not Settings.frame_enabled:
            Settings.frame_enabled = True
        else:
            Settings.frame_enabled = False
    else:
        if Settings.LINKED and not Settings.core_enabled:
            Settings.frame_enabled = True
            Settings.core_enabled = True
        elif Settings.LINKED and Settings.core_enabled:
            Settings.frame_enabled = False
            Settings.core_enabled = False
        elif not Settings.LINKED and not Settings.core_enabled:
            Settings.core_enabled = True
        else:
            Settings.core_enabled = False
    CMD = ("1~0~" + str(int(Settings.frame_enabled)) +
           "~" + str(int(Settings.core_enabled)))
    Settings.sendCMD(CMD)
    UI_Update.motor_update(self)


def reverse_motor(mot, self):
    if Settings.LINKED:
        Settings.frame_dir = not Settings.frame_dir
        Settings.core_dir = not Settings.core_dir
    else:
        if not mot:
            Settings.frame_dir = not Settings.frame_dir

        else:
            Settings.core_dir = not Settings.core_dir
    CMD = ("1~1~" + str(int(Settings.frame_dir)) +
           "~" + str(int(Settings.core_dir)))
    Settings.sendCMD(CMD)
    UI_Update.dir(self)


def spin_change(mot, self):
    self.core_spinBox.blockSignals(True)
    self.frame_spinBox.blockSignals(True)
    self.core_verticalSlider.blockSignals(True)
    self.frame_verticalSlider.blockSignals(True)

    if Settings.LINKED:
        if not mot:
            if int(decimal.Decimal(str(self.frame_spinBox.value())) * 100) in Settings.speed_dict:
                Settings.frame_RPM = self.frame_spinBox.value()
                Settings.core_RPM = Settings.frame_RPM

                self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
                self.core_verticalSlider.setValue(Settings.core_RPM * 20)

                self.core_spinBox.setValue(Settings.core_RPM)
            else:
                Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 20

        else:
            if int(decimal.Decimal(str(self.core_spinBox.value())) * 100) in Settings.speed_dict:
                Settings.core_RPM = self.core_spinBox.value()
                Settings.frame_RPM = Settings.core_RPM

                self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
                self.core_verticalSlider.setValue(Settings.core_RPM * 20)

                self.frame_spinBox.setValue(Settings.frame_RPM)
            else:
                Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 20
    else:
        if not mot:
            if int(decimal.Decimal(str(self.frame_spinBox.value())) * 100) in Settings.speed_dict:
                Settings.frame_RPM = self.frame_spinBox.value()
                self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
            else:
                Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 20
        else:
            if int(decimal.Decimal(str(self.core_spinBox.value())) * 100) in Settings.speed_dict:
                Settings.core_RPM = self.core_spinBox.value()
                self.core_verticalSlider.setValue(Settings.core_RPM * 20)
            else:
                Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 20
    self.core_spinBox.blockSignals(False)
    self.frame_spinBox.blockSignals(False)
    self.core_verticalSlider.blockSignals(False)
    self.frame_verticalSlider.blockSignals(False)

    CMD = "1~2~" + getMicrostep(Settings.frame_RPM * 100) + "~" + str(Settings.speed_dict[int(decimal.Decimal(str(
        Settings.frame_RPM)) * 100)]) + "~" + str(getMicrostep(Settings.core_RPM * 100)) + "~" + str(Settings.speed_dict[int(decimal.Decimal(str(
            Settings.core_RPM)) * 100)])
    Settings.sendCMD(CMD)


def slider_change(mot, self):
    self.core_spinBox.blockSignals(True)
    self.frame_spinBox.blockSignals(True)
    self.core_verticalSlider.blockSignals(True)
    self.frame_verticalSlider.blockSignals(True)

    if Settings.LINKED:
        if not mot:
            Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 20
            Settings.core_RPM = Settings.frame_RPM
            self.core_verticalSlider.setValue(Settings.core_RPM * 20)

        else:
            Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 20
            Settings.frame_RPM = Settings.core_RPM
            self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
        self.frame_spinBox.setValue(Settings.frame_RPM)
        self.core_spinBox.setValue(Settings.core_RPM)
    else:
        if not mot:
            Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 20
            self.frame_spinBox.setValue(Settings.frame_RPM)
        else:
            Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 20
            self.core_spinBox.setValue(Settings.core_RPM)

    self.core_spinBox.blockSignals(False)
    self.frame_spinBox.blockSignals(False)
    self.core_verticalSlider.blockSignals(False)
    self.frame_verticalSlider.blockSignals(False)


def slider_Released():
    CMD = "1~2~" + getMicrostep(Settings.frame_RPM * 100) + "~" + str(Settings.speed_dict[int(decimal.Decimal(str(Settings.frame_RPM)) * 100)]) + "~" + getMicrostep(
        Settings.core_RPM * 100) + "~" + str(Settings.speed_dict[int(decimal.Decimal(str(Settings.core_RPM)) * 100)])
    Settings.sendCMD(CMD)


def getMicrostep(rpm):
    if rpm <= 100:
        return "256"
    elif rpm <= 200:
        return "128"
    elif rpm <= 300:
        return "64"
    elif rpm <= 400:
        return "32"
    elif rpm <= 600:
        return "16"
    elif rpm <= 1000:
        return "8"
