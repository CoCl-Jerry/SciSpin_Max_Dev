from PyQt5.QtGui import QPalette, QColor, QImage

# ---------------------------------------------------------------------------- #
#                       start of UI pallette declarations                      #
# ---------------------------------------------------------------------------- #
global palette_red
palette_red = QPalette()
palette_red.setColor(QPalette.WindowText, QColor(255, 0, 0))

global palette_green
palette_green = QPalette()
palette_green.setColor(QPalette.WindowText, QColor(0, 255, 0))

# ---------------------------------------------------------------------------- #
#                       start of error image declarations                      #
# ---------------------------------------------------------------------------- #
global camera_error_image
camera_error_image = QImage("../_image/camera_error.png")

# ---------------------------------------------------------------------------- #
#                      start of system status declarations                     #
# ---------------------------------------------------------------------------- #
global camera_status
camera_status = False

global motor_status
motor_status = False

global sensor_status
sensor_status = False

global acc_status
acc_status = False

global storage_remaining
storage_remaining = "N/A"

# ---------------------------------------------------------------------------- #
#                         start of general declarations                        #
# ---------------------------------------------------------------------------- #
