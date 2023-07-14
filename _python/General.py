from PyQt5.QtGui import QPalette, QColor, QImage, QIcon, QPixmap
import time
import socket

# ---------------------------------------------------------------------------- #
#                           UI pallette declarations                           #
# ---------------------------------------------------------------------------- #
palette_red = QPalette()
palette_red.setColor(QPalette.WindowText, QColor(150, 0, 0))

palette_green = QPalette()
palette_green.setColor(QPalette.WindowText, QColor(0, 150, 0))
# ---------------------------------------------------------------------------- #
#                           error image declarations                           #
# ---------------------------------------------------------------------------- #
camera_error_image = QImage("../_image/camera_error.png")

storage_critical_error_image = QImage("../_image/storage_critical_error.png")

# ---------------------------------------------------------------------------- #
#                          communication declarations                          #
# ---------------------------------------------------------------------------- #
core_address = '10.0.5.1'

socket_timeout = 20

MCU_address = 0x08

ambient_sensor_address = 0x76

motion_sensor_address = 0x6A

server_address = (core_address, 23456)


# ---------------------------------------------------------------------------- #
#                             lighting declarations                            #
# ---------------------------------------------------------------------------- #
commands_list = []

IR_stat = False

IR_imaging = False

# ---------------------------------------------------------------------------- #
#                         Threads watchdog declarations                        #
# ---------------------------------------------------------------------------- #
cycle_running = False


# ---------------------------------------------------------------------------- #
#                           power cycle declarations                           #
# ---------------------------------------------------------------------------- #
on_duration = 60

off_duration = 60

# ---------------------------------------------------------------------------- #
#                          motor settings declarations                         #
# ---------------------------------------------------------------------------- #

motors_linked = True

frame_enabled = False
frame_RPM = None
frame_SPS = None
frame_microstepping = None
frame_direction = 1

core_enabled = False
core_RPM = None
core_SPS = None
core_microstepping = None
core_direction = 1

motor_steps = 200

gear_ratio = 10

microstepping_options = [2, 4, 8, 16, 32, 64, 128, 256]

# ---------------------------------------------------------------------------- #
#                         imaging settings declarations                        #
# ---------------------------------------------------------------------------- #

date = time.strftime('%m_%d_%Y')

imaging_interval = 2

imaging_duration = 2

imaging_total = 1

imaging_current = 0

received_packets = 0

default_directory = "/home/pi/Desktop"

# --------------------------------- autofocus -------------------------------- #
lens_position = None

autofocus_mode = None

custom_directory = None

full_directory = None

sequence_name = None

current_image = None

core_busy = False
# ---------------------------------------------------------------------------- #
#                               icon declarations                              #
# ---------------------------------------------------------------------------- #


def initialize_icons():
    global linked
    linked = QIcon()
    linked.addPixmap(QPixmap("../_image/Link.png"),
                     QIcon.Normal, QIcon.Off)

    global broken
    broken = QIcon()
    broken.addPixmap(QPixmap("../_image/Broken_Link.png"),
                     QIcon.Normal, QIcon.Off)

    global clockwise
    clockwise = QIcon()
    clockwise.addPixmap(QPixmap("../_image/Clockwise.png"),
                        QIcon.Normal, QIcon.Off)

    global counter_clockwise
    counter_clockwise = QIcon()
    counter_clockwise.addPixmap(QPixmap("../_image/Counter_Clockwise.png"),
                                QIcon.Normal, QIcon.Off)
