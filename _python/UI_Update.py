import General
import os
import Commands
import Functions
import subprocess
from PyQt5.QtGui import QImage, QPixmap

# ---------------------------------------------------------------------------- #
#                              system status check                             #
# ---------------------------------------------------------------------------- #


def system_status_check(self):
    self.main_update_status_pushButton.setEnabled(
        False)  # Disable update button
    # self.main_update_status_pushButton.repaint()

    # --------------------------- check core connection -------------------------- #
    if Functions.check_ip_connection(General.core_address):
        self.main_core_status_value_label.setPalette(General.palette_green)
        self.main_core_status_value_label.setText("Online")
    else:
        self.main_core_status_value_label.setPalette(General.palette_red)
        self.main_core_status_value_label.setText("Offline")
        self.main_image_label.setPixmap(
            QPixmap(General.camera_error_image))
    # --------------------------- check MCU connection --------------------------- #
    if Functions.check_i2c_device(General.MCU_address):
        self.main_MCU_status_value_label.setPalette(General.palette_green)
        self.main_MCU_status_value_label.setText("Online")
    else:
        self.main_MCU_status_value_label.setPalette(General.palette_red)
        self.main_MCU_status_value_label.setText("Offline")
        self.main_image_label.setPixmap(
            QPixmap(General.cummunication_error_image))
    # --------------------------- check ambient sensor connection ---------------- #
    if Functions.check_i2c_device(General.ambient_sensor_address):
        self.main_ambient_sensor_status_value_label.setPalette(
            General.palette_green)
        self.main_ambient_sensor_status_value_label.setText("Online")
        self.ambient_sensor_frame.setEnabled(True)
    else:
        self.main_ambient_sensor_status_value_label.setPalette(
            General.palette_red)
        self.main_ambient_sensor_status_value_label.setText("Offline")
        self.ambient_sensor_frame.setEnabled(False)
    # --------------------------- check motion sensor connection ----------------- #
    if Functions.check_i2c_device(General.motion_sensor_address):
        self.main_motion_sensor_status_value_label.setPalette(
            General.palette_green)
        self.main_motion_sensor_status_value_label.setText("Online")
        self.motion_sensor_frame.setEnabled(True)
    else:
        self.main_motion_sensor_status_value_label.setPalette(
            General.palette_red)
        self.main_motion_sensor_status_value_label.setText("Offline")
        self.motion_sensor_frame.setEnabled(False)
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
#                               repo branch check                              #
# ---------------------------------------------------------------------------- #


def repo_branch_check(self):
    branch_name = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode('UTF-8')
    print(branch_name)
    # Set window title
    self.setWindowTitle(f"Clinostat Control Center - {branch_name}")

# ---------------------------------------------------------------------------- #
#                                graph UI setup                                #
# ---------------------------------------------------------------------------- #


def graph_setup(self):
    self.ambient_temperature_graphWidget.setBackground("#fbfbfb")
    self.ambient_temperature_graphWidget.showGrid(x=True, y=True)
    self.ambient_temperature_graphWidget.setLabel(
        "left", "Temperature (°C)", **General.styles)
    self.ambient_temperature_graphWidget.setLabel(
        "bottom", "Time (s)", **General.styles)

    self.ambient_humidity_graphWidget.setBackground("#fbfbfb")
    self.ambient_humidity_graphWidget.showGrid(x=True, y=True)
    self.ambient_humidity_graphWidget.setLabel(
        "left", "Humidity (%)", **General.styles)
    self.ambient_humidity_graphWidget.setLabel(
        "bottom", "Time (s)", **General.styles)

    self.ambient_pressure_graphWidget.setBackground("#fbfbfb")
    self.ambient_pressure_graphWidget.showGrid(x=True, y=True)
    self.ambient_pressure_graphWidget.setLabel(
        "left", "Pressure (hPa)", **General.styles)
    self.ambient_pressure_graphWidget.setLabel(
        "bottom", "Time (s)", **General.styles)

    self.motion_accelerometer_graphWidget.setBackground("#fbfbfb")
    self.motion_accelerometer_graphWidget.showGrid(x=True, y=True)
    self.motion_accelerometer_graphWidget.setLabel(
        "left", "Acceleration (m/s^2)", **General.styles)
    self.motion_accelerometer_graphWidget.setLabel(
        "bottom", "Time (s)", **General.styles)

    self.motion_gyroscope_graphWidget.setBackground("#fbfbfb")
    self.motion_gyroscope_graphWidget.showGrid(x=True, y=True)
    self.motion_gyroscope_graphWidget.setLabel(
        "left", "Speed (degrees/s)", **General.styles)
    self.motion_gyroscope_graphWidget.setLabel(
        "bottom", "Time (s)", **General.styles)

# ---------------------------------------------------------------------------- #
#                           lighting UI updates                                #
# ---------------------------------------------------------------------------- #


def lighting_source_update(self):
    Commands.lighting_reset()
    General.commands_list.clear()
    self.lighting_brightness_value_spinBox.setValue(50)

    self.lighting_red_value_spinBox.setValue(100)
    self.lighting_green_value_spinBox.setValue(0)
    self.lighting_blue_value_spinBox.setValue(0)
    self.lighting_white_value_spinBox.setValue(0)

    if self.lighting_source_tabWidget.currentIndex() == 0:
        self.lighting_start_LED_value_spinBox.setMaximum(89)
        self.lighting_end_LED_value_spinBox.setMaximum(90)

        self.lighting_start_LED_value_spinBox.setValue(1)
        self.lighting_end_LED_value_spinBox.setValue(90)

        self.lighting_LED_settings_text_label.setText(
            "<html><head/><body><p align="'center'"><span style="' font-weight:700;'">LED Settings: [1,90]</span></p></body></html>")
    else:
        self.lighting_start_LED_value_spinBox.setMaximum(39)
        self.lighting_end_LED_value_spinBox.setMaximum(40)

        self.lighting_start_LED_value_spinBox.setValue(1)
        self.lighting_end_LED_value_spinBox.setValue(40)

        self.lighting_LED_settings_text_label.setText(
            "<html><head/><body><p align="'center'"><span style="' font-weight:700;'">LED Settings: [1,40]</span></p></body></html>")


def IR_lighting_update(self):
    if not General.IR_stat:
        self.lighting_IR_toggle_pushButton.setText("IR STATUS:ON")
        CMD = "4~1"
    else:
        self.lighting_IR_toggle_pushButton.setText("IR STATUS:OFF")
        CMD = "4~0"
    General.IR_stat = not General.IR_stat
    Commands.IR_toggle()


# ---------------------------------------------------------------------------- #
#                               motor UI updates                               #
# ---------------------------------------------------------------------------- #

def link_update(self):
    if General.motors_linked:
        self.motion_link_toggle_pushButton.setIcon(General.broken)
    else:
        self.motion_link_toggle_pushButton.setIcon(General.linked)
    General.motors_linked = not General.motors_linked


def motor_enable(self, mode):
    if General.motors_linked:
        if mode:
            General.frame_enabled = not General.frame_enabled
            General.core_enabled = General.frame_enabled
        else:
            General.core_enabled = not General.core_enabled
            General.frame_enabled = General.core_enabled
    else:
        if mode:
            General.frame_enabled = not General.frame_enabled
        else:
            General.core_enabled = not General.core_enabled
    if General.frame_enabled:
        self.motion_frame_motor_enable_pushButton.setText("DISABLE MOTOR")
    else:
        self.motion_frame_motor_enable_pushButton.setText("ENABLE MOTOR")

    if General.core_enabled:
        self.motion_core_motor_enable_pushButton.setText("DISABLE MOTOR")
    else:
        self.motion_core_motor_enable_pushButton.setText("ENABLE MOTOR")
    Commands.motor_enable()


def reverse_motor(frame_motor, self):

    if General.motors_linked:
        if frame_motor:
            General.frame_direction *= -1
            General.core_direction = General.frame_direction
        else:
            General.core_direction *= -1
            General.frame_direction = General.core_direction
    else:
        if frame_motor:
            General.frame_direction *= -1
        else:
            General.core_direction *= -1

    if General.frame_direction == 1:
        self.motion_frame_motor_reverse_pushButton.setIcon(General.clockwise)
    else:
        self.motion_frame_motor_reverse_pushButton.setIcon(
            General.counter_clockwise)

    if General.core_direction == 1:
        self.motion_core_motor_reverse_pushButton.setIcon(General.clockwise)
    else:
        self.motion_core_motor_reverse_pushButton.setIcon(
            General.counter_clockwise)
    Functions.calculate_speed()


def motor_spinbox_changed(self, mode):

    block_motor_signals(self)
    if General.motors_linked:
        if mode:
            General.frame_RPM = round(
                self.motion_frame_motor_value_spinBox.value(), 2)
            General.core_RPM = General.frame_RPM

            self.motion_frame_motor_value_verticalSlider.setValue(
                General.frame_RPM * 100)
            self.motion_core_motor_value_verticalSlider.setValue(
                General.core_RPM * 100)

            self.motion_core_motor_value_spinBox.setValue(General.core_RPM)

        else:
            General.core_RPM = round(
                self.motion_core_motor_value_spinBox.value(), 2)
            General.frame_RPM = General.core_RPM

            self.motion_frame_motor_value_verticalSlider.setValue(
                General.frame_RPM * 100)
            self.motion_core_motor_value_verticalSlider.setValue(
                General.core_RPM * 100)

            self.motion_frame_motor_value_spinBox.setValue(General.frame_RPM)
    else:
        if mode:
            General.frame_RPM = round(
                self.motion_frame_motor_value_spinBox.value(), 2)
            self.motion_frame_motor_value_verticalSlider.setValue(
                General.frame_RPM * 100)
        else:
            General.core_RPM = round(
                self.motion_core_motor_value_spinBox.value(), 2)
            self.motion_core_motor_value_verticalSlider.setValue(
                General.core_RPM * 100)

    unblock_motor_signals(self)
    Functions.calculate_speed()


def motor_slider_change(self, mode):

    block_motor_signals(self)
    if General.motors_linked:
        if mode:
            General.frame_RPM = self.motion_frame_motor_value_verticalSlider.sliderPosition() / \
                100
            General.core_RPM = General.frame_RPM
            self.motion_core_motor_value_verticalSlider.setValue(
                General.core_RPM * 100)

        else:
            General.core_RPM = self.motion_core_motor_value_verticalSlider.sliderPosition() / \
                100
            General.frame_RPM = General.core_RPM
            self.motion_frame_motor_value_verticalSlider.setValue(
                General.frame_RPM * 100)
        self.motion_frame_motor_value_spinBox.setValue(General.frame_RPM)
        self.motion_core_motor_value_spinBox.setValue(General.core_RPM)
    else:
        if mode:
            General.frame_RPM = self.motion_frame_motor_value_verticalSlider.sliderPosition() / \
                100
            self.motion_frame_motor_value_spinBox.setValue(General.frame_RPM)
        else:
            General.core_RPM = self.motion_core_motor_value_verticalSlider.sliderPosition() / \
                100
            self.motion_core_motor_value_spinBox.setValue(General.core_RPM)
    unblock_motor_signals(self)


def block_motor_signals(self):
    self.motion_frame_motor_value_spinBox.blockSignals(True)
    self.motion_core_motor_value_spinBox.blockSignals(True)
    self.motion_frame_motor_value_verticalSlider.blockSignals(True)
    self.motion_core_motor_value_verticalSlider.blockSignals(True)


def unblock_motor_signals(self):
    self.motion_frame_motor_value_spinBox.blockSignals(False)
    self.motion_core_motor_value_spinBox.blockSignals(False)
    self.motion_frame_motor_value_verticalSlider.blockSignals(False)
    self.motion_core_motor_value_verticalSlider.blockSignals(False)


# ---------------------------------------------------------------------------- #
#                              imaging UI updates                              #
# ---------------------------------------------------------------------------- #
def imaging_UI_update(self):
    imaging_settings_update(self)
    if General.imaging_total > 0 and len(General.sequence_name) != 0:
        self.main_start_timelapse_pushButton.setEnabled(True)
    else:
        self.main_start_timelapse_pushButton.setEnabled(False)
    self.imaging_progress_value_label.setText(
        "Progress: " + str(General.imaging_current_count) + "/" + str(General.imaging_total))
    self.imaging_progress_progressBar.setMaximum(General.imaging_total)

    if General.date not in General.sequence_name:
        self.imaging_add_date_pushButton.setEnabled(True)
    else:
        self.imaging_add_date_pushButton.setEnabled(False)

    if len(General.sequence_name) == 0:
        self.imaging_add_date_pushButton.setEnabled(False)

    if General.custom_directory == None:
        General.full_directory = General.default_directory + "/" + General.sequence_name
    else:
        General.full_directory = General.custom_directory + "/" + General.sequence_name
    self.imaging_directory_value_label.setText(General.full_directory)


def imaging_settings_update(self):
    General.sequence_name = self.imaging_image_sequence_title_value_lineEdit.text()
    General.imaging_interval = self.imaging_image_capture_interval_value_spinBox.value()
    General.imaging_duration = self.imaging_image_sequence_duration_value_spinBox.value()
    General.imaging_total = int(
        General.imaging_duration / General.imaging_interval)
    General.x_resolution = str(
        self.imaging_x_resolution_value_spinBox.value())
    General.y_resolution = str(
        self.imaging_y_resolution_value_spinBox.value())

    General.digital_zoom = str(
        self.imaging_digital_zoom_horizontalSlider.value())
    General.imaging_format = int(self.imaging_JPG_radioButton.isChecked())
    General.IR_imaging = self.lighting_automatic_IR_imaging_checkBox.isChecked()


def image_sequence_title_add_date(self):
    General.sequence_name = General.sequence_name + "_" + General.date
    self.imaging_image_sequence_title_value_lineEdit.setText(
        General.sequence_name)


def imaging_UI_toggle(self):
    if General.core_busy:
        self.main_imaging_frame.setEnabled(False)
        self.imaging_settings_frame.setEnabled(False)
        self.timelapse_setup_frame.setEnabled(False)

    else:
        self.main_imaging_frame.setEnabled(True)
        self.imaging_settings_frame.setEnabled(True)
        self.timelapse_setup_frame.setEnabled(True)
        system_status_check(self)


def transmit_update(self):
    General.received_packets += 1
    self.main_core_status_value_label.setText(str(General.received_packets))


def digital_zoom_update(self):
    self.imaging_digital_zoom_value_label.setText(
        str(self.imaging_digital_zoom_horizontalSlider.value())+" %")


def timelapse_toggle(self, mode):
    if mode:
        General.timelapse_thread_running = True
        self.main_start_timelapse_pushButton.setText("TERMINATE TIMELAPSE")
    else:
        self.main_start_timelapse_pushButton.setText("START TIMELAPSE")


def timelapse_capture_toggle(self, mode):
    if mode:
        General.core_busy = True
        imaging_settings_update(self)

    else:
        General.core_busy = False
        capture_img = QImage(General.current_image)
        self.main_image_label.setPixmap(QPixmap(capture_img))
        General.received_packets = 0

        self.imaging_progress_value_label.setText(
            "Progress: " + str(General.imaging_current_count) + "/" + str(General.imaging_total))
        self.imaging_progress_progressBar.setValue(
            General.imaging_current_count)

    imaging_UI_toggle(self)


def image_capture_toggle(self, mode):
    if mode:
        if General.capture_mode < 3:
            self.main_core_status_value_label.setText("Focusing...")
        General.core_busy = True
        imaging_settings_update(self)
    else:
        if General.capture_mode < 3:
            self.main_autofocus_pushButton.setText(General.lens_position)
        if General.capture_mode == 4:
            os.system("gpicview " + General.current_image)
        snap_img = QImage(General.current_image)
        self.main_image_label.setPixmap(QPixmap(snap_img))
        General.core_busy = False
        General.received_packets = 0

        if General.lens_position != "∞":
            self.main_increase_focus_pushButton.setEnabled(True)
            self.main_decrease_focus_pushButton.setEnabled(True)
    imaging_UI_toggle(self)


def timelapse_countdown(self):
    self.imaging_countdown_value_label.setText(
        "Next Image: "+str(General.timelapse_countdown)+" s")

# ---------------------------------------------------------------------------- #
#                         power cycle thread UI updates                        #
# ---------------------------------------------------------------------------- #


def cycle_start(self):
    self.lighting_confirm_cycle_pushButton.setText("TERMINATE CYCLE")
    General.cycle_thread_running = True


def cycle_end(self):
    self.lighting_confirm_cycle_pushButton.setText("CONFIRM CYCLE")
    General.cycle_thread_running = False


def cycle_countdown(self):
    self.lighting_confirm_cycle_pushButton.setText(
        "TERMINATE CYCLE: " + str(General.cycle_countdown) + " s")


# ---------------------------------------------------------------------------- #
#                          ambient graphing UI updates                         #
# ---------------------------------------------------------------------------- #


def ambient_UI_toggle(self):
    if General.ambient_thread_running:
        self.ambient_start_sensors_pushButton.setText("Stop Ambient Sensors")
        self.ambient_sensor_rate_value_spinBox.setEnabled(False)
        General.ambient_sensor_interval = 60 / \
            self.ambient_sensor_rate_value_spinBox.value()

    else:
        self.ambient_start_sensors_pushButton.setText("Start Ambient Sensors")
        self.ambient_temperture_value_label.setText("N/A °C")
        self.ambient_humidity_value_label.setText("N/A %")
        self.ambient_pressure_value_label.setText("N/A hPa")
        self.ambient_sensor_rate_value_spinBox.setEnabled(True)


def ambient_sensor_initialize(self):
    General.ambient_temperature_graph_ref = self.ambient_temperature_graphWidget.plot(
        General.ambient_sensor_time_stamp, General.ambient_temperature, pen=General.red_pen
    )
    General.ambient_humidity_graph_ref = self.ambient_humidity_graphWidget.plot(
        General.ambient_sensor_time_stamp, General.ambient_humidity, pen=General.red_pen
    )
    General.ambient_pressure_graph_ref = self.ambient_pressure_graphWidget.plot(
        General.ambient_sensor_time_stamp, General.ambient_pressure, pen=General.red_pen
    )


def ambient_sensor_reset(self):
    self.ambient_temperature_graphWidget.clear()
    self.ambient_humidity_graphWidget.clear()
    self.ambient_pressure_graphWidget.clear()

    General.ambient_temperature = []
    General.ambient_humidity = []
    General.ambient_pressure = []

    General.ambient_sensor_time_stamp = []


def ambient_sensor_update(self):
    ambient_sensor_graph_update(self)
    ambient_update_labels(self)


def ambient_sensor_graph_update(self):
    if len(General.ambient_sensor_time_stamp) > 1:
        if self.main_tabWidget.currentIndex() == 3:

            if self.ambient_sensors_tabWidget.currentIndex() == 0:
                General.ambient_temperature_graph_ref.setData(
                    General.ambient_sensor_time_stamp, General.ambient_temperature
                )
            elif self.ambient_sensors_tabWidget.currentIndex() == 1:
                General.ambient_humidity_graph_ref.setData(
                    General.ambient_sensor_time_stamp, General.ambient_humidity
                )
            elif self.ambient_sensors_tabWidget.currentIndex() == 2:
                General.ambient_pressure_graph_ref.setData(
                    General.ambient_sensor_time_stamp, General.ambient_pressure
                )
    General.ambient_graphing_complete = True


def ambient_update_labels(self):
    self.ambient_temperture_value_label.setText(
        str(General.ambient_temperature[-1]) + " °C"
    )
    self.ambient_humidity_value_label.setText(
        str(General.ambient_humidity[-1]) + " %")
    self.ambient_pressure_value_label.setText(
        str(General.ambient_pressure[-1]) + " hPa")


def export_UI_update(self, mode):
    if mode == 0:
        self.ambient_sensor_export_CSV_pushButton.setText("Exporting...")
        self.ambient_sensor_export_CSV_pushButton.setEnabled(False)
    elif mode == 1:
        self.ambient_sensor_export_CSV_pushButton.setText("Export Complete")
        self.ambient_sensor_export_CSV_pushButton.setEnabled(True)
    elif mode == 2:
        self.motion_sensor_export_CSV_pushButton.setText("Exporting...")
        self.motion_sensor_export_CSV_pushButton.setEnabled(False)
    elif mode == 3:
        self.motion_sensor_export_CSV_pushButton.setText("Export Complete")
        self.motion_sensor_export_CSV_pushButton.setEnabled(True)


# ---------------------------------------------------------------------------- #
#                          motion graphing UI updates                          #
# ---------------------------------------------------------------------------- #
def motion_UI_toggle(self):
    if General.motion_thread_running:
        self.motion_start_sensors_pushButton.setText("Stop Motion Sensors")
        self.motion_sensor_rate_value_spinBox.setEnabled(False)
        General.motion_sensor_interval = 60 / \
            self.motion_sensor_rate_value_spinBox.value()

    else:
        self.motion_start_sensors_pushButton.setText("Start Motion Sensors")
        self.motion_x_axis_value_label.setText("N/A")
        self.motion_x_axis_value_label.setText("N/A")
        self.motion_x_axis_value_label.setText("N/A")
        self.motion_sensor_rate_value_spinBox.setEnabled(True)


def motion_sensor_initialize(self):
    General.motion_accelerometer_x_graph_ref = self.motion_accelerometer_graphWidget.plot(
        General.motion_sensor_graph_time_stamp, General.motion_acceleration_graph_x, pen=General.red_pen
    )

    General.motion_accelerometer_y_graph_ref = self.motion_accelerometer_graphWidget.plot(
        General.motion_sensor_graph_time_stamp, General.motion_acceleration_graph_y, pen=General.green_pen
    )

    General.motion_accelerometer_z_graph_ref = self.motion_accelerometer_graphWidget.plot(
        General.motion_sensor_graph_time_stamp, General.motion_acceleration_graph_z, pen=General.blue_pen
    )

    General.motion_gyroscope_x_graph_ref = self.motion_gyroscope_graphWidget.plot(
        General.motion_sensor_graph_time_stamp, General.motion_gyroscope_graph_x, pen=General.red_pen
    )

    General.motion_gyroscope_y_graph_ref = self.motion_gyroscope_graphWidget.plot(
        General.motion_sensor_graph_time_stamp, General.motion_gyroscope_graph_y, pen=General.green_pen
    )

    General.motion_gyroscope_z_graph_ref = self.motion_gyroscope_graphWidget.plot(
        General.motion_sensor_graph_time_stamp, General.motion_gyroscope_graph_z, pen=General.blue_pen
    )


def motion_sensor_reset(self):
    self.motion_accelerometer_graphWidget.clear()
    self.motion_gyroscope_graphWidget.clear()

    General.motion_acceleration_x = []
    General.motion_acceleration_y = []
    General.motion_acceleration_z = []

    General.motion_gyroscope_x = []
    General.motion_gyroscope_y = []
    General.motion_gyroscope_z = []

    General.motion_sensor_time_stamp = []


def motion_sensor_update(self):
    motion_sensor_graph_update(self)


def motion_sensor_graph_update(self):
    if self.main_tabWidget.currentIndex() == 4:
        if self.motion_sensors_tabWidget.currentIndex() == 0:
            self.x_axis_units_text_label.setText(
                "<html><head/><body><p><span style="" font-weight:700;"">m/s</span><span style="" font-weight:700; vertical-align:super;"">2</span></p></body></html"">")
            self.y_axis_units_text_label.setText(
                "<html><head/><body><p><span style="" font-weight:700;"">m/s</span><span style="" font-weight:700; vertical-align:super;"">2</span></p></body></html"">")
            self.z_axis_units_text_label.setText(
                "<html><head/><body><p><span style="" font-weight:700;"">m/s</span><span style="" font-weight:700; vertical-align:super;"">2</span></p></body></html"">")
        else:
            self.x_axis_units_text_label.setText(
                "<html><head/><body><p><span style="" font-weight:700;"">degrees/s</span></p></body></html>")
            self.y_axis_units_text_label.setText(
                "<html><head/><body><p><span style="" font-weight:700;"">degrees/s</span></p></body></html>")
            self.z_axis_units_text_label.setText(
                "<html><head/><body><p><span style="" font-weight:700;"">degrees/s</span></p></body></html>")

    if len(General.motion_sensor_time_stamp) > 1:
        if self.main_tabWidget.currentIndex() == 4:

            if self.motion_sensors_tabWidget.currentIndex() == 0:

                self.motion_x_axis_value_label.setText(
                    str(General.motion_acceleration_x[-1]))
                self.motion_y_axis_value_label.setText(
                    str(General.motion_acceleration_y[-1]))
                self.motion_z_axis_value_label.setText(
                    str(General.motion_acceleration_z[-1]))

                General.motion_accelerometer_x_graph_ref.setData(
                    General.motion_sensor_graph_time_stamp, General.motion_acceleration_graph_x
                )
                General.motion_accelerometer_y_graph_ref.setData(
                    General.motion_sensor_graph_time_stamp, General.motion_acceleration_graph_y
                )

                General.motion_accelerometer_z_graph_ref.setData(
                    General.motion_sensor_graph_time_stamp, General.motion_acceleration_graph_z
                )
            else:
                self.motion_x_axis_value_label.setText(
                    str(General.motion_gyroscope_x[-1]))
                self.motion_y_axis_value_label.setText(
                    str(General.motion_gyroscope_y[-1]))
                self.motion_z_axis_value_label.setText(
                    str(General.motion_gyroscope_z[-1]))
                General.motion_gyroscope_x_graph_ref.setData(
                    General.motion_sensor_graph_time_stamp, General.motion_gyroscope_graph_x
                )

                General.motion_gyroscope_y_graph_ref.setData(
                    General.motion_sensor_graph_time_stamp, General.motion_gyroscope_graph_y
                )

                General.motion_gyroscope_z_graph_ref.setData(
                    General.motion_sensor_graph_time_stamp, General.motion_gyroscope_graph_z
                )
            General.motion_graphing_complete = True

# ---------------------------------------------------------------------------- #
#                              lighting UI updates                             #
# ---------------------------------------------------------------------------- #


def LED_validate(self):
    if self.lighting_start_LED_value_spinBox.value() >= self.lighting_end_LED_value_spinBox.value():
        self.lighting_LED_confirm_pushButton.setEnabled(False)
    else:
        self.lighting_LED_confirm_pushButton.setEnabled(True)


def fanlabel_update(self, mode):
    if mode:
        self.lighting_core_fan_speed_value_label.setText(
            "Speed: " + str(self.lighting_core_fan_speed_horizontalSlider.sliderPosition()) + "%")
    else:
        self.lighting_controller_fan_speed_value_label.setText(
            "Speed: " + str(self.lighting_controller_fan_speed_horizontalSlider.sliderPosition()) + "%")
