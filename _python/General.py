from PyQt5.QtGui import QPalette, QColor, QImage

# ---------------------------------------------------------------------------- #
#                       start of UI pallette declarations                      #
# ---------------------------------------------------------------------------- #
palette_red = QPalette()
palette_red.setColor(QPalette.WindowText, QColor(255, 0, 0))

palette_green = QPalette()
palette_green.setColor(QPalette.WindowText, QColor(0, 255, 0))

# ---------------------------------------------------------------------------- #
#                       start of error image declarations                      #
# ---------------------------------------------------------------------------- #
camera_error_image = QImage("../_image/camera_error.png")

storage_critical_error_image = QImage("../_image/storage_critical_error.png")

# ---------------------------------------------------------------------------- #
#                      system status address declarations                      #
# ---------------------------------------------------------------------------- #
core_address = '10.0.5.1'

MCU_address = 0x08

ambient_sensor_address = 0x76

motion_sensor_address = 0x6A
# ---------------------------------------------------------------------------- #
#                         start of general declarations                        #
# ---------------------------------------------------------------------------- #
