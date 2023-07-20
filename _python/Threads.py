import General
import Functions
import socket
import board
import busio
import os
import timeit
from time import sleep, perf_counter
import Commands
import adafruit_mma8451

from adafruit_bme280 import basic as adafruit_bme280

from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal


class Cycle(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        Commands.extract_lights()
        on_stat = False
        sleep(2)
        Commands.deploy_lights()
        on_stat = True

        while True:
            if on_stat:
                for x in range(General.on_duration * 1):
                    sleep(1)

                    if not General.cycle_thread_running:
                        on_stat = False
                        break
                Commands.extract_lights()
                on_stat = False
            else:
                for x in range(General.off_duration * 1):
                    sleep(1)

                    if not General.cycle_thread_running:
                        on_stat = False
                        break
                Commands.deploy_lights()
                on_stat = True
            if not General.cycle_thread_running:
                break


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
                cmd = "A~350~350~1~0~0~" + General.digital_zoom
            elif General.capture_mode == 1:
                cmd = "A~350~350~0~1~-1~" + General.digital_zoom
            elif General.capture_mode == 2:
                cmd = "A~350~350~0~1~1~" + General.digital_zoom
            elif General.capture_mode == 3:
                cmd = "A~350~350~0~0~0~" + General.digital_zoom
            elif General.capture_mode == 4:
                cmd = "A~"+General.x_resolution+"~" + \
                    General.y_resolution+"~0~0~0~" + General.digital_zoom

            core_socket.sendall(cmd.encode())
            print("Command sent", cmd)

            try:
                response = core_socket.recv(128).decode("utf-8").split('~', 2)
                if float(response[1]) > 0:
                    General.lens_position = str(
                        round(100/float(response[1]), 2))+"mm"
                else:
                    General.lens_position = "∞"
                print("Lens Position:", General.lens_position)
            except socket.timeout:
                print("No response from server, timed out")

            with open('../_temp/snapshot.jpg', 'wb') as f:
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

        except Exception as e:
            print(e, "snapshot failure,contact Jerry for support")
        if General.IR_imaging:
            Commands.IR_imaging_toggle(1)


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
                > 2
                or len(General.ambient_sensor_time_stamp) == 0
            ):
                print("ambient sensor measuring...")
                General.ambient_sensor_time_stamp.append(
                    round(perf_counter() -
                          General.ambient_sensor_initial_time, 2)
                )
                General.ambient_sensor_previous_time = (
                    General.ambient_sensor_time_stamp[-1]
                )

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

                # if len(General.ambient_sensor_time_stamp) == 2:
                #     self.initialized.emit()
                # elif len(General.ambient_sensor_time_stamp) > 2:
                self.ambient_sensor_update.emit()


# class Preview(QThread):
#     transmit = pyqtSignal()

#     def __init__(self):
#         QThread.__init__(self)

#     def __del__(self):
#         self._running = False

#     def run(self):
#         if Settings.IR_imaging:
#             Commands.extract_lights()
#             Settings.sendCMD("4~1")
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             ip_address = "10.0.5.1"
#             server_address = (ip_address, 23456)
#             sock.connect(server_address)
#             cmd = "A~" + str(Settings.x_resolution) + "~" + str(Settings.y_resolution) + "~" + \
#                 str(Settings.rotation) + "~" + str(int(Settings.AOI_X * 100)) + "~" + \
#                 str(int(Settings.AOI_Y * 100)) + "~" + str(int(Settings.AOI_W * 100)) + \
#                 "~" + str(int(Settings.AOI_H * 100)) + \
#                 "~" + str(int(Settings.imaging_mode))

#             start_time = timeit.default_timer()
#             sock.sendall(cmd.encode())

#             if Settings.imaging_mode == 1:
#                 with open('../_temp/preview.jpg', 'wb') as f:
#                     while True:
#                         try:
#                             data = sock.recv(5)
#                         except Exception as e:
#                             print(
#                                 e, ': no connection for 20 seconds... retaking image')
#                         if not data:
#                             break
#                         f.write(data)
#                         self.transmit.emit()
#                 sock.close()

#             else:
#                 with open('../_temp/preview.png', 'wb') as f:
#                     while True:
#                         data = sock.recv(5)
#                         if not data:
#                             break
#                         f.write(data)
#                         self.transmit.emit()
#                 sock.close()
#         except Exception as e:
#             print(e, "preview failure,contact Jerry for support")
#         Settings.time_elipsed = int(timeit.default_timer() - start_time)
#         if Settings.IR_imaging:
#             Settings.sendCMD("4~0")
#             Commands.deploy_lights()


# class Timelapse(QThread):
#     captured = pyqtSignal()
#     transmit = pyqtSignal()
#     transmitstart = pyqtSignal()

#     def __init__(self):
#         QThread.__init__(self)

#     def __del__(self):
#         self._running = False

#     def run(self):
#         if not os.path.isdir(Settings.full_dir):
#             os.umask(0)
#             os.mkdir(Settings.full_dir)

#         Settings.current = 0
#         while Settings.current < Settings.total:

#             start_time = timeit.default_timer()
#             if Settings.imaging_mode == 1:
#                 Settings.current_image = Settings.full_dir + \
#                     "/" + Settings.sequence_name + "_%04d.jpg" % Settings.current
#             else:
#                 Settings.current_image = Settings.full_dir + \
#                     "/" + Settings.sequence_name + "_%04d.png" % Settings.current

#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(20)
#             ip_address = "10.0.5.1"
#             skip = False
#             server_address = (ip_address, 23456)
#             if Functions.check_connection():
#                 try:
#                     sock.connect(server_address)
#                 except Exception as e:
#                     print(e, ': socket connection failed, please reboot device')
#                     skip = True
#                 if Settings.IR_imaging:
#                     Commands.extract_lights()
#                     Settings.sendCMD("4~1")

#                 cmd = "A~" + str(Settings.x_resolution) + "~" + str(Settings.y_resolution) + "~" + \
#                     str(Settings.rotation) + "~" + str(int(Settings.AOI_X * 100)) + "~" + \
#                     str(int(Settings.AOI_Y * 100)) + "~" + str(int(Settings.AOI_W * 100)) + \
#                     "~" + str(int(Settings.AOI_H * 100)) + \
#                     "~" + str(int(Settings.imaging_mode))
#                 if not skip:
#                     sock.sendall(cmd.encode())

#                     with open(Settings.current_image, 'wb') as f:
#                         self.transmitstart.emit()
#                         while True:
#                             try:
#                                 data = sock.recv(5)
#                             except Exception as e:
#                                 print(
#                                     e, ': no connection for 20 seconds... retaking image')
#                                 if Settings.IR_imaging:
#                                     Settings.sendCMD("4~0")
#                                     Commands.deploy_lights()
#                                 break
#                             if not data:
#                                 Settings.current += 1
#                                 print("image capture and transmission succesful")
#                                 if Settings.IR_imaging:
#                                     Settings.sendCMD("4~0")
#                                     Commands.deploy_lights()
#                                 break
#                             f.write(data)
#                             self.transmit.emit()
#                         sock.close()
#                         self.captured.emit()
#                 elapsed = int(timeit.default_timer() - start_time)

#             if elapsed < Settings.interval * 60:
#                 for x in range(Settings.interval * 60 - elapsed):
#                     sleep(1)
#                     if not Settings.timelapse_running:
#                         break
#             if not Settings.timelapse_running:
#                 break
