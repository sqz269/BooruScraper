import logging
import threading
from typing import Any, Optional, Dict
from traceback import format_tb

from UserInterface.Ui_Handler.status_window_handler import StatusWindowHandler
from UserInterface.libs.log_window_update_helper import UiLoggingHelper

from PyQt5.QtWidgets import QMainWindow, QMessageBox

"""
How does this file work

This file contains a class that Inherited from the Logger object, so it can override some basic logging methods
such as `debug, info, warning, error, exception, critical` logging methods,
These methods were overridden because we want to redirect the normal logging output (CLI) to our GUI
so when our Scraper components call the logging methods, we can effectively catch such message and
output it to the GUI element.

? Why don't just redirect stdout and stderr ?
It's harder to redirect stdout and stderr if we are running the scraper with multiprocessing
and it might require some changes within the scraper module and framework, which i didn't want to do
also the original logging method have ANSI escape sequences to render colors which makes harder to format to GUI text

But to make the scraper components to use this class, we have to first replace it's original logger
that it initialized during the call `init_scraper_base` and discard the old one

For example initialization of scraper when in gui mode:
    module = init_scraper_base(ComponentPixiv)  # This will also initialize a logger with it
    gui_logger = UiLogger("Pixiv GUI", self._status_window)  # Initialize the logger to redirect messages
    module.logger = gui_logger # Replace the default logger with our UI logger
    module.run()  # Run the module
"""


class UiLogger(logging.Logger):

    def __init__(self, name: str, status_window: StatusWindowHandler):
        """
        Initializes the logger for UI

        Args:
            name: The logger name, Totally useless, but it's to satisfy logging.Logger's init args
            status_window: The status window where it displays the scraper's status (Should be from status_window.py)
        """
        super(UiLogger, self).__init__(name, logging.NOTSET)

        self.ui_helper = UiLoggingHelper()

        self._status_window: StatusWindowHandler = status_window

        self._info_count = 0
        self._warn_count = 0
        self._error_count = 0
        self._counter_lock = threading.Lock()

        self._error_message_style = '<p style=" margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; '\
                                    '-qt-block-indent:0; text-indent:0px;"><span style=" color:#ff0000;">{time} [ERROR] ' \
                                    '</span><span style=" color:#000000;">{message}</span></p> '
        self._warning_message_style = '<p style=" margin-top:5px; margin-bottom:5px; margin-left:0px; ' \
                                      'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" ' \
                                      'color:#ffaa00;">{time} [WARNING]</span><span style=" color:#000000;">{message}</span></p>'
        self._info_message_style = '<p style=" margin-top:5px; margin-bottom:5px; margin-left:0px; margin-right:0px; ' \
                                   '-qt-block-indent:0; text-indent:0px;"><span style=" color:#0000ff;">{time} [INFO]'\
                                   '</span><span style=" color:#000000;">{message}</span></p></body></html> '

    @property
    def info_count(self):
        return self._info_count

    @property
    def warn_count(self):
        return self._warn_count

    @property
    def error_count(self):
        return self._error_count

    def debug(self, msg: Any, *args: Any, exc_info=...,
              stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
              **kwargs: Any) -> None:
        # Drop Debug messages as we don't need such level of details with GUI mode
        pass

    def info(self, msg: Any, *args: Any, exc_info=...,
             stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
             **kwargs: Any) -> None:
        self._counter_lock.acquire()
        self._info_count += 1
        self._counter_lock.release()

        fmt_msg = self._info_message_style.format(message=msg)

        self.ui_helper.log_event.emit(fmt_msg)

    def warning(self, msg, *args, **kwargs):
        self._counter_lock.acquire()
        self._warn_count += 1
        self._counter_lock.release()

        fmt_msg = self._warning_message_style.format(message=msg)

    def error(self, msg: Any, *args: Any, exc_info=...,
              stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
              **kwargs: Any) -> None:
        self._counter_lock.acquire()
        self._error_count += 1
        self._counter_lock.release()

        fmt_msg = self._error_message_style.format(message=msg)

    def exception(self, msg: Any, *args: Any, exc_info=...,
                  stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
                  **kwargs: Any) -> None:
        self._counter_lock.acquire()
        self._error_count += 1
        self._counter_lock.release()

        exec_tb = format_tb()

        QMessageBox(QMessageBox.Critical, f"{msg}", f"An Exception Occurred:\n{exec_tb}", QMessageBox.Ok)

    def critical(self, msg: Any, *args: Any, exc_info=...,
                 stack_info: bool = ..., stacklevel: int = ..., extra: Optional[Dict[str, Any]] = ...,
                 **kwargs: Any) -> None:
        pass

    fatal = critical

    def append_message(self, msg):
        pass

if __name__ == "__main__":
    # level does not matter
    ul = UiLogger("Test", logging.NOTSET)
    # None of the statement should be printing anything to the stdout
    ul.critical("This is a CRITICAL level entry")
    ul.error("This is a ERROR level entry")
    ul.warning("This is a WARNING level entry")
    ul.info("This is a INFO level entry")
    ul.debug("This is a DEBUG level entry")
