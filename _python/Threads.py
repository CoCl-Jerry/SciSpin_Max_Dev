import Settings
import Functions
import socket
import board
import busio
import os
import timeit
import time
import Commands
import adafruit_mma8451
import adafruit_bme280
import requests

from requests.auth import HTTPBasicAuth
from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal
from picamera import PiCamera


class Cycle(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        Commands.extract_lights()
        on_stat = False
        sleep(5)
        Commands.deploy_lights()
        on_stat = True

        while True:
            for x in range(Settings.cycle_time * 60):
                sleep(1)

                if not Settings.cycle_running:
                    on_stat = False
                    break

            if on_stat:
                Commands.extract_lights()
                on_stat = False
            else:
                Commands.deploy_lights()
                on_stat = True
            if not Settings.cycle_running:
                break


class Auth(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        uri = "https://data.cyverse.org/dav/iplant/home/" + \
            Settings.cyverseUsername
        print(uri)
        auth = HTTPBasicAuth(Settings.cyverseUsername,
                             Settings.cyversePassword)
        print(auth.__dict__)
        r = requests.get(uri, auth=auth)
        if(r.status_code != 200):
            # Put actual logic in place to trigger a popup or some error message that flashes
            print("ERR: Failed authentication!")
            print(r)
            Settings.cyverse_authenticated = False
        else:
            # Put actual logic in place to trigger a popup or some error message that flashes
            print("Authentication success")
            Settings.cyverse_authenticated = True


class Snap(QThread):

    transmit = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        if Settings.IR_imaging:
            Commands.extract_lights()
            Settings.sendCMD("4~1")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip_address = "10.0.5.1"
            server_address = (ip_address, 23456)
            sock.connect(server_address)
            cmd = "A~" + str(350) + "~" + str(350) + "~" + \
                str(Settings.rotation) + "~" + str(int(Settings.AOI_X * 100)) + "~" + \
                str(int(Settings.AOI_Y * 100)) + "~" + str(int(Settings.AOI_W * 100)) + \
                "~" + str(int(Settings.AOI_H * 100)) + "~1"
            sock.sendall(cmd.encode())

            with open('../_temp/snapshot.jpg', 'wb') as f:
                while True:
                    try:
                        data = sock.recv(5)
                    except Exception as e:
                        print(e, 'timeout after 20 seconds... retaking image')
                    if not data:
                        break
                    f.write(data)
                    self.transmit.emit()
            sock.close()

        except Exception as e:
            print(e, "snapshot failure,contact Jerry for support")
        if Settings.IR_imaging:
            Settings.sendCMD("4~0")
            Commands.deploy_lights()


class Preview(QThread):
    transmit = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        if Settings.IR_imaging:
            Commands.extract_lights()
            Settings.sendCMD("4~1")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip_address = "10.0.5.1"
            server_address = (ip_address, 23456)
            sock.connect(server_address)
            cmd = "A~" + str(Settings.x_resolution) + "~" + str(Settings.y_resolution) + "~" + \
                str(Settings.rotation) + "~" + str(int(Settings.AOI_X * 100)) + "~" + \
                str(int(Settings.AOI_Y * 100)) + "~" + str(int(Settings.AOI_W * 100)) + \
                "~" + str(int(Settings.AOI_H * 100)) + \
                "~" + str(int(Settings.imaging_mode))

            start_time = timeit.default_timer()
            sock.sendall(cmd.encode())

            if Settings.imaging_mode == 1:
                with open('../_temp/preview.jpg', 'wb') as f:
                    while True:
                        try:
                            data = sock.recv(5)
                        except Exception as e:
                            print(
                                e, ': no connection for 20 seconds... retaking image')
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
        except Exception as e:
            print(e, "preview failure,contact Jerry for support")
        Settings.time_elipsed = int(timeit.default_timer() - start_time)
        if Settings.IR_imaging:
            Settings.sendCMD("4~0")
            Commands.deploy_lights()


class Sensor(QThread):
    update = pyqtSignal()
    logstart = pyqtSignal()
    logdone = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        time.sleep(1)
        if Settings.acc_attached:
            sensor = adafruit_mma8451.MMA8451(i2c)
        if Settings.temp_attached:
            bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

        while True:
            try:
                if Settings.tag_index == 0 and Settings.acc_attached:
                    accel_x, accel_y, accel_z = sensor.acceleration
                    Settings.ACC_X_text = "{0:.2f}".format(accel_x)
                    Settings.ACC_Y_text = "{0:.2f}".format(accel_y)
                    Settings.ACC_Z_text = "{0:.2f}".format(accel_z)
                elif Settings.temp_attached:
                    Settings.TEMP_text = "{0:.2f}".format(bme280.temperature)
                    Settings.HUD_text = "{0:.2f}".format(bme280.humidity)
                    Settings.PR_text = "{0:.2f}".format(bme280.pressure)

                self.update.emit()
                sleep(Settings.sample_time)

                if Settings.log_sensor:
                    if not Settings.sensor_flag:
                        self.logstart.emit()
                        if not os.path.isdir(Settings.prelog_dir):
                            os.umask(0)
                            os.mkdir(Settings.prelog_dir)
                        if not os.path.isdir(Settings.log_dir):
                            os.umask(0)
                            os.mkdir(Settings.log_dir)
                        log_file = open(Settings.log_dir + "/log.txt", "w")
                        Settings.sensor_flag = True
                        os.chmod(Settings.log_dir + "/log.txt", 0o777)

                    if Settings.tag_index == 0:

                        log_file.write(Settings.ACC_X_text + "\t" +
                                       Settings.ACC_Y_text + "\t" + Settings.ACC_Z_text + "\r\n")
                    else:

                        log_file.write(Settings.TEMP_text + "\t" +
                                       Settings.HUD_text + "\t" + Settings.PR_text + "\r\n")

                    if int(timeit.default_timer() - Settings.log_start_time > Settings.log_duration):
                        Settings.log_sensor = False
                        Settings.sensor_flag = False
                        log_file.close()
                        self.logdone.emit()
            except Exception as e:
                pass


class Timelapse(QThread):
    captured = pyqtSignal()
    transmit = pyqtSignal()
    transmitstart = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        if not os.path.isdir(Settings.full_dir):
            os.umask(0)
            os.mkdir(Settings.full_dir)

        Settings.current = 0
        while Settings.current < Settings.total:

            start_time = timeit.default_timer()
            if Settings.imaging_mode == 1:
                Settings.current_image = Settings.full_dir + \
                    "/" + Settings.sequence_name + "_%04d.jpg" % Settings.current
            else:
                Settings.current_image = Settings.full_dir + \
                    "/" + Settings.sequence_name + "_%04d.png" % Settings.current

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(20)
            ip_address = "10.0.5.1"
            skip = False
            server_address = (ip_address, 23456)
            if Functions.check_connection():
                try:
                    sock.connect(server_address)
                except Exception as e:
                    print(e, ': socket connection failed, please reboot device')
                    skip = True
                if Settings.IR_imaging:
                    Commands.extract_lights()
                    Settings.sendCMD("4~1")

                cmd = "A~" + str(Settings.x_resolution) + "~" + str(Settings.y_resolution) + "~" + \
                    str(Settings.rotation) + "~" + str(int(Settings.AOI_X * 100)) + "~" + \
                    str(int(Settings.AOI_Y * 100)) + "~" + str(int(Settings.AOI_W * 100)) + \
                    "~" + str(int(Settings.AOI_H * 100)) + \
                    "~" + str(int(Settings.imaging_mode))
                if not skip:
                    sock.sendall(cmd.encode())

                    with open(Settings.current_image, 'wb') as f:
                        self.transmitstart.emit()
                        while True:
                            try:
                                data = sock.recv(5)
                            except Exception as e:
                                print(
                                    e, ': no connection for 20 seconds... retaking image')
                                if Settings.IR_imaging:
                                    Settings.sendCMD("4~0")
                                    Commands.deploy_lights()
                                break
                            if not data:
                                Settings.current += 1
                                print("image capture and transmission successful")
                                if Settings.IR_imaging:
                                    Settings.sendCMD("4~0")
                                    Commands.deploy_lights()
                                break
                            f.write(data)
                            self.transmit.emit()
                        sock.close()
                        self.captured.emit()
                if Settings.storage_mode:
                    Settings.file_list.append(Settings.current_image)
                elapsed = int(timeit.default_timer() - start_time)

            if elapsed < Settings.interval * 60:
                for x in range(Settings.interval * 60 - elapsed):
                    sleep(1)
                    if not Settings.timelapse_running:
                        break
            if not Settings.timelapse_running:
                break


class Cyverse(QThread):
    def __init__(self):
        QThread.__init__(self)
        Settings.cyverse_running = True

    def __del__(self):
        self._running = False

    def run(self):
        base_uri = "https://data.cyverse.org/dav/iplant/home/"
        uri = base_uri + Settings.cyverseUsername + "/" + 'FlashLapse'
        headers = {'Content-Type': 'image/jpeg'}

        auth = HTTPBasicAuth(Settings.cyverseUsername,
                             Settings.cyversePassword)
        requests.request(method='MKCOL', url=uri, auth=auth)
        uri = uri + '/' + Settings.date
        requests.request(method='MKCOL', url=uri, auth=auth)
        uri = uri + '/' + Settings.cpuserial
        requests.request(method='MKCOL', url=uri, auth=auth)
        uri = uri + '/' + Settings.sequence_name
        requests.request(method='MKCOL', url=uri, auth=auth)
        count = 0
        while (count < Settings.total):
            if (len(Settings.file_list) > 0):
                print("Cyverse Thread: File " + Settings.file_list[0])
                fh = open(Settings.file_list[0], 'rb')
                requests.put(url=uri + '/' + os.path.basename(Settings.file_list[0]),
                             headers=headers,
                             auth=auth,
                             data=fh)
                fh.close()
                #os.system("rm " + Settings.file_list[0])
                del Settings.file_list[0]
                count += 1
            if not Settings.cyverse_running:
                break
        Settings.cyverse_running = False
        return
