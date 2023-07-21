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
        UI_Update.graph_setup(self)
        Commands.reset_MCU()
        General.initialize_icons()
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
        self.motion_frame_motor_enable_pushButton.clicked.connect(
            lambda: UI_Update.motor_enable(1, self))
        self.motion_core_motor_enable_pushButton.clicked.connect(
            lambda: UI_Update.motor_enable(0, self))

        self.motion_link_toggle_pushButton.clicked.connect(
            lambda: UI_Update.link_update(self))

        self.motion_frame_motor_value_spinBox.valueChanged.connect(
            lambda: UI_Update.motor_spinbox_changed(1, self))
        self.motion_core_motor_value_spinBox.valueChanged.connect(
            lambda: UI_Update.motor_spinbox_changed(0, self))

        self.motion_frame_motor_value_verticalSlider.valueChanged.connect(
            lambda: UI_Update.motor_slider_change(1, self))
        self.motion_core_motor_value_verticalSlider.valueChanged.connect(
            lambda: UI_Update.motor_slider_change(0, self))

        self.motion_frame_motor_value_verticalSlider.sliderReleased.connect(
            lambda: Functions.calculate_speed())
        self.motion_core_motor_value_verticalSlider.sliderReleased.connect(
            lambda: Functions.calculate_speed())

        self.motion_frame_motor_reverse_pushButton.clicked.connect(
            lambda: UI_Update.reverse_motor(1, self))
        self.motion_core_motor_reverse_pushButton.clicked.connect(
            lambda: UI_Update.reverse_motor(0, self))

# ---------------------------------------------------------------------------- #
#                                imaging signals                               #
# ---------------------------------------------------------------------------- #

        self.imaging_image_sequence_title_value_lineEdit.textChanged.connect(
            lambda: UI_Update.imaging_UI_update(self))
        self.imaging_add_date_pushButton.clicked.connect(
            lambda: UI_Update.image_sequence_title_add_date(self))

        self.imaging_image_capture_interval_value_spinBox.valueChanged.connect(
            lambda: UI_Update.imaging_UI_update(self))
        self.imaging_image_sequence_duration_value_spinBox.valueChanged.connect(
            lambda: UI_Update.imaging_UI_update(self))
        self.imaging_select_directory_pushButton.clicked.connect(
            lambda: Functions.select_directory(self))

        self.main_autofocus_pushButton.clicked.connect(
            lambda: Call_Thread.start_capture(self, 0))
        self.main_increase_focus_pushButton.clicked.connect(
            lambda: Call_Thread.start_capture(self, 1))
        self.main_decrease_focus_pushButton.clicked.connect(
            lambda: Call_Thread.start_capture(self, 2))
        self.main_snapshot_pushButton.clicked.connect(
            lambda: Call_Thread.start_capture(self, 3))

        self.imaging_digital_zoom_horizontalSlider.valueChanged.connect(
            lambda: UI_Update.digital_zoom_update(self))

        self.main_preview_pushButton.clicked.connect(
            lambda: Call_Thread.start_capture(self, 4))
# ---------------------------------------------------------------------------- #
#                            ambient sensor signals                            #
# ---------------------------------------------------------------------------- #
        self.ambient_sensors_tabWidget.currentChanged.connect(
            lambda: UI_Update.ambient_sensor_graph_update(self))

        self.main_tabWidget.currentChanged.connect(
            lambda: UI_Update.ambient_sensor_graph_update(self))

        self.ambient_start_sensors_pushButton.clicked.connect(
            lambda: Call_Thread.ambient_sensors(self))

        self.ambient_confirm_temperature_offset_pushButton.clicked.connect(
            lambda: Functions.ambient_sensor_temperature_offset(self)
        )

        self.ambient_confirm_humidity_offset_pushButton.clicked.connect(
            lambda: Functions.ambient_sensor_humidity_offset(self)
        )

        self.ambient_confirm_pressure_offset_pushButton.clicked.connect(
            lambda: Functions.ambient_sensor_pressure_offset(self)
        )

        self.ambient_export_sensor_CSV_pushButton.clicked.connect(
            lambda: Functions.sensor_export_data(self)
        )

# ---------------------------------------------------------------------------- #
#                             motion sensor signals                            #
# ---------------------------------------------------------------------------- #
        self.motion_sensors_tabWidget.currentChanged.connect(
            lambda: UI_Update.motion_sensor_graph_update(self))
        self.motion_start_sensors_pushButton.clicked.connect(
            lambda: Call_Thread.motion_sensors(self))


#         Call_Thread.sensor_init(self)
#         Commands.init()

#         self.Sensor_tabWidget.currentChanged.connect(
#             lambda: Functions.printci(self))

#         self.startImaging_pushButton.clicked.connect(
#             lambda: Call_Thread.start_timelapse(self))
#         self.preview_pushButton.clicked.connect(
#             lambda: Call_Thread.start_preview(self))

#         self.rotate_pushButton.clicked.connect(
#             lambda: Functions.rotate_image(self))

#         self.sample_doubleSpinBox.valueChanged.connect(
#             lambda: Functions.sample_change(self))


#         self.Start_spinBox.valueChanged.connect(
#             lambda: UI_Update.LED_validate(self))
#         self.End_spinBox.valueChanged.connect(
#             lambda: UI_Update.LED_validate(self))


#         self.log_pushButton.clicked.connect(
#             lambda: Functions.sensor_log(self))


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
