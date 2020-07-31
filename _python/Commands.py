import Settings
import socket
import UI_Update
#from PyQt5.QtCore import QThread
#from PyQt5 import QtCore, QtGui, QtWidgets


def init():
    Settings.sendCMD(Settings.lighting_addr, "7~")
    Settings.sendCMD(Settings.frame_addr, "5~")
    Settings.sendCMD(Settings.core_addr, "5~")


def light_confirm(self):
    curr_cmd = str(self.Start_spinBox.value() - 1) + "~" + str(self.End_spinBox.value() - 1) + "~" + str(self.R_spinBox.value()) + \
        "~" + str(self.G_spinBox.value()) + "~" + \
        str(self.B_spinBox.value()) + "~" + str(self.W_spinBox.value())
    Settings.commands_list.append(curr_cmd)
    print(Settings.lighting_addr, "1~" + curr_cmd)
    Settings.sendCMD(Settings.lighting_addr, "1~" + curr_cmd)
    curr_cmd = "2~" + str(self.BRT_spinBox.value())
    Settings.sendCMD(Settings.lighting_addr, curr_cmd)


def light_reset(self):
    Settings.sendCMD(Settings.lighting_addr, "1~0~83~0~0~0~0")
    Settings.sendCMD(Settings.lighting_addr, "2~128")

    self.R_spinBox.setValue(50)
    self.G_spinBox.setValue(0)
    self.B_spinBox.setValue(0)
    self.W_spinBox.setValue(0)
    self.Start_spinBox.setValue(1)
    self.End_spinBox.setValue(84)
    self.BRT_spinBox.setValue(50)
    Settings.commands_list.clear()


def clear_lights():
    Settings.sendCMD(Settings.lighting_addr, "1~0~83~0~0~0~0")


def ergz_motor(addr):
    if(Settings.LINKED):
        Settings.sendCMD(Settings.frame_addr, "1~")
        Settings.sendCMD(Settings.core_addr, "1~")
    else:
        Settings.sendCMD(addr, "1~")


def reverse_motor(addr, motor, self):
    if(Settings.LINKED):
        Settings.sendCMD(Settings.frame_addr, "3~")
        Settings.sendCMD(Settings.core_addr, "3~")
        Settings.frame_dir = not Settings.frame_dir
        Settings.core_dir = not Settings.core_dir
    else:
        if (motor):
            Settings.sendCMD(Settings.frame_addr, "3~")
            Settings.frame_dir = not Settings.frame_dir
        else:
            Settings.sendCMD(Settings.core_addr, "3~")
            Settings.core_dir = not Settings.core_dir
    UI_Update.dir(self)


def linked_spin_change(self):
    self.core_spinBox.blockSignals(True)
    self.frame_spinBox.blockSignals(True)
    self.core_verticalSlider.blockSignals(True)
    self.frame_verticalSlider.blockSignals(True)

    if(Settings.frame_RPM != self.frame_spinBox.value()):

        Settings.frame_RPM = self.frame_spinBox.value()
        Settings.core_RPM = Settings.frame_RPM
        self.core_verticalSlider.setValue(Settings.core_RPM * 10)
        self.frame_verticalSlider.setValue(Settings.frame_RPM * 10)
        self.core_spinBox.setValue(Settings.core_RPM)

    else:
        Settings.core_RPM = self.core_spinBox.value()
        Settings.frame_RPM = Settings.core_RPM
        self.frame_verticalSlider.setValue(Settings.frame_RPM * 10)
        self.core_verticalSlider.setValue(Settings.core_RPM * 10)
        self.frame_spinBox.setValue(Settings.frame_RPM)

    CMD = "2~" + str(int(Settings.frame_RPM * 10))
    Settings.sendCMD(Settings.frame_addr, CMD)
    CMD = "2~" + str(int(Settings.core_RPM * 10))
    Settings.sendCMD(Settings.core_addr, CMD)

    self.core_spinBox.blockSignals(False)
    self.frame_spinBox.blockSignals(False)
    self.core_verticalSlider.blockSignals(False)
    self.frame_verticalSlider.blockSignals(False)


def frame_spin_select(self):
    Settings.frame_RPM = self.frame_spinBox.value()

    self.frame_verticalSlider.blockSignals(True)
    self.frame_verticalSlider.setValue(Settings.frame_RPM * 10)
    self.frame_verticalSlider.blockSignals(False)

    CMD = "2~" + str(int(Settings.frame_RPM * 10))
    Settings.sendCMD(Settings.frame_addr, CMD)


def core_spin_select(self):
    Settings.core_RPM = self.core_spinBox.value()

    self.core_verticalSlider.blockSignals(True)
    self.core_verticalSlider.setValue(Settings.core_RPM * 10)
    self.core_verticalSlider.blockSignals(False)

    CMD = "2~" + str(int(Settings.core_RPM * 10))
    Settings.sendCMD(Settings.core_addr, CMD)


def frame_slider_change(self):
    Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 10
    self.frame_spinBox.setValue(Settings.frame_RPM)


def core_slider_change(self):
    Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 10
    self.core_spinBox.setValue(Settings.core_RPM)


def linked_slider_change(self):
    self.core_spinBox.blockSignals(True)
    self.frame_spinBox.blockSignals(True)
    self.core_verticalSlider.blockSignals(True)
    self.frame_verticalSlider.blockSignals(True)

    if(Settings.frame_RPM != self.frame_verticalSlider.sliderPosition() / 10):
        Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 10
        Settings.core_RPM = Settings.frame_RPM
        self.core_verticalSlider.setValue(Settings.core_RPM * 10)
        self.core_spinBox.setValue(Settings.core_RPM)
        self.frame_spinBox.setValue(Settings.frame_RPM)
    else:
        Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 10
        Settings.frame_RPM = Settings.core_RPM
        self.frame_verticalSlider.setValue(Settings.frame_RPM * 10)
        self.core_spinBox.setValue(Settings.core_RPM)
        self.frame_spinBox.setValue(Settings.frame_RPM)

    CMD = "2~" + str(int(Settings.frame_RPM * 10))
    Settings.sendCMD(Settings.frame_addr, CMD)
    CMD = "2~" + str(int(Settings.core_RPM * 10))
    Settings.sendCMD(Settings.core_addr, CMD)

    self.core_spinBox.blockSignals(False)
    self.frame_spinBox.blockSignals(False)
    self.core_verticalSlider.blockSignals(False)
    self.frame_verticalSlider.blockSignals(False)


def IR_trigger():
    Settings.sendCMD(Settings.lighting_addr, "3~")
    if not Settings.IR_STAT:
        Settings.IR_STAT = True

    else:
        Settings.IR_STAT = False

# def Rainbow_trigger():
# def Disco_trigger():


def IR_Imaging_trigger():
    Settings.sendCMD(Settings.lighting_addr, "6~")
