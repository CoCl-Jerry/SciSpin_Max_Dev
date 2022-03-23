import os
import Settings
import Commands
from PyQt5.QtGui import QImage, QPixmap


def cycle_start(self):
    self.confirmCycle_pushButton.setText("TERMINATE CYCLE")
    Settings.cycle_running = True


def cycle_end(self):
    self.confirmCycle_pushButton.setText("CONFIRM")
    Settings.cycle_running = False

def interval_start(self):
    self.startInterval_pushButton.setText("TERMINATE SEQUENCE")
    Settings.interval_running = True

def interval_end(self):
    self.startInterval_pushButton.setText("START SEQUENCE")


def snap_start(self):
    self.core_status_label.setText("Core Status: IMAGING")
    Settings.imaging = True
    update_imaging(self)


def snap_complete(self):
    self.core_status_label.setText("Core Status: IDLE")

    snap_img = QImage("../_temp/snapshot.jpg")
    self.Image_Frame.setPixmap(QPixmap(snap_img))
    Settings.imaging = False
    Settings.trasmitted = 0
    update_imaging(self)


def preview_complete(self):
    self.core_status_label.setText(
        "Time Taken " + str(Settings.time_elipsed) + "s")
    if Settings.imaging_mode == 1:
        preview_img = QImage("../_temp/preview.jpg")
        self.Image_Frame.setPixmap(QPixmap(preview_img))
        os.system("gpicview ../_temp/preview.jpg")
    else:
        preview_img = QImage("../_temp/preview.png")
        self.Image_Frame.setPixmap(QPixmap(preview_img))
        os.system("gpicview ../_temp/preview.png")
    Settings.imaging = False
    Settings.trasmitted = 0
    update_imaging(self)


def image_captured(self):
    capture_img = QImage(Settings.current_image)
    self.Image_Frame.setPixmap(QPixmap(capture_img))
    Settings.trasmitted = 0
    self.core_status_label.setText("Core Status: IDLE")
    self.Progress_Label.setText(
        "Progress: " + str(Settings.current) + "/" + str(Settings.total))
    self.Progress_Bar.setValue(Settings.current)
    self.startImaging_pushButton.setEnabled(True)


def lightingPreset_update(self):
    self.lightingPreset_tabWidget.setEnabled(
        not Settings.lightingPreset_running)
    if not Settings.lightingPreset_running:
        Commands.light_reset(self)


def sensor_update(self):

    if Settings.tag_index == 0:
        self.ACC_X_text_label.setText(Settings.ACC_X_text)
        self.ACC_Y_text_label.setText(Settings.ACC_Y_text)
        self.ACC_Z_text_label.setText(Settings.ACC_Z_text)

    elif Settings.tag_index == 1:
        self.TEMP_text_label.setText(Settings.TEMP_text)
        self.HUM_text_label.setText(Settings.HUD_text)

    else:
        self.PR_text_label.setText(Settings.PR_text)


def LED_validate(self):
    if self.Start_spinBox.value() >= self.End_spinBox.value():
        self.light_Confirm_pushButton.setEnabled(False)
    else:
        self.light_Confirm_pushButton.setEnabled(True)


def link(self):
    if Settings.LINKED:
        Settings.LINKED = False
        self.link_pushButton.setIcon(Settings.broken)
    else:
        Settings.LINKED = True
        self.link_pushButton.setIcon(Settings.linked)


def dir(self):
    if Settings.frame_dir:
        self.frameReverse_pushButton.setIcon(Settings.reverse)
    else:
        self.frameReverse_pushButton.setIcon(Settings.forward)

    if Settings.core_dir:
        self.coreReverse_pushButton.setIcon(Settings.reverse)
    else:
        self.coreReverse_pushButton.setIcon(Settings.forward)


def validate_input(self):
    Settings.total = int(Settings.duration / Settings.interval)
    if Settings.total > 0 and len(Settings.sequence_name) != 0:
        self.startImaging_pushButton.setEnabled(True)
    else:
        self.startImaging_pushButton.setEnabled(False)
    self.Progress_Label.setText(
        "Progress: " + str(Settings.current) + "/" + str(Settings.total))


def update_imaging(self):
    if Settings.imaging:
        self.Capture_frame.setEnabled(False)
        self.tabWidget.setEnabled(False)

    else:
        self.Capture_frame.setEnabled(True)
        self.tabWidget.setEnabled(True)

        validate_input(self)


def transmit_update(self):
    Settings.trasmitted += 1
    self.core_status_label.setText(
        "Recieving Packets: " + str(Settings.trasmitted))


def transmitst(self):
    self.startImaging_pushButton.setEnabled(False)


def sensor_logstart(self):
    self.log_pushButton.setEnabled(False)
    self.sample_doubleSpinBox.setEnabled(False)
    self.log_spinBox.setEnabled(False)


def sensor_logdone(self):
    self.log_pushButton.setEnabled(True)
    self.sample_doubleSpinBox.setEnabled(True)
    self.log_spinBox.setEnabled(True)


def timelapse_start(self):
    Settings.timelapse_running = True
    self.snapshot_pushButton.setEnabled(False)
    self.preview_pushButton.setEnabled(False)
    self.rotate_pushButton.setEnabled(False)

    self.title_lineEdit.setEnabled(False)
    self.addDate_pushButton.setEnabled(False)
    self.ICI_spinBox.setEnabled(False)
    self.ISD_spinBox.setEnabled(False)
    self.directory_pushButton.setEnabled(False)
    self.x_resolution_spinBox.setEnabled(False)
    self.y_resolution_spinBox.setEnabled(False)
    self.PNG_radioButton.setEnabled(False)
    self.JPG_radioButton.setEnabled(False)

    self.startImaging_pushButton.setText("TERMINATE TIMELAPSE")

    self.core_status_label.setText("Core Status: IMAGING")
    self.Progress_Bar.setMaximum(Settings.total)
    self.Progress_Bar.setMinimum(0)


def timelapse_end(self):
    Settings.timelapse_running = True
    self.snapshot_pushButton.setEnabled(True)
    self.preview_pushButton.setEnabled(True)
    self.rotate_pushButton.setEnabled(True)

    self.title_lineEdit.setEnabled(True)
    self.addDate_pushButton.setEnabled(True)
    self.ICI_spinBox.setEnabled(True)
    self.ISD_spinBox.setEnabled(True)
    self.directory_pushButton.setEnabled(True)
    self.x_resolution_spinBox.setEnabled(True)
    self.y_resolution_spinBox.setEnabled(True)
    self.PNG_radioButton.setEnabled(True)
    self.JPG_radioButton.setEnabled(True)
    self.startImaging_pushButton.setText("START TIMELAPSE")

    self.core_status_label.setText("Core Status: IDLE")


def motor_update(self):
    if not Settings.frame_enabled:
        self.frameErgz_pushButton.setText("DISABLE MOTOR")
    else:
        self.frameErgz_pushButton.setText("ENABLE MOTOR")

    if not Settings.core_enabled:
        self.coreErgz_pushButton.setText("DISABLE MOTOR")
    else:
        self.coreErgz_pushButton.setText("ENABLE MOTOR")


def fanlabel_update(self):
    self.fanSpeed_label.setText(
        "Speed: " + str(self.fanSpeed_horizontalSlider.sliderPosition()) + "%")
