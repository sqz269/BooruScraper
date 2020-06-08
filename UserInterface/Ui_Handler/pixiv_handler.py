from PyQt5 import QtCore, QtGui, QtWidgets
from UserInterface.Ui_Scripts.pixiv_window import Ui_PixivConfigurationWindow
from UserInterface.libs.IModuleConfigWindowHandler import IModuleConfigWindowHandler

class PixivConfigurationWindowHandler(Ui_PixivConfigurationWindow, IModuleConfigWindowHandler):


    def __init__(self):
        super().__init__()
        self._window = QtWidgets.QMainWindow()
        self.setupUi(self._window)

    def show_config(self):
        self._window.show()

    def load_config(self):
        return super().load_config()

    def save_config(self):
        return super().save_config()
