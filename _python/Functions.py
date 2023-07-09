import General
import Commands
import UI_Update
import timeit
import Call_Thread
import socket
import os
import psutil
import subprocess
import smbus

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
        sps = (General.frame_RPM * steps_per_rotation_with_microstepping) / 60
        # Check if SPS is within the desired range
        if 400 <= sps <= 1000 and (best_sps is None or sps < best_sps):
            General.frame_SPS = sps
            General.frame_microstepping = microstepping

    for microstepping in General.microstepping_options:
        # Calculate effective steps per rotation with microstepping
        steps_per_rotation_with_microstepping = General.motor_steps * \
            General.gear_ratio * microstepping
        # Calculate SPS for the given RPM
        sps = (General.core_RPM * steps_per_rotation_with_microstepping) / 60
        # Check if SPS is within the desired range
        if 400 <= sps <= 1000 and (best_sps is None or sps < best_sps):
            General.core_SPS = sps
            General.core_microstepping = microstepping


# def rotate_image(self):
#     Settings.rotation += 1
#     Call_Thread.start_snapshot(self)


# def IST_Edit(self):
#     Settings.sequence_name = self.title_lineEdit.text()
#     Settings.full_dir = Settings.default_dir + "/" + Settings.sequence_name
#     self.directory_label.setText(Settings.full_dir)

#     if Settings.date not in Settings.sequence_name:
#         self.addDate_pushButton.setEnabled(True)
#     if len(Settings.sequence_name) == 0:
#         self.addDate_pushButton.setEnabled(False)
#     UI_Update.validate_input(self)


# def add_date(self):
#     Settings.sequence_name = Settings.sequence_name + "_" + Settings.date
#     self.title_lineEdit.setText(Settings.sequence_name)
#     Settings.full_dir = Settings.default_dir + "/" + Settings.sequence_name
#     self.directory_label.setText(Settings.full_dir)
#     self.addDate_pushButton.setEnabled(False)


# def ICI_Change(self):
#     Settings.interval = self.ICI_spinBox.value()
#     UI_Update.validate_input(self)


# def Cycle_Change(self):
#     Settings.on_time = self.onCycle_spinBox.value()
#     Settings.off_time = self.offCycle_spinBox.value()


# def ISD_Change(self):
#     Settings.duration = self.ISD_spinBox.value()
#     UI_Update.validate_input(self)


# def select_directory(self):
#     m_directory = str(QFileDialog.getExistingDirectory(
#         self, "Select Directory", '/media/pi'))
#     if len(m_directory) != 0:
#         Settings.full_dir = m_directory + "/" + Settings.sequence_name
#         self.directory_label.setText(Settings.full_dir)
#     UI_Update.validate_input(self)


# def camera_update(self):
#     Settings.AOI_X = self.xAxis_horizontalSlider.sliderPosition() / 100
#     Settings.AOI_Y = self.xAxis_horizontalSlider.sliderPosition() / 100
#     Settings.AOI_W = self.yAxis_horizontalSlider.sliderPosition() / 100
#     Settings.AOI_H = self.yAxis_horizontalSlider.sliderPosition() / 100

#     Settings.x_resolution = self.x_resolution_spinBox.value()
#     Settings.y_resolution = self.y_resolution_spinBox.value()

#     formatted_x = "{:.2f}".format(
#         self.xAxis_horizontalSlider.sliderPosition() / 100)
#     formatted_y = "{:.2f}".format(
#         self.yAxis_horizontalSlider.sliderPosition() / 100)
#     self.xAxis_label.setText(
#         "Zoom Axis A: " + formatted_x)
#     self.yAxis_label.setText(
#         "Zoom Axis B: " + formatted_y)


# def update_mode(self):
#     Settings.imaging_mode = self.JPG_radioButton.isChecked()


# def fanspeed_update(self):
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         ip_address = "10.0.5.1"
#         server_address = (ip_address, 23456)
#         sock.connect(server_address)
#         cmd = "B~" + str(self.fanSpeed_horizontalSlider.sliderPosition())
#         sock.sendall(cmd.encode())
#         sock.close()

#     except Exception as e:
#         print(e, "Fan failure,contact Jerry for support")


# def IR_mode(self):
#     Settings.IR_imaging = self.infraredImaging_checkBox.isChecked()


# def check_connection():
#     os.system("ip addr show > ../_temp/output.txt")
#     if 'peer' in open('../_temp/output.txt').read():
#         print("peer connected")
#         return True
#     else:
#         print("peer unconnected")
#         return False


# def printci(self):
#     Settings.tag_index = self.Sensor_tabWidget.currentIndex()


# def sample_change(self):
#     Settings.sample_time = self.sample_doubleSpinBox.value()


# def sensor_log(self):
#     Settings.log_start_time = timeit.default_timer()
#     Settings.log_sensor = True
#     Settings.log_duration = self.log_spinBox.value() * 60
