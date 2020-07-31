import Settings
import Commands
import UI_Update
import timeit

import PyQt5
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


def rotate_image():
    Settings.rotation += 1
    self.start_snapshot(self)


def IST_Edit(self):
    Settings.sequence_name = self.title_lineEdit.text()
    Settings.full_dir = Settings.default_dir + "/" + Settings.sequence_name
    self.directory_label.setText(Settings.full_dir)

    if Settings.date not in Settings.sequence_name:
        self.addDate_pushButton.setEnabled(True)
    if(len(Settings.sequence_name) == 0):
        self.addDate_pushButton.setEnabled(False)
    UI_Update.validate_input(self)


def add_date(self):
    Settings.sequence_name = Settings.sequence_name + "_" + Settings.date
    self.title_lineEdit.setText(Settings.sequence_name)
    Settings.full_dir = Settings.default_dir + "/" + Settings.sequence_name
    self.directory_label.setText(Settings.full_dir)
    self.addDate_pushButton.setEnabled(False)


def ICI_Change(self):
    Settings.interval = self.ICI_spinBox.value()
    UI_Update.validate_input(self)


def Cycle_Change(self):
    Settings.cycle_time = self.powerCycle_spinBox.value()


def ISD_Change(self):
    Settings.duration = self.ISD_spinBox.value()
    UI_Update.validate_input(self)


def select_directory(self):
    m_directory = str(QFileDialog.getExistingDirectory(
        self, "Select Directory", '/media/pi'))
    if(len(m_directory) != 0):
        Settings.full_dir = m_directory + "/" + Settings.sequence_name
        self.directory_label.setText(Settings.full_dir)
    UI_Update.validate_input(self)


def camera_update(self):
    Settings.AOI_X = self.xAxis_horizontalSlider.sliderPosition() / 100
    Settings.AOI_Y = self.xAxis_horizontalSlider.sliderPosition() / 100
    Settings.AOI_W = self.yAxis_horizontalSlider.sliderPosition() / 100
    Settings.AOI_H = self.yAxis_horizontalSlider.sliderPosition() / 100

    Settings.x_resolution = self.x_resolution_spinBox.value()
    Settings.y_resolution = self.y_resolution_spinBox.value()

    formatted_x = "{:.2f}".format(
        self.xAxis_horizontalSlider.sliderPosition() / 100)
    formatted_y = "{:.2f}".format(
        self.yAxis_horizontalSlider.sliderPosition() / 100)
    self.xAxis_label.setText(
        "Zoom Axis A: " + formatted_x)
    self.yAxis_label.setText(
        "Zoom Axis B: " + formatted_y)


def update_mode(self):
    Settings.imaging_mode = self.JPG_radioButton.isChecked()


def IR_mode(self):
    Settings.IR_imaging = self.infraredImaging_checkBox.isChecked()


def printci(self):
    Settings.tag_index = self.Sensor_tabWidget.currentIndex()


def sample_change(self):
    Settings.sample_time = self.sample_doubleSpinBox.value()


def frame_slider_select(self):
    if(Settings.LINKED):
        Commands.linked_slider_change(self)
    else:
        Commands.frame_slider_change(self)


def core_slider_select(self):
    if(Settings.LINKED):
        Commands.linked_slider_change(self)
    else:
        Commands.core_slider_change(self)


def frame_spin_select(self):
    if(Settings.LINKED):
        Commands.linked_spin_change(self)
    else:
        Commands.frame_spin_select(self)


def core_spin_select(self):
    if(Settings.LINKED):
        Commands.linked_spin_change(self)
    else:
        Commands.core_spin_select(self)


def sensor_log(self):
    Settings.log_start_time = timeit.default_timer()
    Settings.log_sensor = True
    Settings.log_duration = self.log_spinBox.value() * 60
