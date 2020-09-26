import Settings
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

        Settings.init()
        Call_Thread.sensor_init(self)
        Commands.init()

        self.Sensor_tabWidget.currentChanged.connect(
            lambda: Functions.printci(self))

        self.frameErgz_pushButton.clicked.connect(
            lambda: Commands.motor_toggle(0, self))
        self.coreErgz_pushButton.clicked.connect(
            lambda: Commands.motor_toggle(1, self))

        self.frameReverse_pushButton.clicked.connect(
            lambda: Commands.reverse_motor(0, self))
        self.coreReverse_pushButton.clicked.connect(
            lambda: Commands.reverse_motor(1, self))

        self.snapshot_pushButton.clicked.connect(
            lambda: Call_Thread.start_snapshot(self))
        self.startImaging_pushButton.clicked.connect(
            lambda: Call_Thread.start_timelapse(self))
        self.preview_pushButton.clicked.connect(
            lambda: Call_Thread.start_preview(self))

        self.rotate_pushButton.clicked.connect(
            lambda: Functions.rotate_image(self))

        self.confirmCycle_pushButton.clicked.connect(
            lambda: Call_Thread.start_cycle(self))
        self.powerCycle_spinBox.valueChanged.connect(
            lambda: Functions.Cycle_Change(self))

        self.frame_spinBox.valueChanged.connect(
            lambda: Commands.spin_change(0, self))
        self.core_spinBox.valueChanged.connect(
            lambda: Commands.spin_change(1, self))

        self.frame_verticalSlider.valueChanged.connect(
            lambda: Commands.slider_change(0, self))
        self.core_verticalSlider.valueChanged.connect(
            lambda: Commands.slider_change(1, self))

        self.frame_verticalSlider.sliderReleased.connect(
            lambda: Commands.slider_Released())
        self.core_verticalSlider.sliderReleased.connect(
            lambda: Commands.slider_Released())

        self.sample_doubleSpinBox.valueChanged.connect(
            lambda: Functions.sample_change(self))

        self.link_pushButton.clicked.connect(lambda: UI_Update.link(self))

        self.Start_spinBox.valueChanged.connect(
            lambda: UI_Update.LED_validate(self))
        self.End_spinBox.valueChanged.connect(
            lambda: UI_Update.LED_validate(self))

        self.IR_pushButton.clicked.connect(lambda: Commands.IR_toggle(self))

        self.log_pushButton.clicked.connect(
            lambda: Functions.sensor_log(self))

        self.light_Confirm_pushButton.clicked.connect(
            lambda: Commands.light_confirm(self))
        self.light_Reset_pushButton.clicked.connect(
            lambda: Commands.light_reset(self))

        self.title_lineEdit.textChanged.connect(
            lambda: Functions.IST_Edit(self))
        self.addDate_pushButton.clicked.connect(
            lambda: Functions.add_date(self))

        self.ICI_spinBox.valueChanged.connect(
            lambda: Functions.ICI_Change(self))
        self.ISD_spinBox.valueChanged.connect(
            lambda: Functions.ISD_Change(self))
        self.directory_pushButton.clicked.connect(
            lambda: Functions.select_directory(self))

        self.x_resolution_spinBox.valueChanged.connect(
            lambda: Functions.camera_update(self))
        self.y_resolution_spinBox.valueChanged.connect(
            lambda: Functions.camera_update(self))

        self.xAxis_horizontalSlider.valueChanged.connect(
            lambda: Functions.camera_update(self))
        self.xAxis_horizontalSlider.sliderReleased.connect(
            lambda: Call_Thread.start_snapshot(self))

        self.yAxis_horizontalSlider.valueChanged.connect(
            lambda: Functions.camera_update(self))
        self.yAxis_horizontalSlider.sliderReleased.connect(
            lambda: Call_Thread.start_snapshot(self))

        self.JPG_radioButton.toggled.connect(
            lambda: Functions.update_mode(self))
        self.infraredImaging_checkBox.stateChanged.connect(
            lambda: Functions.IR_mode(self))


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
