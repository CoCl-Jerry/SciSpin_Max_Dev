import General
import Communication
import socket
import UI_Update
import decimal
from time import sleep


def reset_MCU():
    Communication.sendCMD("0~")

# ---------------------------------------------------------------------------- #
#                             commands for lighting                            #
# ---------------------------------------------------------------------------- #


def lighting_confirm(self):
    if self.lighting_source_tabWidget.currentIndex() == 0:
        curr_cmd = str(self.lighting_start_LED_value_spinBox.value() - 1) + "~" + str(self.lighting_end_LED_value_spinBox.value()) + "~" + str(self.lighting_red_value_spinBox.value()) + \
            "~" + str(self.lighting_green_value_spinBox.value()) + "~" + \
            str(self.lighting_blue_value_spinBox.value()) + "~" + str(self.lighting_white_value_spinBox.value()) + \
            "~" + str(self.lighting_brightness_value_spinBox.value()) + "\n"
    else:
        curr_cmd = str(self.lighting_start_LED_value_spinBox.value() + 89) + "~" + str(self.lighting_end_LED_value_spinBox.value()+90) + "~" + str(self.lighting_red_value_spinBox.value()) + \
            "~" + str(self.lighting_green_value_spinBox.value()) + "~" + \
            str(self.lighting_blue_value_spinBox.value()) + "~" + str(self.lighting_white_value_spinBox.value()) + \
            "~" + str(self.lighting_brightness_value_spinBox.value()) + "\n"

    General.commands_list.append(curr_cmd)

    Communication.sendCMD("3~1~" + curr_cmd)


def lighting_reset():
    Communication.sendCMD("3~0")
    Communication.sendCMD("3~4~50")


def clear_lights():
    Communication.sendCMD("3~0")


def IR_toggle():
    if General.IR_stat:
        Communication.sendCMD("4~1")
    else:
        Communication.sendCMD("4~0")

# ---------------------------------------------------------------------------- #
#                           commands for power cycle                           #
# ---------------------------------------------------------------------------- #


def extract_lights():
    Communication.sendCMD("4~0")
    Communication.sendCMD("3~0")


def deploy_lights():
    for x in General.commands_list:
        CMD = "3~2~" + x
        Communication.sendCMD(CMD)
    Communication.sendCMD("3~3")
    Communication.sendCMD("4~" + str(int(General.IR_stat)))


# def motor_toggle(mot, self):
#     if not mot:
#         if Settings.LINKED and not Settings.frame_enabled:
#             Settings.frame_enabled = True
#             Settings.core_enabled = True
#         elif Settings.LINKED and Settings.frame_enabled:
#             Settings.frame_enabled = False
#             Settings.core_enabled = False
#         elif not Settings.LINKED and not Settings.frame_enabled:
#             Settings.frame_enabled = True
#         else:
#             Settings.frame_enabled = False
#     else:
#         if Settings.LINKED and not Settings.core_enabled:
#             Settings.frame_enabled = True
#             Settings.core_enabled = True
#         elif Settings.LINKED and Settings.core_enabled:
#             Settings.frame_enabled = False
#             Settings.core_enabled = False
#         elif not Settings.LINKED and not Settings.core_enabled:
#             Settings.core_enabled = True
#         else:
#             Settings.core_enabled = False
#     CMD = ("1~0~" + str(int(Settings.frame_enabled)) +
#            "~" + str(int(Settings.core_enabled)))
#     Settings.sendCMD(CMD)
#     UI_Update.motor_update(self)


# def reverse_motor(mot, self):
#     if Settings.LINKED:
#         Settings.frame_dir = not Settings.frame_dir
#         Settings.core_dir = not Settings.core_dir
#     else:
#         if not mot:
#             Settings.frame_dir = not Settings.frame_dir

#         else:
#             Settings.core_dir = not Settings.core_dir
#     CMD = ("1~1~" + str(int(Settings.frame_dir)) +
#            "~" + str(int(Settings.core_dir)))
#     Settings.sendCMD(CMD)
#     UI_Update.dir(self)


# def slider_Released():
#     CMD = "1~2~" + getMicrostep(Settings.frame_RPM * 100) + "~" + str(Settings.speed_dict[int(decimal.Decimal(str(Settings.frame_RPM)) * 100)]) + "~" + getMicrostep(
#         Settings.core_RPM * 100) + "~" + str(Settings.speed_dict[int(decimal.Decimal(str(Settings.core_RPM)) * 100)])
#     Settings.sendCMD(CMD)
