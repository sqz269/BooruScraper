from PyQt5 import QtWidgets

from UserInterface.Ui_Handler.pixiv_handler import \
    PixivConfigurationWindowHandler
from UserInterface.Ui_Scripts.module_selection import Ui_ModuleSelectionWindow


class ModuleSelectionWindowHandler(Ui_ModuleSelectionWindow):

    def __init__(self):
        super().__init__()
        # Initialize the module selection window
        self._window = QtWidgets.QMainWindow()
        self.setupUi(self._window)

        # Initialize the pixiv's config window and bind buttons with it's function
        # You can take a look at PixivConfigurationWindowHandler() to see how it's structured.
        # it's far from perfect but it works
        self.pixiv_config_window_handler = PixivConfigurationWindowHandler()
        self.bind_pixiv_elements()

    def bind_pixiv_elements(self):
        self.pixiv_config_show.clicked.connect(self.pixiv_config_window_handler.show_config)
        self.pixiv_config_load.clicked.connect(self.pixiv_config_window_handler.load_config)
        self.pixiv_config_save.clicked.connect(self.pixiv_config_window_handler.dump_config)
        self.pixiv_status_show_detail.clicked.connect(self.pixiv_config_window_handler.show_status_window)

        # We use a lambda expression (anonymous function) here to pass extra arguments when the function is called
        self.pixiv_config_window_handler.status_window.ui_helper.scrape_event.connect(
            lambda event_name:
            self.pixiv_config_window_handler.status_window.update_overall_status(event_name, self.pixiv_status_current))

    def show_window(self):
        self._window.show()
