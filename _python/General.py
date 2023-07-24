from PyQt5.QtGui import QPalette, QColor, QImage, QIcon, QPixmap
from pyqtgraph import mkPen

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

cummunication_error_image = QImage("../_image/communication_error.png")

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
#                         Threads flag declarations                            #
# ---------------------------------------------------------------------------- #
timelapse_thread_running = False

cycle_thread_running = False

ambient_thread_running = False

motion_thread_running = False

# ---------------------------------------------------------------------------- #
#                           power cycle declarations                           #
# ---------------------------------------------------------------------------- #
on_duration = 60

off_duration = 60

power_status = None

cycle_countdown = None

# ---------------------------------------------------------------------------- #
#                          motor settings declarations                         #
# ---------------------------------------------------------------------------- #

motors_linked = True

frame_enabled = False
frame_RPM = 1
frame_SPS = None
frame_microstepping = None
frame_direction = 1

core_enabled = False
core_RPM = 1
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

imaging_current_count = 0

received_packets = 0

digital_zoom = 0

imaging_format = 0

x_resolution = 2592

y_resolution = 2592

default_directory = "/home/pi/Desktop"

timelapse_countdown = None

lens_position = None

capture_mode = None

custom_directory = None

full_directory = None

sequence_name = None

current_image = None

core_busy = False

# ---------------------------------------------------------------------------- #
#                             graphing delarations                             #
# ---------------------------------------------------------------------------- #
styles = {"color": "r", "font-size": "15px"}

red_pen = mkPen(color=(204, 0, 0), width=2)

green_pen = mkPen(color=(0, 204, 0), width=2)

blue_pen = mkPen(color=(0, 0, 204), width=2)

# ambient_graphing_complete = True

# motion_graphing_complete = True

# ---------------------------------------------------------------------------- #
#                          ambient sensor declarations                         #
# ---------------------------------------------------------------------------- #

ambient_temperature_graph_ref = ""

ambient_humidity_graph_ref = ""

ambient_pressure_graph_ref = ""

ambient_sensor_time_stamp = []

ambient_temperature = []

ambient_humidity = []

ambient_pressure = []

ambient_sensor_initial_time = None

ambient_sensor_interval = None

ambient_sensor_previous_time = 0

ambient_temperature_offset = 0

ambient_humidity_offset = 0

ambient_pressure_offset = 0

# ---------------------------------------------------------------------------- #
#                          motion sensor declarations                          #
# ---------------------------------------------------------------------------- #

motion_accelerometer_x_graph_ref = None

motion_accelerometer_y_graph_ref = None

motion_accelerometer_z_graph_ref = None

motion_gyroscope_x_graph_ref = None

motion_gyroscope_y_graph_ref = None

motion_gyroscope_z_graph_ref = None

motion_sensor_time_stamp = []

motion_sensor_graph_time_stamp = []

motion_acceleration_x = []

motion_acceleration_y = []

motion_acceleration_z = []

motion_acceleration_graph_x = []

motion_acceleration_graph_y = []

motion_acceleration_graph_z = []

motion_gyroscope_x = []

motion_gyroscope_y = []

motion_gyroscope_z = []

motion_gyroscope_graph_x = []

motion_gyroscope_graph_y = []

motion_gyroscope_graph_z = []

motion_sensor_initial_time = None

motion_sensor_interval = None

motion_sensor_previous_time = 0

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
