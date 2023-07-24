import General
import socket
import board
import math
import os
import datetime
from time import sleep, perf_counter
from collections import deque
import Commands

from adafruit_bme280 import basic as adafruit_bme280
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
from adafruit_lsm6ds import Rate, AccelRange, GyroRange

from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal


class Cycle(QThread):
    countdown = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        Commands.extract_lights()
        General.power_status = False
        sleep(2)
        Commands.deploy_lights()
        General.power_status = True

        while True:
            if General.power_status:
                target_time = datetime.datetime.now() + datetime.timedelta(minutes=General.on_duration)
                while datetime.datetime.now() < target_time:
                    sleep(1)
                    General.cycle_countdown = int(
                        (target_time - datetime.datetime.now()).total_seconds())
                    self.countdown.emit()
                    if not General.cycle_thread_running:
                        General.power_status = False
                        break
                Commands.extract_lights()
                General.power_status = False
            else:
                target_time = datetime.datetime.now() + datetime.timedelta(minutes=General.off_duration)

                while datetime.datetime.now() < target_time:
                    sleep(1)
                    General.cycle_countdown = int(
                        (target_time - datetime.datetime.now()).total_seconds())
                    self.countdown.emit()

                    if not General.cycle_thread_running:
                        General.power_status = False
                        break
                Commands.deploy_lights()
                General.power_status = True
            if not General.cycle_thread_running:
                break


class Ambient(QThread):
    ambient_sensor_update = pyqtSignal()
    initialized = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(
            i2c, General.ambient_sensor_address)
        General.ambient_sensor_initial_time = round(perf_counter(), 2)

        while General.ambient_thread_running:
            if (
                perf_counter()
                - General.ambient_sensor_initial_time
                - General.ambient_sensor_previous_time
                > General.ambient_sensor_interval
                or len(General.ambient_sensor_time_stamp) == 0
            ):

                General.ambient_temperature.append(
                    round(bme280.temperature +
                          General.ambient_temperature_offset, 2)
                )
                General.ambient_humidity.append(
                    round(
                        bme280.humidity + General.ambient_humidity_offset, 2
                    )
                )
                General.ambient_pressure.append(
                    round(
                        bme280.pressure + General.ambient_pressure_offset, 2
                    )
                )

                General.ambient_sensor_time_stamp.append(
                    round(perf_counter() -
                          General.ambient_sensor_initial_time, 2)
                )

                General.ambient_sensor_previous_time = (
                    General.ambient_sensor_time_stamp[-1]
                )

                if len(General.ambient_sensor_time_stamp) == 2:
                    self.initialized.emit()
                elif len(General.ambient_sensor_time_stamp) > 2:
                    self.ambient_sensor_update.emit()


class Motion(QThread):
    motion_sensor_update = pyqtSignal()
    initialized = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        motion_sensor = ISM330DHCX(i2c)

        motion_sensor.accelerometer_data_rate = Rate.RATE_208_HZ
        motion_sensor.accelerometer_range = AccelRange.RANGE_8G
        motion_sensor.gyro_data_rate = Rate.RATE_208_HZ

        # LSM6DS_RATE_SHUTDOWN, LSM6DS_RATE_12_5_HZ, LSM6DS_RATE_26_HZ, LSM6DS_RATE_52_HZ,
        # LSM6DS_RATE_104_HZ, LSM6DS_RATE_208_HZ, LSM6DS_RATE_416_HZ, LSM6DS_RATE_833_HZ,
        # LSM6DS_RATE_1_66K_HZ, LSM6DS_RATE_3_33K_HZ, LSM6DS_RATE_6_66K_HZ

        General.motion_sensor_initial_time = round(perf_counter(), 2)

        General.motion_sensor_graph_time_stamp = deque(maxlen=500)

        General.motion_acceleration_graph_x = deque(maxlen=500)

        General.motion_acceleration_graph_y = deque(maxlen=500)

        General.motion_acceleration_graph_z = deque(maxlen=500)

        General.motion_gyroscope_graph_x = deque(maxlen=500)

        General.motion_gyroscope_graph_y = deque(maxlen=500)

        General.motion_gyroscope_graph_z = deque(maxlen=500)

        while General.motion_thread_running:
            if (
                perf_counter()
                - General.motion_sensor_initial_time
                - General.motion_sensor_previous_time
                > General.motion_sensor_interval
                or len(General.motion_sensor_time_stamp) == 0
            ):
                curent_acceleration = motion_sensor.acceleration
                current_gyro = motion_sensor.gyro

                General.motion_acceleration_x.append(
                    round(curent_acceleration[0], 2)
                )

                General.motion_acceleration_y.append(
                    round(curent_acceleration[1], 2)
                )

                General.motion_acceleration_z.append(
                    round(curent_acceleration[2], 2)
                )

                General.motion_acceleration_graph_x.append(
                    General.motion_acceleration_x[-1]
                )

                General.motion_acceleration_graph_y.append(
                    General.motion_acceleration_y[-1]
                )

                General.motion_acceleration_graph_z.append(
                    General.motion_acceleration_z[-1]
                )

                General.motion_gyroscope_x.append(
                    round(math.degrees(current_gyro[0]), 2))

                General.motion_gyroscope_y.append(
                    round(math.degrees(current_gyro[1]), 2))

                General.motion_gyroscope_z.append(
                    round(math.degrees(current_gyro[2]), 2))

                General.motion_gyroscope_graph_x.append(
                    General.motion_gyroscope_x[-1])
                General.motion_gyroscope_graph_y.append(
                    General.motion_gyroscope_y[-1])
                General.motion_gyroscope_graph_z.append(
                    General.motion_gyroscope_z[-1])

                General.motion_sensor_time_stamp.append(
                    round(perf_counter() -
                          General.motion_sensor_initial_time, 2)
                )

                General.motion_sensor_graph_time_stamp.append(
                    General.motion_sensor_time_stamp[-1]
                )
                General.motion_sensor_previous_time = (
                    General.motion_sensor_time_stamp[-1]
                )

                if len(General.motion_sensor_time_stamp) == 2:
                    self.initialized.emit()
                elif len(General.motion_sensor_time_stamp) > 2:
                    self.motion_sensor_update.emit()


# ---------------------------------------------------------------------------- #
#                                imaging thread                                #
# ---------------------------------------------------------------------------- #
class Capture(QThread):

    transmit = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        if General.IR_imaging:
            Commands.IR_imaging_toggle(1)
        try:
            core_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            core_socket.settimeout(General.socket_timeout)
            core_socket.connect(General.server_address)

            if General.capture_mode == 0:
                cmd = "A~350~350~1~0~0~" + General.digital_zoom+"~1"
                General.current_image = "../_temp/snapshot.jpg"
            elif General.capture_mode == 1:
                cmd = "A~350~350~0~1~-1~" + General.digital_zoom+"~1"
                General.current_image = "../_temp/snapshot.jpg"
            elif General.capture_mode == 2:
                cmd = "A~350~350~0~1~1~" + General.digital_zoom+"~1"
                General.current_image = "../_temp/snapshot.jpg"
            elif General.capture_mode == 3:
                cmd = "A~350~350~0~0~0~" + General.digital_zoom+"~1"
                General.current_image = "../_temp/snapshot.jpg"
            else:
                cmd = "A~"+General.x_resolution+"~" + \
                    General.y_resolution+"~0~0~0~" + General.digital_zoom + \
                    "~" + str(General.imaging_format)
                if General.imaging_format:
                    General.current_image = "../_temp/snapshot.jpg"
                else:
                    General.current_image = "../_temp/snapshot.png"

            core_socket.sendall(cmd.encode())
            print("Command sent", cmd)
            if General.capture_mode < 3:
                try:
                    response = core_socket.recv(
                        128).decode("utf-8").split('~', 2)
                    if float(response[1]) > 0:
                        General.lens_position = str(
                            round(float(response[1]), 2))+"mm"
                    else:
                        General.lens_position = "∞"
                    print("Lens Position:", General.lens_position)
                except socket.timeout:
                    print("No response from server, timed out")

            with open(General.current_image, 'wb') as f:

                while True:
                    try:
                        data = core_socket.recv(128)
                    except Exception as e:
                        print(e)
                    if not data:
                        break
                    f.write(data)
                    self.transmit.emit()
            core_socket.close()

        except Exception as e:
            print(e, "snapshot failure,contact Jerry for support")
        if General.IR_imaging:
            Commands.IR_imaging_toggle(0)

# ------------------------- imaging timelapse thread ------------------------- #


class Timelapse(QThread):
    capturing = pyqtSignal()
    transmit = pyqtSignal()
    captured = pyqtSignal()
    countdown = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        if not os.path.isdir(General.full_directory):
            os.umask(0)
            os.mkdir(General.full_directory)

        General.imaging_current_count = 0
        while General.imaging_current_count < General.imaging_total:

            self.capturing.emit()

            target_time = datetime.datetime.now(
            ) + datetime.timedelta(minutes=General.imaging_interval)

            if General.imaging_format:
                General.current_image = General.full_directory + \
                    "/" + General.sequence_name + "_%04d.jpg" % General.imaging_current_count
            else:
                General.current_image = General.full_directory + \
                    "/" + General.sequence_name + "_%04d.png" % General.imaging_current_count

            core_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            core_socket.settimeout(General.socket_timeout)
            core_socket.connect(General.server_address)

            if General.IR_imaging:
                Commands.IR_imaging_toggle(1)
            cmd = "A~"+General.x_resolution+"~" + General.y_resolution + \
                "~0~0~0~" + General.digital_zoom + \
                "~" + str(General.imaging_format)
            core_socket.sendall(cmd.encode())
            print("Command sent", cmd)

            with open(General.current_image, 'wb') as f:
                while True:
                    try:
                        data = core_socket.recv(128)
                    except Exception as e:
                        print(e, 'timeout after 20 seconds... retaking image')
                    if not data:
                        break
                    f.write(data)
                    self.transmit.emit()
                core_socket.close()
            if General.IR_imaging:
                Commands.IR_imaging_toggle(0)
            General.imaging_current_count += 1
            self.captured.emit()

            while datetime.datetime.now() < target_time:
                sleep(1)
                self.countdown.emit()
                General.timelapse_countdown = int(
                    (target_time - datetime.datetime.now()).total_seconds())
                if not General.timelapse_thread_running:
                    break
            if not General.timelapse_thread_running:
                break
