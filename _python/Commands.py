import Settings
import socket
import UI_Update
import math
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
        current_CMD = "4~1"
    else:
        self.IR_pushButton.setText("IR STATUS:OFF")
        current_CMD = "4~0"
    Settings.IR_stat = not Settings.IR_stat
    Settings.sendCMD(current_CMD)


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
    current_CMD = ("1~0~" + str(int(Settings.frame_enabled)) +
                   "~" + str(int(Settings.core_enabled)))
    UI_Update.motor_update(self)


def reverse_motor(mot, self):
    if Settings.LINKED:
        Settings.frame_dir = not Settings.frame_dir
        Settings.core_dir = not Settings.core_dir
    else:
        if not motor:
            Settings.frame_dir = not Settings.frame_dir

        else:
            Settings.core_dir = not Settings.core_dir
    current_CMD = ("1~1~" + str(int(Settings.frame_dir)) +
                   "~" + str(int(Settings.frame_dir)))
    UI_Update.dir(self)


def linked_spin_change(self):
    self.core_spinBox.blockSignals(True)
    self.frame_spinBox.blockSignals(True)
    self.core_verticalSlider.blockSignals(True)
    self.frame_verticalSlider.blockSignals(True)

    if Settings.frame_RPM != self.frame_spinBox.value():

        Settings.frame_RPM = self.frame_spinBox.value()
        Settings.core_RPM = Settings.frame_RPM
        self.core_verticalSlider.setValue(Settings.core_RPM * 20)
        self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
        self.core_spinBox.setValue(Settings.core_RPM)

    else:
        Settings.core_RPM = self.core_spinBox.value()
        Settings.frame_RPM = Settings.core_RPM
        self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
        self.core_verticalSlider.setValue(Settings.core_RPM * 20)
        self.frame_spinBox.setValue(Settings.frame_RPM)

    try:
        CMD = "1~3~" + getMicrostep(Settings.frame_RPM * 20) + "~" + \
            str(Settings.speed_dict[int(Settings.frame_RPM * 100)])
        Settings.sendCMD(CMD)
        CMD = "2~3~" + getMicrostep(Settings.core_RPM * 20) + "~" + \
            str(Settings.speed_dict[int(Settings.core_RPM * 100)])
        Settings.sendCMD(CMD)
    except Exception as e:
        print(e)

    self.core_spinBox.blockSignals(False)
    self.frame_spinBox.blockSignals(False)
    self.core_verticalSlider.blockSignals(False)
    self.frame_verticalSlider.blockSignals(False)


def frame_spin_select(self):
    Settings.frame_RPM = self.frame_spinBox.value()

    self.frame_verticalSlider.blockSignals(True)
    self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
    self.frame_verticalSlider.blockSignals(False)
    try:
        CMD = "1~3~" + getMicrostep(Settings.frame_RPM * 20) + "~" + \
            str(Settings.speed_dict[int(Settings.frame_RPM * 100)])
        Settings.sendCMD(CMD)
    except Exception as e:
        print(e)


def core_spin_select(self):
    Settings.core_RPM = self.core_spinBox.value()

    self.core_verticalSlider.blockSignals(True)
    self.core_verticalSlider.setValue(Settings.core_RPM * 20)
    self.core_verticalSlider.blockSignals(False)
    try:
        CMD = "2~3~" + getMicrostep(Settings.core_RPM * 20) + "~" + \
            str(Settings.speed_dict[int(Settings.core_RPM * 100)])
        Settings.sendCMD(CMD)
    except Exception as e:
        print(e)


def frame_slider_change(self):
    Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 20
    self.frame_spinBox.setValue(Settings.frame_RPM)


def core_slider_change(self):
    Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 20
    self.core_spinBox.setValue(Settings.core_RPM)


def linked_slider_change(self):
    self.core_spinBox.blockSignals(True)
    self.frame_spinBox.blockSignals(True)
    self.core_verticalSlider.blockSignals(True)
    self.frame_verticalSlider.blockSignals(True)

    if Settings.frame_RPM != self.frame_verticalSlider.sliderPosition() / 20:
        Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 20
        Settings.core_RPM = Settings.frame_RPM
        self.core_verticalSlider.setValue(Settings.core_RPM * 20)
        self.core_spinBox.setValue(Settings.core_RPM)
        self.frame_spinBox.setValue(Settings.frame_RPM)
    else:
        Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 20
        Settings.frame_RPM = Settings.core_RPM
        self.frame_verticalSlider.setValue(Settings.frame_RPM * 20)
        self.core_spinBox.setValue(Settings.core_RPM)
        self.frame_spinBox.setValue(Settings.frame_RPM)

    try:
        CMD = "1~3~" + getMicrostep(Settings.frame_RPM * 20) + "~" + \
            str(Settings.speed_dict[int(Settings.frame_RPM * 100)])
        Settings.sendCMD(CMD)
        CMD = "2~3~" + getMicrostep(Settings.core_RPM * 20) + "~" + \
            str(Settings.speed_dict[int(Settings.core_RPM * 100)])
        Settings.sendCMD(CMD)
    except Exception as e:
        print(e)

    self.core_spinBox.blockSignals(False)
    self.frame_spinBox.blockSignals(False)
    self.core_verticalSlider.blockSignals(False)
    self.frame_verticalSlider.blockSignals(False)


def getMicrostep(rpm):
    if rpm <= 150:
        return "256"
    elif rpm <= 250:
        return "128"
    elif rpm <= 350:
        return "64"
