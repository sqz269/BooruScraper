from PyQt5 import QtCore, QtGui, QtWidgets
from UserInterface.Ui_Scripts.module_selection import Ui_ModuleSelectionWindow

from UserInterface.Ui_Handler.pixiv_handler import PixivConfigurationWindowHandler

class ModuleSelectionWindowHandler(Ui_ModuleSelectionWindow):


    def __init__(self):
        super().__init__()
        self._window = QtWidgets.QMainWindow()
        self.setupUi(self._window)

        self.pixiv_config_window_handler = PixivConfigurationWindowHandler()
        self.bind_pixiv_elements()

    def bind_pixiv_elements(self):
        self.pixiv_config_show.clicked.connect(self.pixiv_config_window_handler.show_config)

    def show_window(self):
        self._window.show()
