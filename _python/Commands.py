import General
import Communication


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


def IR_imaging_toggle(state):
    if state:
        extract_lights()
        Communication.sendCMD("4~1")
    else:
        Communication.sendCMD("4~0")
        deploy_lights()
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


# ---------------------------------------------------------------------------- #
#                              commands for motors                             #
# ---------------------------------------------------------------------------- #

def set_speed():
    print("Frame Target Speed: "+str(General.frame_RPM))
    print("Frame SPS: "+str(General.frame_SPS))
    print("Frame Microstepping: "+str(General.frame_microstepping))
    print("Core Target Speed: "+str(General.core_RPM))
    print("Core SPS: "+str(General.core_SPS))
    print("Core Microstepping: "+str(General.core_microstepping))
    print()
    Communication.sendCMD("1~2~" + str(General.frame_SPS*1000*General.frame_direction) + "~" + str(General.frame_microstepping) +
                          "~" + str(General.core_SPS*1000*General.core_direction) + "~" + str(General.core_microstepping))


def motor_enable():
    Communication.sendCMD(
        "1~0~"+str(int(General.frame_enabled)) + "~"+str(int(General.core_enabled)))

# ---------------------------------------------------------------------------- #
#                               commands for fan                               #
# ---------------------------------------------------------------------------- #


def set_fan_speed(self):
    Communication.sendCMD(
        "5~"+str(self.lighting_controller_fan_speed_horizontalSlider.value()))
