import General

import os
import subprocess
import Commands
import Functions
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor

# ---------------------------------------------------------------------------- #
#                              system status check                             #
# ---------------------------------------------------------------------------- #


def system_status_check(self):
    self.main_update_status_pushButton.setEnabled(
        False)  # Disable update button

    # --------------------------- check core connection -------------------------- #
    if Functions.check_ip_connection(General.core_address):
        self.main_core_status_value_label.setPalette(General.palette_green)
        self.main_core_status_value_label.setText("Online")
    else:
        self.main_core_status_value_label.setPalette(General.palette_red)
        self.main_core_status_value_label.setText("Offline")
    # --------------------------- check MCU connection --------------------------- #
    if Functions.check_i2c_device(General.MCU_address):
        self.main_MCU_status_value_label.setPalette(General.palette_green)
        self.main_MCU_status_value_label.setText("Online")
    else:
        self.main_MCU_status_value_label.setPalette(General.palette_red)
        self.main_MCU_status_value_label.setText("Offline")
    # --------------------------- check ambient sensor connection ---------------- #
    if Functions.check_i2c_device(General.ambient_sensor_address):
        self.main_ambient_sensor_status_value_label.setPalette(
            General.palette_green)
        self.main_ambient_sensor_status_value_label.setText("Online")
    else:
        self.main_ambient_sensor_status_value_label.setPalette(
            General.palette_red)
        self.main_ambient_sensor_status_value_label.setText("Offline")
    # --------------------------- check motion sensor connection ----------------- #
    if Functions.check_i2c_device(General.motion_sensor_address):
        self.main_motion_sensor_status_value_label.setPalette(
            General.palette_green)
        self.main_motion_sensor_status_value_label.setText("Online")
    else:
        self.main_motion_sensor_status_value_label.setPalette(
            General.palette_red)
        self.main_motion_sensor_status_value_label.setText("Offline")
    # --------------------------- check storage space ---------------------------- #
    free_space = Functions.get_remaining_storage()
    formatted_free_space = "{:.1f}".format(free_space)
    if free_space < 2:
        self.main_drive_capacity_value_label.setPalette(General.palette_red)
        self.main_drive_capacity_value_label.setText(
            formatted_free_space + "GB")
        self.main_image_label.setPixmap(
            QPixmap(General.storage_critical_error_image))
    else:
        self.main_drive_capacity_value_label.setPalette(General.palette_green)
        self.main_drive_capacity_value_label.setText(
            formatted_free_space + "GB")

    self.main_update_status_pushButton.setEnabled(True)  # Enable update button

# ---------------------------------------------------------------------------- #
#                           lighting UI manipulations                          #
# ---------------------------------------------------------------------------- #


def lighting_reset(self):
    self.lighting_start_LED_value_spinBox.setValue(1)
    self.lighting_end_LED_value_spinBox.setValue(130)
    self.lighting_brightness_value_spinBox.setValue(50)

    self.lighting_red_value_spinBox.setValue(100)
    self.lighting_green_value_spinBox.setValue(0)
    self.lighting_blue_value_spinBox.setValue(0)
    self.lighting_white_value_spinBox.setValue(0)
    General.commands_list.clear()

def lighting_source_update(self):
    Commands.lighting_reset(self)
    if self.lighting_source_tabWidget.currentIndex() == 0:
        self.lighting_LED_settings_text_label.setText("<html><head/><body><p align="center"><span style=" font-weight:700;">LED Settings: [1,90]</span></p></body></html>")
    else:
        self.lighting_LED_settings_text_label.setText("<html><head/><body><p align="center"><span style=" font-weight:700;">LED Settings: [1,40]</span></p></body></html>")


# def init(self):
#     # --------------------------- check core connection -------------------------- #
#     output = subprocess.check_output(["ip", "addr", "show"])
#     if "peer" in str(output):
#         General.camera_status = True
#         self.camera_status_value_label.setText()
#     else:
#         General.camera_status = False

#     filesystem = os.statvfs("/")
#     free_space = filesystem.f_bsize * filesystem.f_bavail
#     free_space_mb = free_space / (1024 * 1024)
#     if free_space_mb < 500:
#         General.storage_critical_error = True
#         error_UI_update(self)
#         print("remaining storage space:" + str(free_space_mb))


# def cycle_start(self):
#     self.confirmCycle_pushButton.setText("TERMINATE CYCLE")
#     Settings.cycle_running = True


# def cycle_end(self):
#     self.confirmCycle_pushButton.setText("CONFIRM")
#     Settings.cycle_running = False


# def snap_start(self):
#     self.core_status_label.setText("Core Status: IMAGING")
#     Settings.imaging = True
#     update_imaging(self)


# def snap_complete(self):
#     self.core_status_label.setText("Core Status: IDLE")

#     snap_img = QImage("../_temp/snapshot.jpg")
#     self.Image_Frame.setPixmap(QPixmap(snap_img))
#     Settings.imaging = False
#     Settings.trasmitted = 0
#     update_imaging(self)


# def preview_complete(self):
#     self.core_status_label.setText(
#         "Time Taken " + str(Settings.time_elipsed) + "s")
#     if Settings.imaging_mode == 1:
#         preview_img = QImage("../_temp/preview.jpg")
#         self.Image_Frame.setPixmap(QPixmap(preview_img))
#         os.system("gpicview ../_temp/preview.jpg")
#     else:
#         preview_img = QImage("../_temp/preview.png")
#         self.Image_Frame.setPixmap(QPixmap(preview_img))
#         os.system("gpicview ../_temp/preview.png")
#     Settings.imaging = False
#     Settings.trasmitted = 0
#     update_imaging(self)


# def image_captured(self):
#     capture_img = QImage(Settings.current_image)
#     self.Image_Frame.setPixmap(QPixmap(capture_img))
#     Settings.trasmitted = 0
#     self.core_status_label.setText("Core Status: IDLE")
#     self.Progress_Label.setText(
#         "Progress: " + str(Settings.current) + "/" + str(Settings.total))
#     self.Progress_Bar.setValue(Settings.current)
#     self.startImaging_pushButton.setEnabled(True)


# def lightingPreset_update(self):
#     self.lightingPreset_tabWidget.setEnabled(
#         not Settings.lightingPreset_running)
#     if not Settings.lightingPreset_running:
#         Commands.light_reset(self)


# def sensor_update(self):

#     if Settings.tag_index == 0:
#         self.ACC_X_text_label.setText(Settings.ACC_X_text)
#         self.ACC_Y_text_label.setText(Settings.ACC_Y_text)
#         self.ACC_Z_text_label.setText(Settings.ACC_Z_text)

#     elif Settings.tag_index == 1:
#         self.TEMP_text_label.setText(Settings.TEMP_text)
#         self.HUM_text_label.setText(Settings.HUD_text)

#     else:
#         self.PR_text_label.setText(Settings.PR_text)


# def LED_validate(self):
#     if self.Start_spinBox.value() >= self.End_spinBox.value():
#         self.light_Confirm_pushButton.setEnabled(False)
#     else:
#         self.light_Confirm_pushButton.setEnabled(True)


# def link(self):
#     if Settings.LINKED:
#         Settings.LINKED = False
#         self.link_pushButton.setIcon(Settings.broken)
#     else:
#         Settings.LINKED = True
#         self.link_pushButton.setIcon(Settings.linked)


# def dir(self):
#     if Settings.frame_dir:
#         self.frameReverse_pushButton.setIcon(Settings.reverse)
#     else:
#         self.frameReverse_pushButton.setIcon(Settings.forward)

#     if Settings.core_dir:
#         self.coreReverse_pushButton.setIcon(Settings.reverse)
#     else:
#         self.coreReverse_pushButton.setIcon(Settings.forward)


# def validate_input(self):
#     Settings.total = int(Settings.duration / Settings.interval)
#     if Settings.total > 0 and len(Settings.sequence_name) != 0:
#         self.startImaging_pushButton.setEnabled(True)
#     else:
#         self.startImaging_pushButton.setEnabled(False)
#     self.Progress_Label.setText(
#         "Progress: " + str(Settings.current) + "/" + str(Settings.total))


# def update_imaging(self):
#     if Settings.imaging:
#         self.Capture_frame.setEnabled(False)
#         self.tabWidget.setEnabled(False)

#     else:
#         self.Capture_frame.setEnabled(True)
#         self.tabWidget.setEnabled(True)

#         validate_input(self)


# def transmit_update(self):
#     Settings.trasmitted += 1
#     self.core_status_label.setText(
#         "Recieving Packets: " + str(Settings.trasmitted))


# def transmitst(self):
#     self.startImaging_pushButton.setEnabled(False)


# def sensor_logstart(self):
#     self.log_pushButton.setEnabled(False)
#     self.sample_doubleSpinBox.setEnabled(False)
#     self.log_spinBox.setEnabled(False)


# def sensor_logdone(self):
#     self.log_pushButton.setEnabled(True)
#     self.sample_doubleSpinBox.setEnabled(True)
#     self.log_spinBox.setEnabled(True)


# def timelapse_start(self):
#     Settings.timelapse_running = True
#     self.snapshot_pushButton.setEnabled(False)
#     self.preview_pushButton.setEnabled(False)
#     self.rotate_pushButton.setEnabled(False)

#     self.title_lineEdit.setEnabled(False)
#     self.addDate_pushButton.setEnabled(False)
#     self.ICI_spinBox.setEnabled(False)
#     self.ISD_spinBox.setEnabled(False)
#     self.directory_pushButton.setEnabled(False)
#     self.x_resolution_spinBox.setEnabled(False)
#     self.y_resolution_spinBox.setEnabled(False)
#     self.PNG_radioButton.setEnabled(False)
#     self.JPG_radioButton.setEnabled(False)

#     self.startImaging_pushButton.setText("TERMINATE TIMELAPSE")

#     self.core_status_label.setText("Core Status: IMAGING")
#     self.Progress_Bar.setMaximum(Settings.total)
#     self.Progress_Bar.setMinimum(0)


# def timelapse_end(self):
#     Settings.timelapse_running = True
#     self.snapshot_pushButton.setEnabled(True)
#     self.preview_pushButton.setEnabled(True)
#     self.rotate_pushButton.setEnabled(True)

#     self.title_lineEdit.setEnabled(True)
#     self.addDate_pushButton.setEnabled(True)
#     self.ICI_spinBox.setEnabled(True)
#     self.ISD_spinBox.setEnabled(True)
#     self.directory_pushButton.setEnabled(True)
#     self.x_resolution_spinBox.setEnabled(True)
#     self.y_resolution_spinBox.setEnabled(True)
#     self.PNG_radioButton.setEnabled(True)
#     self.JPG_radioButton.setEnabled(True)
#     self.startImaging_pushButton.setText("START TIMELAPSE")

#     self.core_status_label.setText("Core Status: IDLE")


# def motor_update(self):
#     if not Settings.frame_enabled:
#         self.frameErgz_pushButton.setText("DISABLE MOTOR")
#     else:
#         self.frameErgz_pushButton.setText("ENABLE MOTOR")

#     if not Settings.core_enabled:
#         self.coreErgz_pushButton.setText("DISABLE MOTOR")
#     else:
#         self.coreErgz_pushButton.setText("ENABLE MOTOR")


# def fanlabel_update(self):
#     self.fanSpeed_label.setText(
#         "Speed: " + str(self.fanSpeed_horizontalSlider.sliderPosition()) + "%")
