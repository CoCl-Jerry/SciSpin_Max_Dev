import General
import Functions
import UI_Update
import Threads
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5

import os


def start_cycle(self):
    General.on_duration = self.lighting_on_duration_value_spinBox.value()
    General.off_duration = self.lighting_off_duration_value_spinBox.value()

    if not General.cycle_thread_running:
        try:
            self.Cycle_Thread = Threads.Cycle()
            self.Cycle_Thread.started.connect(
                lambda: UI_Update.cycle_start(self))
            self.Cycle_Thread.finished.connect(
                lambda: UI_Update.cycle_end(self))

            self.Cycle_Thread.start()

        except Exception as e:
            print(e, "cycle failure, please contact Jerry for support")
    else:
        General.cycle_thread_running = False


def start_capture(self, mode):
    if mode == 0:
        General.capture_mode = 0
    elif mode == 1:
        General.capture_mode = 1
    elif mode == 2:
        General.capture_mode = 2
    elif mode == 3:
        General.capture_mode = 3
    elif mode == 4:
        General.capture_mode = 4

    self.Capture_Thread = Threads.Capture()
    self.Capture_Thread.transmit.connect(
        lambda: UI_Update.transmit_update(self))
    self.Capture_Thread.started.connect(
        lambda: UI_Update.capture_start(self))
    self.Capture_Thread.finished.connect(
        lambda: UI_Update.capture_complete(self))

    self.Capture_Thread.start()


def ambient_sensors(self):
    if not General.ambient_thread_running:
        self.Ambient_Thread = Threads.Ambient()
        self.Ambient_Thread.started.connect(
            lambda: UI_Update.ambient_UI_toggle(self))
        self.Ambient_Thread.started.connect(
            lambda: UI_Update.ambient_sensor_reset(self)
        )
        self.Ambient_Thread.finished.connect(
            lambda: UI_Update.ambient_UI_toggle(self))
        self.Ambient_Thread.initialized.connect(
            lambda: UI_Update.ambient_sensor_initialize(self)
        )
        self.Ambient_Thread.ambient_sensor_update.connect(
            lambda: UI_Update.ambient_sensor_update(self)
        )

        General.ambient_thread_running = True
        self.Ambient_Thread.start()
    else:
        General.ambient_thread_running = False


def motion_sensors(self):
    if not General.motion_thread_running:
        self.Motion_Thread = Threads.Motion()
        self.Motion_Thread.started.connect(
            lambda: UI_Update.motion_UI_toggle(self))
        self.Motion_Thread.started.connect(
            lambda: UI_Update.motion_sensor_reset(self)
        )
        self.Motion_Thread.finished.connect(
            lambda: UI_Update.motion_UI_toggle(self))
        self.Motion_Thread.initialized.connect(
            lambda: UI_Update.motion_sensor_initialize(self)
        )
        self.Motion_Thread.motion_sensor_update.connect(
            lambda: UI_Update.motion_sensor_update(self)
        )

        General.motion_thread_running = True
        self.Motion_Thread.start()
    else:
        General.motion_thread_running = False


# def start_timelapse(self):

#     if not Settings.timelapse_running:
#         self.Timelapse_Thread = Threads.Timelapse()
#         self.Timelapse_Thread.transmit.connect(
#             lambda: UI_Update.transmit_update(self))

#         self.Timelapse_Thread.started.connect(
#             lambda: UI_Update.timelapse_start(self))
#         self.Timelapse_Thread.captured.connect(
#             lambda: UI_Update.image_captured(self))
#         self.Timelapse_Thread.transmitstart.connect(
#             lambda: UI_Update.transmitst(self))
#         self.Timelapse_Thread.finished.connect(
#             lambda: UI_Update.timelapse_end(self))

#         self.Timelapse_Thread.start()

#     else:
#         Settings.timelapse_running = False
#         self.Progress_Bar.setValue(Settings.current + 1)


# def sensor_init(self):

#     if Functions.check_connection():
#         self.core_status_label.setText("Core Status: Online")
#     else:
#         error = PyQt5.QtGui.QImage("../_image/Error.png")
#         self.Image_Frame.setPixmap(QtGui.QPixmap(error))

#     os.system("i2cdetect -y 1 > ../_temp/output.txt")

#     if '1d' in open('../_temp/output.txt').read():
#         Settings.acc_attached = True
#     if '76' in open('../_temp/output.txt').read():
#         Settings.temp_attached = True

#     if Settings.temp_attached or Settings.acc_attached:
#         self.Sensor_Thread = Threads.Sensor()
#         self.Sensor_Thread.update.connect(
#             lambda: UI_Update.sensor_update(self))
#         self.Sensor_Thread.logstart.connect(
#             lambda: UI_Update.sensor_logstart(self))
#         self.Sensor_Thread.logdone.connect(
#             lambda: UI_Update.sensor_logdone(self))
#         self.Sensor_Thread.start()
