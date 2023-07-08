import General
import Commands
import Threads
import UI_Update
import Functions
import Call_Thread
import os
import time

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

import Clinostat_UI


class MainWindow(QMainWindow, Clinostat_UI.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

# ------------------------------- initialzation ------------------------------ #
        UI_Update.system_status_check(self)
        Commands.reset_MCU()
# ------------------------------ Main UI signals ----------------------------- #
        self.main_update_status_pushButton.clicked.connect(
            lambda: UI_Update.system_status_check(self))

# ------------------------- RGB LED lighting signals ------------------------- #
        self.lighting_LED_confirm_pushButton.clicked.connect(
            lambda: Commands.lighting_confirm(self))
        self.lighting_LED_reset_pushButton.clicked.connect(
            lambda: UI_Update.lighting_source_update(self))
        self.lighting_source_tabWidget.currentChanged.connect(
            lambda: UI_Update.lighting_source_update(self))

# --------------------------- Power cycle signals ---------------------------- #
        self.lighting_confirm_cycle_pushButton.clicked.connect(
            lambda: Call_Thread.start_cycle(self))

# -------------------------- IR LED lighting signals ------------------------- #
        self.lighting_IR_toggle_pushButton.clicked.connect(
            lambda: UI_Update.IR_lighting_update(self))

# ------------------------------- motor signals ------------------------------ #
        self.motion_frame_motor_value_spinBox.valueChanged.connect(
            lambda: UI_Update.motor_spinbox_changed(1, self))
        self.motion_core_motor_value_spinBox.valueChanged.connect(
            lambda: UI_Update.motor_spinbox_changed(0, self))

        self.motion_frame_motor_value_verticalSlider.valueChanged.connect(
            lambda: UI_Update.motor_slider_change(1, self))
        self.motion_core_motor_value_verticalSlider.valueChanged.connect(
            lambda: UI_Update.motor_slider_change(0, self))


#         Call_Thread.sensor_init(self)
#         Commands.init()

#         self.Sensor_tabWidget.currentChanged.connect(
#             lambda: Functions.printci(self))

#         self.frameErgz_pushButton.clicked.connect(
#             lambda: Commands.motor_toggle(0, self))
#         self.coreErgz_pushButton.clicked.connect(
#             lambda: Commands.motor_toggle(1, self))

#         self.frameReverse_pushButton.clicked.connect(
#             lambda: Commands.reverse_motor(0, self))
#         self.coreReverse_pushButton.clicked.connect(
#             lambda: Commands.reverse_motor(1, self))

#         self.snapshot_pushButton.clicked.connect(
#             lambda: Call_Thread.start_snapshot(self))
#         self.startImaging_pushButton.clicked.connect(
#             lambda: Call_Thread.start_timelapse(self))
#         self.preview_pushButton.clicked.connect(
#             lambda: Call_Thread.start_preview(self))

#         self.rotate_pushButton.clicked.connect(
#             lambda: Functions.rotate_image(self))


#         self.frame_verticalSlider.sliderReleased.connect(
#             lambda: Commands.slider_Released())
#         self.core_verticalSlider.sliderReleased.connect(
#             lambda: Commands.slider_Released())

#         self.sample_doubleSpinBox.valueChanged.connect(
#             lambda: Functions.sample_change(self))

#         self.link_pushButton.clicked.connect(lambda: UI_Update.link(self))

#         self.Start_spinBox.valueChanged.connect(
#             lambda: UI_Update.LED_validate(self))
#         self.End_spinBox.valueChanged.connect(
#             lambda: UI_Update.LED_validate(self))


#         self.log_pushButton.clicked.connect(
#             lambda: Functions.sensor_log(self))


#         self.title_lineEdit.textChanged.connect(
#             lambda: Functions.IST_Edit(self))
#         self.addDate_pushButton.clicked.connect(
#             lambda: Functions.add_date(self))

#         self.ICI_spinBox.valueChanged.connect(
#             lambda: Functions.ICI_Change(self))
#         self.ISD_spinBox.valueChanged.connect(
#             lambda: Functions.ISD_Change(self))
#         self.directory_pushButton.clicked.connect(
#             lambda: Functions.select_directory(self))

#         self.x_resolution_spinBox.valueChanged.connect(
#             lambda: Functions.camera_update(self))
#         self.y_resolution_spinBox.valueChanged.connect(
#             lambda: Functions.camera_update(self))

#         self.xAxis_horizontalSlider.valueChanged.connect(
#             lambda: Functions.camera_update(self))
#         self.xAxis_horizontalSlider.sliderReleased.connect(
#             lambda: Call_Thread.start_snapshot(self))

#         self.yAxis_horizontalSlider.valueChanged.connect(
#             lambda: Functions.camera_update(self))
#         self.yAxis_horizontalSlider.sliderReleased.connect(
#             lambda: Call_Thread.start_snapshot(self))

#         self.JPG_radioButton.toggled.connect(
#             lambda: Functions.update_mode(self))
#         self.infraredImaging_checkBox.stateChanged.connect(
#             lambda: Functions.IR_mode(self))

#         self.fanSpeed_horizontalSlider.sliderReleased.connect(
#             lambda: Functions.fanspeed_update(self))
#         self.fanSpeed_horizontalSlider.valueChanged.connect(
#             lambda: UI_Update.fanlabel_update(self))


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
