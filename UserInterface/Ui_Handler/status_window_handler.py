import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox

from UserInterface.Ui_Scripts.status_window import Ui_StatusWindow
from UserInterface.libs.ui_config_assist import UiConfigurationHelper
from UserInterface.libs.log_window_update_helper import UiLoggingHelper


class StatusWindowHandler(Ui_StatusWindow):

    def __init__(self, name):
        super(StatusWindowHandler, self).__init__()
        self.ui_helper = UiLoggingHelper()
        self._window = QtWidgets.QMainWindow()
        self.setupUi(self._window)
        self.bind_buttons()
        self.bind_signals()

        self.status_window_name = name
        self._window.setWindowTitle(self.status_window_name)

        self._raw_message = ""

    def show_window(self):
        self._window.show()

    def log_message(self, msg):
        pass

    def export_logs(self):
        try:
            dst = UiConfigurationHelper.browse_dir()  # Get the folder the log is going to be saved into
            dst = os.path.join(dst, f"{self.status_window_name}_export.log")
            with open(dst, "wb") as file:
                file.write(self._raw_message.encode("utf-8"))
            ret = QMessageBox.information(self._window, "Success", "Successfully exported log to: {}".format(dst))
        except (FileNotFoundError, PermissionError) as e:
            QMessageBox.critical(self._window, "Error", "Error while exporting logs: {}".format(e))

    def clear_log_window(self):
        self.log_window.setText("")

    def bind_buttons(self):
        self.logs_clear_window.clicked.connect(self.clear_log_window)
        self.logs_export.clicked.connect(self.export_logs)
        self.terminate_current_task.clicked.connect(self.debug_s_s)

    def bind_signals(self):
        self.ui_helper.log_event.connect(self.update_log_window)

    def update_log_window(self, msg):
        self.log_window.append(msg)

    def debug_s_s(self):
        self.ui_helper.log_event.emit("Test")
