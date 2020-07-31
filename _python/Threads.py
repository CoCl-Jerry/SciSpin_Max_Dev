import Settings
import socket
import board
import busio
import adafruit_fxos8700
import adafruit_fxas21002c
import os
import timeit
import Commands

from time import sleep
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from picamera import PiCamera


class Cycle(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        if(Settings.IR_STAT):
            Settings.sendCMD(Settings.lighting_addr, "3~")
        Commands.clear_lights()
        sleep(1)
        for x in Settings.commands_list:
            cmd = "4~" + x
            Settings.sendCMD(Settings.lighting_addr, cmd)
            sleep(0.1)
        Settings.sendCMD(Settings.lighting_addr, "5~")
        if(Settings.IR_STAT):
            sleep(0.1)
            Settings.sendCMD(Settings.lighting_addr, "3~")
        on_stat = True

        while True:
            for x in range(Settings.cycle_time * 60):
                sleep(1)

                if not Settings.cycle_running:
                    on_stat = False
                    break

            if(on_stat):
                if(Settings.IR_STAT):
                    Settings.sendCMD(Settings.lighting_addr, "3~")
                Commands.clear_lights()
                on_stat = False
            else:
                for i in Settings.commands_list:
                    cmd = "4~" + i
                    Settings.sendCMD(Settings.lighting_addr, cmd)
                    sleep(0.1)
                Settings.sendCMD(Settings.lighting_addr, "5~")
                if(Settings.IR_STAT):
                    sleep(0.1)
                    Settings.sendCMD(Settings.lighting_addr, "3~")
                on_stat = True
            if not Settings.cycle_running:
                break


class Snap(QThread):

    transmit = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        if Settings.IR_imaging:
            Commands.IR_Imaging_trigger()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_address = "10.0.5.2"
        server_address = (ip_address, 23456)
        sock.connect(server_address)
        cmd = "A~" + str(350) + "~" + str(350) + "~" + \
            str(Settings.rotation) + "~" + str(int(Settings.AOI_X * 100)) + "~" + \
            str(int(Settings.AOI_Y * 100)) + "~" + str(int(Settings.AOI_W * 100)) + \
            "~" + str(int(Settings.AOI_H * 100)) + "~1"
        print(cmd)
        sock.sendall(cmd.encode())

        with open('../_temp/snapshot.jpg', 'wb') as f:
            while True:
                data = sock.recv(5)
                if not data:
                    break
                f.write(data)
                self.transmit.emit()
        sock.close()


class Preview(QThread):
    transmit = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip_address = "10.0.5.2"
        server_address = (ip_address, 23456)
        sock.connect(server_address)
        cmd = "A~" + str(Settings.x_resolution) + "~" + str(Settings.y_resolution) + \
            "~" + str(Settings.rotation) + "~" + str(Settings.imaging_mode)

        start_time = timeit.default_timer()
        sock.sendall(cmd.encode())

        if(Settings.imaging_mode == 1):
            with open('../_temp/preview.jpg', 'wb') as f:
                while True:
                    data = sock.recv(5)
                    if not data:
                        break
                    f.write(data)
                    self.transmit.emit()
            sock.close()

        else:
            with open('../_temp/preview.png', 'wb') as f:
                while True:
                    data = sock.recv(5)
                    if not data:
                        break
                    f.write(data)
                    self.transmit.emit()
            sock.close()
        Settings.time_elipsed = int(timeit.default_timer() - start_time)


class Sensor(QThread):
    update = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_fxos8700.FXOS8700(i2c)

        i2c2 = busio.I2C(board.SCL, board.SDA)
        sensor2 = adafruit_fxas21002c.FXAS21002C(i2c2)
        while True:
            while Settings.free_sensor:
                if(Settings.tag_index == 0):
                    accel_x, accel_y, accel_z = sensor.accelerometer
                    Settings.ACC_X_text = "{0:.2f}".format(accel_x)
                    Settings.ACC_Y_text = "{0:.2f}".format(accel_y)
                    Settings.ACC_Z_text = "{0:.2f}".format(accel_z)

                elif(Settings.tag_index == 1):
                    gyro_x, gyro_y, gyro_z = sensor2.gyroscope
                    Settings.GYRO_X_text = "{0:.2f}".format(gyro_x)
                    Settings.GYRO_Y_text = "{0:.2f}".format(gyro_y)
                    Settings.GYRO_Z_text = "{0:.2f}".format(gyro_z)
                else:
                    mag_x, mag_y, mag_z = sensor.magnetometer
                    Settings.MAG_X_text = "{0:.2f}".format(mag_x)
                    Settings.MAG_Y_text = "{0:.2f}".format(mag_y)
                    Settings.MAG_Z_text = "{0:.2f}".format(mag_z)

                self.update.emit()
                sleep(0.1)
            if(not os.path.isdir(Settings.log_dir)):
                os.umask(0)
                os.mkdir(Settings.log_dir)

                log_file = open(Settings.log_dir + "log.txt", "w")

                log_file.write("Purchase Amount:test"")
                log_file.close()
                Settings.free_sensor = True


class Timelapse(QThread):
    captured = QtCore.pyqtSignal()
    transmit = QtCore.pyqtSignal()
    transmitstart = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        if(not os.path.isdir(Settings.full_dir)):
            os.umask(0)
            os.mkdir(Settings.full_dir)

        for i in range(Settings.total):
            start_time = timeit.default_timer()
            Settings.current = i
            if(Settings.imaging_mode == 1):
                Settings.current_image = Settings.full_dir + \
                    "/" + Settings.sequence_name + "_%04d.jpg" % i
            else:
                Settings.current_image = Settings.full_dir + \
                    "/" + Settings.sequence_name + "_%04d.png" % i

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip_address = "10.0.5.2"
            server_address = (ip_address, 23456)
            sock.connect(server_address)

            cmd = "A~" + str(Settings.x_resolution) + "~" + str(Settings.y_resolution) + \
                "~" + str(Settings.rotation) + "~" + str(Settings.imaging_mode)

            sock.sendall(cmd.encode())

            with open(Settings.current_image, 'wb') as f:
                self.transmitstart.emit()
                while True:
                    data = sock.recv(5)
                    if not data:
                        break
                    f.write(data)
                    self.transmit.emit()

            sock.close()

            self.captured.emit()
            elapsed = int(timeit.default_timer() - start_time)

            if(elapsed < Settings.interval * 60):
                for x in range(Settings.interval * 60 - elapsed):
                    sleep(1)
                    if not Settings.timelapse_running:
                        break
            if not Settings.timelapse_running:
                break
