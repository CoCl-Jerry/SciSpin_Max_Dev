import Settings
import socket
import UI_Update
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


def frame_toggle(self):
    if Settings.LINKED and not Settings.frame_enabled:
        Settings.sendCMD("1~1")
        Settings.sendCMD("2~1")

        Settings.frame_enabled = True
        Settings.core_enabled = True
    elif Settings.LINKED and Settings.frame_enabled:
        Settings.sendCMD("1~0")
        Settings.sendCMD("2~0")

        Settings.frame_enabled = False
        Settings.core_enabled = False
    elif not Settings.LINKED and not Settings.frame_enabled:
        Settings.sendCMD("1~1")
        Settings.frame_enabled = True

    else:
        Settings.sendCMD("1~0")
        Settings.frame_enabled = False
    UI_Update.motor_update(self)


def core_toggle(self):
    if Settings.LINKED and not Settings.core_enabled:
        Settings.sendCMD("1~1")
        Settings.sendCMD("2~1")

        Settings.frame_enabled = True
        Settings.core_enabled = True
    elif Settings.LINKED and Settings.core_enabled:
        Settings.sendCMD("1~0")
        Settings.sendCMD("2~0")

        Settings.frame_enabled = False
        Settings.core_enabled = False
    elif not Settings.LINKED and not Settings.core_enabled:
        Settings.sendCMD("2~1")
        Settings.core_enabled = True

    else:
        Settings.sendCMD("2~0")
        Settings.core_enabled = False
    UI_Update.motor_update(self)


def reverse_motor(motor, self):
    if(Settings.LINKED):
        Settings.frame_dir = not Settings.frame_dir
        Settings.core_dir = not Settings.core_dir
        Settings.sendCMD("1~2" + str(int(Settings.frame_dir)))
        Settings.sendCMD("2~2" + str(int(Settings.core_dir)))

    else:
        if not motor:
            Settings.frame_dir = not Settings.frame_dir
            Settings.sendCMD("1~2" + str(int(Settings.frame_dir)))

        else:
            Settings.core_dir = not Settings.core_dir
            Settings.sendCMD("2~2" + str(int(Settings.core_dir)))
    UI_Update.dir(self)
#
#
# def linked_spin_change(self):
#     self.core_spinBox.blockSignals(True)
#     self.frame_spinBox.blockSignals(True)
#     self.core_verticalSlider.blockSignals(True)
#     self.frame_verticalSlider.blockSignals(True)
#
#     if(Settings.frame_RPM != self.frame_spinBox.value()):
#
#         Settings.frame_RPM = self.frame_spinBox.value()
#         Settings.core_RPM = Settings.frame_RPM
#         self.core_verticalSlider.setValue(Settings.core_RPM * 10)
#         self.frame_verticalSlider.setValue(Settings.frame_RPM * 10)
#         self.core_spinBox.setValue(Settings.core_RPM)
#
#     else:
#         Settings.core_RPM = self.core_spinBox.value()
#         Settings.frame_RPM = Settings.core_RPM
#         self.frame_verticalSlider.setValue(Settings.frame_RPM * 10)
#         self.core_verticalSlider.setValue(Settings.core_RPM * 10)
#         self.frame_spinBox.setValue(Settings.frame_RPM)
#
#     CMD = "2~" + str(int(Settings.frame_RPM * 10))
#     Settings.sendCMD(Settings.frame_addr, CMD)
#     CMD = "2~" + str(int(Settings.core_RPM * 10))
#     Settings.sendCMD(Settings.core_addr, CMD)
#
#     self.core_spinBox.blockSignals(False)
#     self.frame_spinBox.blockSignals(False)
#     self.core_verticalSlider.blockSignals(False)
#     self.frame_verticalSlider.blockSignals(False)
#
#
# def frame_spin_select(self):
#     Settings.frame_RPM = self.frame_spinBox.value()
#
#     self.frame_verticalSlider.blockSignals(True)
#     self.frame_verticalSlider.setValue(Settings.frame_RPM * 10)
#     self.frame_verticalSlider.blockSignals(False)
#
#     CMD = "2~" + str(int(Settings.frame_RPM * 10))
#     Settings.sendCMD(Settings.frame_addr, CMD)
#
#
# def core_spin_select(self):
#     Settings.core_RPM = self.core_spinBox.value()
#
#     self.core_verticalSlider.blockSignals(True)
#     self.core_verticalSlider.setValue(Settings.core_RPM * 10)
#     self.core_verticalSlider.blockSignals(False)
#
#     CMD = "2~" + str(int(Settings.core_RPM * 10))
#     Settings.sendCMD(Settings.core_addr, CMD)
#
#
# def frame_slider_change(self):
#     Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 10
#     self.frame_spinBox.setValue(Settings.frame_RPM)
#
#
# def core_slider_change(self):
#     Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 10
#     self.core_spinBox.setValue(Settings.core_RPM)
#
#
# def linked_slider_change(self):
#     self.core_spinBox.blockSignals(True)
#     self.frame_spinBox.blockSignals(True)
#     self.core_verticalSlider.blockSignals(True)
#     self.frame_verticalSlider.blockSignals(True)
#
#     if(Settings.frame_RPM != self.frame_verticalSlider.sliderPosition() / 10):
#         Settings.frame_RPM = self.frame_verticalSlider.sliderPosition() / 10
#         Settings.core_RPM = Settings.frame_RPM
#         self.core_verticalSlider.setValue(Settings.core_RPM * 10)
#         self.core_spinBox.setValue(Settings.core_RPM)
#         self.frame_spinBox.setValue(Settings.frame_RPM)
#     else:
#         Settings.core_RPM = self.core_verticalSlider.sliderPosition() / 10
#         Settings.frame_RPM = Settings.core_RPM
#         self.frame_verticalSlider.setValue(Settings.frame_RPM * 10)
#         self.core_spinBox.setValue(Settings.core_RPM)
#         self.frame_spinBox.setValue(Settings.frame_RPM)
#
#     CMD = "2~" + str(int(Settings.frame_RPM * 10))
#     Settings.sendCMD(Settings.frame_addr, CMD)
#     CMD = "2~" + str(int(Settings.core_RPM * 10))
#     Settings.sendCMD(Settings.core_addr, CMD)
#
#     self.core_spinBox.blockSignals(False)
#     self.frame_spinBox.blockSignals(False)
#     self.core_verticalSlider.blockSignals(False)
#     self.frame_verticalSlider.blockSignals(False)
#
#
#
#
# def IR_Imaging_trigger():
#     Settings.sendCMD(Settings.lighting_addr, "6~\n")
