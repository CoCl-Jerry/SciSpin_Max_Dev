import General
import Commands
import UI_Update
import Functions
import Call_Thread

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
        UI_Update.repo_branch_check(self)
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
        self.lighting_start_LED_value_spinBox.valueChanged.connect(
            lambda: UI_Update.LED_validate(self))
        self.lighting_end_LED_value_spinBox.valueChanged.connect(
            lambda: UI_Update.LED_validate(self))

# --------------------------- Power cycle signals ---------------------------- #
        self.lighting_confirm_cycle_pushButton.clicked.connect(
            lambda: Call_Thread.start_cycle(self))

# -------------------------- IR LED lighting signals ------------------------- #
        self.lighting_IR_toggle_pushButton.clicked.connect(
            lambda: UI_Update.IR_lighting_update(self))

# ------------------------------- motor signals ------------------------------ #
        self.motion_frame_motor_enable_pushButton.clicked.connect(
            lambda: UI_Update.motor_enable(self, 1))
        self.motion_core_motor_enable_pushButton.clicked.connect(
            lambda: UI_Update.motor_enable(self, 0))

        self.motion_link_toggle_pushButton.clicked.connect(
            lambda: UI_Update.link_update(self))

        self.motion_frame_motor_value_spinBox.valueChanged.connect(
            lambda: UI_Update.motor_spinbox_changed(self, 1))
        self.motion_core_motor_value_spinBox.valueChanged.connect(
            lambda: UI_Update.motor_spinbox_changed(self, 0))

        self.motion_frame_motor_value_verticalSlider.valueChanged.connect(
            lambda: UI_Update.motor_slider_change(self, 1))
        self.motion_core_motor_value_verticalSlider.valueChanged.connect(
            lambda: UI_Update.motor_slider_change(self, 0))

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

        self.main_start_timelapse_pushButton.clicked.connect(
            lambda: Call_Thread.start_timelapse(self))

        self.main_autofocus_pushButton.clicked.connect(
            lambda: Call_Thread.start_capture(self, 0))
        self.main_increase_focus_pushButton.clicked.connect(
            lambda: Call_Thread.start_capture(self, 1))
        self.main_decrease_focus_pushButton.clicked.connect(
            lambda: Call_Thread.start_capture(self, 2))
        self.main_snapshot_pushButton.clicked.connect(
            lambda: Call_Thread.start_capture(self, 3))
        self.main_preview_pushButton.clicked.connect(
            lambda: Call_Thread.start_capture(self, 4))

        self.imaging_digital_zoom_horizontalSlider.valueChanged.connect(
            lambda: UI_Update.digital_zoom_update(self))
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

        self.ambient_sensor_export_CSV_pushButton.clicked.connect(
            lambda: Functions.sensor_export_data(self)
        )

# ---------------------------------------------------------------------------- #
#                             motion sensor signals                            #
# ---------------------------------------------------------------------------- #
        self.motion_sensors_tabWidget.currentChanged.connect(
            lambda: UI_Update.motion_sensor_graph_update(self))
        self.motion_start_sensors_pushButton.clicked.connect(
            lambda: Call_Thread.motion_sensors(self))

        self.motion_sensor_export_CSV_pushButton.clicked.connect(
            lambda: Functions.sensor_export_data(self)
        )

# ---------------------------------------------------------------------------- #
#                              fan control signals                             #
# ---------------------------------------------------------------------------- #

        self.lighting_core_fan_speed_horizontalSlider.sliderReleased.connect(
            lambda: Functions.fanspeed_update(self, 1))
        self.lighting_controller_fan_speed_horizontalSlider.sliderReleased.connect(
            lambda: Functions.fanspeed_update(self, 0))

        self.lighting_core_fan_speed_horizontalSlider.valueChanged.connect(
            lambda: UI_Update.fanlabel_update(self, 1))
        self.lighting_controller_fan_speed_horizontalSlider.valueChanged.connect(
            lambda: UI_Update.fanlabel_update(self, 0))


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
