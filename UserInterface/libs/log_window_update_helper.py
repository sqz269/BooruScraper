from PyQt5.QtCore import QObject, pyqtSignal

class ScraperEvent:
    IN_PROGRESS = 0
    CLEANING_UP = 1
    COMPLETED = 2

class UiLoggingHelper(QObject):
    # Log message, Normal Message, Level Count, Level Name
    log_event = pyqtSignal(str, str, int, str)

    # Total pages completed
    page_complete = pyqtSignal(int)

    # Event Name
    scrape_event = pyqtSignal(int)
