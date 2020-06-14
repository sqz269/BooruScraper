import sys

from PyQt5.QtWidgets import QMessageBox

from UserInterface.Ui_Handler.module_selection_handler import ModuleSelectionWindowHandler

from PyQt5 import QtCore, QtGui, QtWidgets

from traceback import format_tb

import sys


def global_exception_handler(exctype, value, traceback):
    tb = "\n".join(format_tb(traceback))
    QMessageBox.critical(None, "Unhandled Exception",
                         f"Exception Type: {exctype.__name__}\nException Message: {value}\n\n"
                         f"---------------\nTraceback:\n {tb}---------------\n\n\nPress OK to Exit")
    raise SystemExit(1)


sys.excepthook = global_exception_handler

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    module_selection_handler = ModuleSelectionWindowHandler()
    module_selection_handler.show_window()

    sys.exit(app.exec_())
