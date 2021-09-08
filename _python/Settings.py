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

    global on_time
    on_time = 60

    global off_time
    off_time = 60

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
        10: 2290,
        15: 1498,
        20: 1128,
        25: 896,
        30: 738,
        35: 632,
        40: 548,
        45: 476,
        50: 432,
        55: 392,
        60: 360,
        65: 328,
        70: 300,
        75: 276,
        80: 260,
        85: 244,
        90: 228,
        95: 212,
        100: 200,

        105: 409,
        110: 394,
        115: 378,
        120: 362,
        125: 342,
        130: 330,
        135: 313,
        140: 301,
        145: 294,
        150: 278,
        155: 271,
        160: 262,
        165: 253,
        170: 246,
        175: 238,
        180: 230,
        185: 226,
        190: 214,
        195: 210,
        200: 202,

        205: 426,
        210: 410,
        215: 399,
        220: 393,
        225: 378,
        230: 377,
        235: 362,
        240: 361,
        245: 346,
        250: 342,
        255: 334,
        260: 328,
        265: 318,
        270: 308,
        275: 307,
        280: 302,
        285: 298,
        290: 294,
        295: 284,
        300: 278,

        305: 578,
        310: 566,
        315: 558,
        320: 550,
        325: 541,
        330: 530,
        335: 526,
        340: 514,
        345: 509,
        350: 498,
        355: 494,
        360: 478,
        365: 477,
        370: 466,
        375: 462,
        380: 458,
        385: 450,
        390: 446,
        395: 442,
        400: 434,

        405: 882,
        410: 866,
        415: 859,
        420: 850,
        425: 838,
        430: 829,
        435: 814,
        440: 810,
        445: 798,
        450: 790,
        455: 782,
        460: 773,
        465: 762,
        470: 757,
        475: 746,
        480: 741,
        485: 733,
        490: 726,
        495: 714,
        500: 710,
        505: 698,
        510: 694,
        515: 682,
        520: 681,
        525: 674,
        530: 666,
        535: 662,
        540: 652,
        545: 646,
        550: 642,
        555: 634,
        560: 630,
        565: 626,
        570: 618,
        575: 610,
        580: 609,
        585: 601,
        590: 595,
        595: 594,
        600: 582,

        605: 1186,
        610: 1178,
        615: 1162,
        620: 1161,
        625: 1146,
        630: 1142,
        635: 1130,
        640: 1120,
        645: 1114,
        650: 1098,
        655: 1094,
        660: 1082,
        665: 1078,
        670: 1066,
        675: 1062,
        680: 1050,
        685: 1046,
        690: 1038,
        695: 1030,
        700: 1026,
        705: 1014,
        710: 1010,
        715: 998,
        720: 990,
        725: 982,
        730: 978,
        735: 974,
        740: 966,
        745: 962,
        750: 950,
        755: 946,
        760: 942,
        765: 930,
        770: 929,
        775: 919,
        780: 914,
        785: 910,
        790: 898,
        795: 897,
        800: 894,
        805: 882,
        810: 880,
        815: 878,
        820: 866,
        825: 864,
        830: 858,
        835: 850,
        840: 848,
        845: 845,
        850: 837,
        855: 830,
        860: 827,
        865: 826,
        870: 814,
        875: 813,
        880: 810,
        885: 798,
        890: 797,
        895: 796,
        900: 790,
        905: 782,
        910: 781,
        915: 778,
        920: 772,
        925: 766,
        930: 762,
        935: 758,
        940: 754,
        945: 750,
        950: 746,
        955: 742,
        960: 738,
        965: 734,
        970: 730,
        975: 726,
        980: 725,
        985: 718,
        990: 714,
        995: 713,
        1000: 710,


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
