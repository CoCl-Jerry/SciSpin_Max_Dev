import General
import Commands
import UI_Update
import socket
import psutil
import subprocess
import smbus
import csv

from PyQt5.QtWidgets import QFileDialog


def check_ip_connection(ip_address):
    # Send a ping request to the IP address
    result = subprocess.call(['ping', '-c', '1', '-W', '1', ip_address],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Check the result of the ping command
    if result == 0:
        return True
    else:
        return False


def check_i2c_device(address):
    # Define the I2C bus number (typically 1 for Raspberry Pi)
    bus = smbus.SMBus(1)

    try:
        bus.read_byte(address)  # Try to read a byte from the device address
        return True
    except IOError:
        return False


def get_remaining_storage():
    disk_usage = psutil.disk_usage('/')
    remaining_bytes = disk_usage.free
    return remaining_bytes / (1024 ** 3)  # Convert bytes to gigabytes


def calculate_speed():

    best_sps = None

    for microstepping in General.microstepping_options:
        # Calculate effective steps per rotation with microstepping
        steps_per_rotation_with_microstepping = General.motor_steps * \
            General.gear_ratio * microstepping
        # Calculate SPS for the given RPM
        sps = round(
            (General.frame_RPM * steps_per_rotation_with_microstepping) / 60, 3)
        # Check if SPS is within the desired range
        if 400 <= sps <= 1000 and (best_sps is None or sps < best_sps):
            General.frame_SPS = sps
            General.frame_microstepping = microstepping

    for microstepping in General.microstepping_options:
        # Calculate effective steps per rotation with microstepping
        steps_per_rotation_with_microstepping = General.motor_steps * \
            General.gear_ratio * microstepping
        # Calculate SPS for the given RPM
        sps = round(
            (General.core_RPM * steps_per_rotation_with_microstepping) / 60, 3)
        # Check if SPS is within the desired range
        if 400 <= sps <= 1000 and (best_sps is None or sps < best_sps):
            General.core_SPS = sps
            General.core_microstepping = microstepping
    Commands.set_speed()

# ---------------------------------------------------------------------------- #
#                               imaging functions                              #
# ---------------------------------------------------------------------------- #


def select_directory(self):
    m_directory = str(QFileDialog.getExistingDirectory(
        self, "Select Directory", '/media/pi'))
    if len(m_directory) != 0:
        General.custom_directory = m_directory
    UI_Update.imaging_UI_update(self)


def ambient_sensor_temperature_offset(self):
    General.ambient_temperature_offset = self.ambient_temperature_offset_value_doubleSpinBox.value()


def ambient_sensor_humidity_offset(self):
    General.ambient_humidity_offset = self.ambient_humidity_offset_value_doubleSpinBox.value()


def ambient_sensor_pressure_offset(self):
    General.ambient_pressure_offset = self.ambient_pressure_offset_value_doubleSpinBox.value()


def sensor_export_data(self):
    try:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        if self.main_tabWidget.currentIndex() == 3:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save CSV File",
                General.default_directory
                + "/ambient_sensor_data_"
                + General.date
                + ".csv",
                "CSV Files (*.csv)",
                options=options,
            )
            if file_name:
                UI_Update.export_UI_update(self, 0)
                export = list(
                    zip(
                        General.ambient_sensor_time_stamp,
                        General.ambient_temperature,
                        General.ambient_humidity,
                        General.ambient_pressure,
                    )
                )
                with open(file_name, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        ["Time", "Temperature", "Humidity", "Pressure"])
                    writer.writerows(export)
                    UI_Update.export_UI_update(self, 1)
        elif self.main_tabWidget.currentIndex() == 4:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save CSV File",
                General.default_directory
                + "/motion_sensor_data_"
                + General.date
                + ".csv",
                "CSV Files (*.csv)",
                options=options,
            )
            if file_name:
                UI_Update.export_UI_update(self, 2)
                export = list(
                    zip(
                        General.motion_sensor_time_stamp,
                        General.motion_acceleration_x,
                        General.motion_acceleration_y,
                        General.motion_acceleration_z,
                        General.motion_gyroscope_x,
                        General.motion_gyroscope_y,
                        General.motion_gyroscope_z,
                    )
                )
                with open(file_name, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        [
                            "Time",
                            "acceleration_x",
                            "acceleration_y",
                            "acceleration_z",
                            "gyroscope_x",
                            "gyroscope_y",
                            "gyroscope_z",
                        ]
                    )
                    writer.writerows(export)
                    UI_Update.export_UI_update(self, 3)
    except Exception as e:
        print(e, "Export failure, contact Jerry for support")


def fanspeed_update(self, mode):
    if mode:
        try:
            core_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            core_socket.settimeout(General.socket_timeout)
            core_socket.connect(General.server_address)
            cmd = "B~" + \
                str(self.lighting_core_fan_speed_horizontalSlider.sliderPosition())
            core_socket.sendall(cmd.encode())
            core_socket.close()

        except Exception as e:
            print(e, "Fan failure,contact Jerry for support")
    else:
        Commands.set_fan_speed(self)
