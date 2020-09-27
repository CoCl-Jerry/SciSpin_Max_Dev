import smbus
import time
import Settings
from PyQt5 import QtGui

i2c_cmd = 0x5E


def init():

    global LINKED
    LINKED = True

    global IR_stat
    IR_stat = False

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

    global frame_enabled
    frame_enabled = True

    global core_enabled
    core_enabled = True

    global frame_microstep
    frame_microstep = 256

    global core_microstep
    core_microstep = 256

    global frame_interval
    frame_interval = 1126

    global core_interval
    core_interval = 1126

    global acc_attached
    acc_attached = False

    global temp_attached
    temp_attached = False

    global tag_index
    tag_index = 0

    global ACC_X_text
    ACC_X_text = "offline"
    global ACC_Y_text
    ACC_Y_text = "offline"
    global ACC_Z_text
    ACC_Z_text = "offline"

    global TEMP_text
    TEMP_text = "offline"
    global HUD_text
    HUD_text = "offline"

    global PR_text
    PR_text = "offline"

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
    interval = 2

    global duration
    duration = 2

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

    global speed_dict
    speed_dict = {
        10: 5716,
        15: 3744,
        20: 2840,
        25: 2246,
        30: 1892,
        35: 1600,
        40: 1410,
        45: 1250,
        50: 1126,
        55: 1018,
        60: 934,
        65: 862,
        70: 794,
        75: 740,
        80: 694,
        85: 650,
        90: 614,
        95: 582,
        100: 552,
        105: 518,
        110: 492,
        115: 472,
        120: 448,
        125: 432,
        130: 412,
        135: 396,
        140: 376,
        145: 368,
        150: 356,

        155: 712,
        160: 688,
        165: 664,
        170: 644,
        175: 628,
        180: 608,
        185: 592,
        190: 576,
        195: 560,
        200: 546,
        205: 530,
        210: 516,
        215: 508,
        220: 492,
        225: 476,
        230: 472,
        235: 460,
        240: 448,
        245: 444,
        250: 432,

        255: 898,
        260: 860,
        265: 840,
        270: 824,
        275: 810,
        280: 796,
        285: 776,
        290: 764,
        295: 748,
        300: 738,
        305: 724,
        310: 712,
        315: 696,
        320: 688,
        325: 680,
        330: 664,
        335: 658,
        340: 646,
        345: 640,
        350: 626,


    }


def sendCMD(cont):
    print("sending command...\n" + cont)
    temp = cont + "\n"
    try:
        if Settings.busy:
            time.sleep(0.02)

        Settings.busy = True
        bus = smbus.SMBus(1)
        converted = []
        for b in temp:
            converted.append(ord(b))
        bus.write_i2c_block_data(0x08, i2c_cmd, converted)
        time.sleep(0.02)
        Settings.busy = False
    except Exception as e:
        print(e, "command send failure,contact Jerry for support")
