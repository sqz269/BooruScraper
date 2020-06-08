import sys

from UserInterface.Ui_Handler.module_selection_handler import ModuleSelectionWindowHandler

from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    module_selection_handler = ModuleSelectionWindowHandler()
    module_selection_handler.show_window()

    sys.exit(app.exec_())
