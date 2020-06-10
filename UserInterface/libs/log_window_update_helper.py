from PyQt5.QtCore import QObject, pyqtSignal


class UiLoggingHelper(QObject):
    log_event = pyqtSignal(str, str, int, str)
