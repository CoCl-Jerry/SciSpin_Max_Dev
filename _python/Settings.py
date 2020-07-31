import smbus
import time
import Settings
from PyQt5 import QtGui

i2c_cmd = 0x5E


def init():

    global LINKED
    LINKED = True

    global IR_STAT
    IR_STAT = False

    global IR_imaging
    IR_imaging = False

    global imaging
    imaging = False

    global busy
    busy = False

    global log_sensor
    log_sensor = False

    global sensor_flag
    sensor_flag = False

    global log_duration
    log_duration = 1

    global frame_RPM
    frame_RPM = 0.3

    global core_RPM
    core_RPM = 0.3

    global lighting_addr
    lighting_addr = 0x08

    global frame_addr
    frame_addr = 0x09

    global core_addr
    core_addr = 0x10

    global tag_index
    tag_index = 0

    global ACC_X_text
    ACC_X_text = "offline"
    global ACC_Y_text
    ACC_Y_text = "offline"
    global ACC_Z_text
    ACC_Z_text = "offline"

    global GYRO_X_text
    GYRO_X_text = "offline"
    global GYRO_Y_text
    GYRO_Y_text = "offline"
    global GYRO_Z_text
    GYRO_Z_text = "offline"

    global MAG_X_text
    MAG_X_text = "offline"
    global MAG_Y_text
    MAG_Y_text = "offline"
    global MAG_Z_text
    MAG_Z_text = "offline"

    global sequence_name
    sequence_name = ""

    global current_image
    current_image = ""

    global default_dir
    default_dir = "/home/pi/Desktop"

    global full_dir
    full_dir = ""

    global date
    date = time.strftime('%m_%d_%Y')

    global prelog_dir
    prelog_dir = "/home/pi/Desktop/sensor_log/"

    global log_dir
    log_dir = "/home/pi/Desktop/sensor_log/" + date

    global AOI_X
    AOI_X = 0
    global AOI_Y
    AOI_Y = 0
    global AOI_W
    AOI_W = 1
    global AOI_H
    AOI_H = 1

    global interval
    interval = 5

    global duration
    duration = 5

    global total
    total = 1

    global current
    current = 0

    global rotation
    rotation = 0

    global frame_dir
    frame_dir = False

    global core_dir
    core_dir = False

    global x_resolution
    x_resolution = 2464

    global y_resolution
    y_resolution = 2464

    global imaging_mode
    imaging_mode = 1

    global trasmitted
    trasmitted = 0

    global commands_list
    commands_list = []

    global timelapse_running
    timelapse_running = False

    global cycle_running
    cycle_running = False

    global cycle_time
    cycle_time = 60

    global time_elipsed
    time_elipsed = 0

    global log_start_time
    log_start_time = 0

    global sample_time
    sample_time = 0

    global forward
    forward = QtGui.QIcon()
    forward.addPixmap(QtGui.QPixmap("../_image/forward.png"),
                      QtGui.QIcon.Normal, QtGui.QIcon.Off)

    global reverse
    reverse = QtGui.QIcon()
    reverse.addPixmap(QtGui.QPixmap("../_image/Reverse.png"),
                      QtGui.QIcon.Normal, QtGui.QIcon.Off)

    global linked
    linked = QtGui.QIcon()
    linked.addPixmap(QtGui.QPixmap("../_image/Link.png"),
                     QtGui.QIcon.Normal, QtGui.QIcon.Off)

    global broken
    broken = QtGui.QIcon()
    broken.addPixmap(QtGui.QPixmap("../_image/Broken_Link.png"),
                     QtGui.QIcon.Normal, QtGui.QIcon.Off)


def sendCMD(addr, cont):
    print(cont)
    try:
        if Settings.busy:
            time.sleep(0.05)

        Settings.busy = True
        bus = smbus.SMBus(1)
        converted = []
        for b in cont:
            converted.append(ord(b))
        bus.write_i2c_block_data(addr, i2c_cmd, converted)
        Settings.busy = False
    except Exception as e:
        print(e)
