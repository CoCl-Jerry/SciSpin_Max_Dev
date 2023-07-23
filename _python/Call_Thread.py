import General
import UI_Update
import Threads


import os


def start_cycle(self):
    General.on_duration = self.lighting_on_duration_value_spinBox.value()
    General.off_duration = self.lighting_off_duration_value_spinBox.value()

    if not General.cycle_thread_running:
        self.Cycle_Thread = Threads.Cycle()
        self.Cycle_Thread.started.connect(
            lambda: UI_Update.cycle_start(self))
        self.Cycle_Thread.finished.connect(
            lambda: UI_Update.cycle_end(self))
        self.Cycle_Thread.countdown.connect(
            lambda: UI_Update.cycle_countdown(self))

        self.Cycle_Thread.start()

    else:
        General.cycle_thread_running = False


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

# ---------------------------------------------------------------------------- #
#                             imaging call threads                             #
# ---------------------------------------------------------------------------- #


def start_capture(self, mode):
    General.capture_mode = mode
    self.Capture_Thread = Threads.Capture()
    self.Capture_Thread.transmit.connect(
        lambda: UI_Update.transmit_update(self))
    self.Capture_Thread.started.connect(
        lambda: UI_Update.image_capture_toggle(self, 1))
    self.Capture_Thread.finished.connect(
        lambda: UI_Update.image_capture_toggle(self, 0))

    self.Capture_Thread.start()


def start_timelapse(self):

    if not General.timelapse_thread_running:
        self.Timelapse_Thread = Threads.Timelapse()
        self.Timelapse_Thread.transmit.connect(
            lambda: UI_Update.transmit_update(self))
        self.Timelapse_Thread.capturing.connect(
            lambda: UI_Update.timelapse_capture_toggle(self, 1))
        self.Timelapse_Thread.captured.connect(
            lambda: UI_Update.timelapse_capture_toggle(self, 0))
        self.Timelapse_Thread.countdown.connect(
            lambda: UI_Update.timelapse_countdown(self))

        self.Timelapse_Thread.started.connect(
            lambda: UI_Update.timelapse_toggle(self, 1))
        self.Timelapse_Thread.finished.connect(
            lambda: UI_Update.timelapse_toggle(self, 0))

        self.Timelapse_Thread.start()

    else:
        General.timelapse_thread_running = False
