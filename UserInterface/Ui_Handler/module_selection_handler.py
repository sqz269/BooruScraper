from PyQt5 import QtCore, QtGui, QtWidgets

from UserInterface.libs.ui_config_assist import UiConfigurationHelper
from UserInterface.Ui_Handler.pixiv_handler import \
    PixivConfigurationWindowHandler
from UserInterface.Ui_Scripts.module_selection import Ui_ModuleSelectionWindow


class ModuleSelectionWindowHandler(Ui_ModuleSelectionWindow):


    def __init__(self):
        super().__init__()
        self._window = QtWidgets.QMainWindow()
        self.setupUi(self._window)

        self.pixiv_config_window_handler = PixivConfigurationWindowHandler()
        self.bind_pixiv_elements()

        self.configuration_dir_browse.clicked.connect(lambda: UiConfigurationHelper.browse_dir(self.configuration_dir))

    def bind_pixiv_elements(self):
        self.pixiv_config_show.clicked.connect(self.pixiv_config_window_handler.show_config)
        self.pixiv_config_load.clicked.connect(self.pixiv_config_window_handler.load_config)
        self.pixiv_config_save.clicked.connect(self.pixiv_config_window_handler.dump_config)
        self.pixiv_status_show_detail.clicked.connect(self.pixiv_config_window_handler.show_status_window)

    def show_window(self):
        self._window.show()
