import os
from multiprocessing import Process

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from Scraper import ComponentPixiv
from Scraper.framework.framework import init_scraper_base
from UserInterface.libs.i_config_window_handler import IConfigWindowHandler
from UserInterface.Ui_Handler.status_window_handler import StatusWindowHandler
from UserInterface.libs.ui_config_assist import UI_TYPE, UiConfigurationHelper
from UserInterface.Ui_Scripts.pixiv_window import Ui_PixivConfigurationWindow
from UserInterface.libs.custom_logger import UiLogger


class PixivConfigurationWindowHandler(Ui_PixivConfigurationWindow, IConfigWindowHandler):

    def __init__(self):
        super().__init__()
        self._window = QtWidgets.QMainWindow()
        self.setupUi(self._window)

        self._status_window: StatusWindowHandler = StatusWindowHandler("Pixiv Status")

        self.bind_elements()

        self.UI_CONFIG_NAME_TO_NORMAL_NAME = None
        self.COMBO_BOX_SETTING_NAME_TO_INDEX = None
        self.init_config_vars()

        self.config_file_path = None

        self._active_scraping_process: Process = None

    def init_config_vars(self):

        self.UI_CONFIG_NAME_TO_NORMAL_NAME = [
            #   Original name,              Variable name,                  Type
            ["TAGS_QUERY",              self.pixiv_query_tags,          UI_TYPE.TEXT_INPUT],
            ["TAGS_EXCLUDE_QUERY",      self.pixiv_query_tags_exclude,  UI_TYPE.TEXT_INPUT],
            ["SEARCH_MODE",             self.pixiv_search_mode,         UI_TYPE.DROPDOWN],
            ["SUBMISSION_TYPE",         self.pixiv_submission_type,     UI_TYPE.DROPDOWN],
            ["RATING",                  self.pixiv_rating,              UI_TYPE.DROPDOWN],
            ["HEIGHT_MIN",              self.pixiv_query_min_height,    UI_TYPE.SPIN_BOX],
            ["WIDTH_MIN",               self.pixiv_query_min_width,     UI_TYPE.SPIN_BOX],
            ["HEIGHT_MAX",              self.pixiv_query_max_height,    UI_TYPE.SPIN_BOX],
            ["WIDTH_MAX",               self.pixiv_query_max_width,     UI_TYPE.SPIN_BOX],
            ["ORIENTATION",             self.pixiv_query_orientation,   UI_TYPE.TEXT_INPUT],

            # Because tags_query_exclude doesn't work so it's just a temp work around
            ["TAGS_EXCLUDE",            self.pixiv_query_tags_exclude,  UI_TYPE.TEXT_INPUT],
            ["VIEW_MIN",                self.pixiv_min_view,            UI_TYPE.SPIN_BOX],
            ["BOOKMARK_MIN",            self.pixiv_min_bookmark,        UI_TYPE.SPIN_BOX],
            # Make following spin box
            ["AVG_VIEW_PER_DAY",        self.pixiv_avg_view_per_day,    UI_TYPE.TEXT_INPUT],
            ["VIEW_BOOKMARK_RATIO",     self.pixiv_view_bookmark_ratio, UI_TYPE.SPIN_BOX],
            ["AVG_BOOKMARK_PER_DAY",    self.pixiv_avg_bookmark_per_day,UI_TYPE.TEXT_INPUT],
            ["USER_EXCLUDE",            self.pixiv_user_exclude,        UI_TYPE.TEXT_INPUT],
            ["IGNORE_BOOKMARKED",       self.pixiv_ignore_bookmarked,   UI_TYPE.CHECK_BOX],
            ["PAGE_COUNT_MIN",          self.pixiv_min_page_count,      UI_TYPE.SPIN_BOX],
            ["PAGE_COUNT_MAX",          self.pixiv_max_page_count,      UI_TYPE.SPIN_BOX],

            ["START_PAGE",              self.pixiv_start_page,          UI_TYPE.SPIN_BOX],
            ["END_PAGE",                self.pixiv_end_page,            UI_TYPE.SPIN_BOX],
            ["REVERSE_GENERATED_URL",   self.pixiv_reverse_generated_url, UI_TYPE.CHECK_BOX],
            ["SORTED_BY",               self.pixiv_submission_sort_by,  UI_TYPE.DROPDOWN],
            ["SUBMISSION_BEFORE",       self.pixiv_submission_before,   UI_TYPE.DATE_INPUT],
            ["SUBMISSION_AFTER",        self.pixiv_submission_after,    UI_TYPE.DATE_INPUT],
            ["PHPSESSID",               self.pixiv_phpsessid,           UI_TYPE.TEXT_INPUT],
            ["SAVE_PATH",               self.pixiv_output_folder,       UI_TYPE.TEXT_INPUT],
            ["MASTER_DIRECTORY_NAME_STRING", self.pixiv_master_directory_string, UI_TYPE.TEXT_INPUT],
            ["FILENAME_STRING",         self.pixiv_file_name_string,    UI_TYPE.TEXT_INPUT],
            ["CSV_ENTRY_STRING",        self.pixiv_csv_entry_string,    UI_TYPE.TEXT_INPUT],

            ["MAX_CONCURRENT_THREAD",   self.pixiv_max_concurrent_thread, UI_TYPE.SPIN_BOX],
            # TODO Make this delay a double spin
            ["DOWNLOAD_DELAY",          self.pixiv_download_delay,      UI_TYPE.SPIN_BOX],
            ["DELAY_START",             self.pixiv_start_delay,         UI_TYPE.SPIN_BOX],
            ["READ_IMG_INFO_DELAY",     self.pixiv_read_image_info_delay,UI_TYPE.SPIN_BOX],
            ["COLLECT_DATA_ONLY",       self.pixiv_collect_data_only,   UI_TYPE.CHECK_BOX],
            ["USER_AGENT",              self.pixiv_user_agent,          UI_TYPE.TEXT_INPUT],
            ["IMAGE_SIZE",              self.pixiv_image_size,          UI_TYPE.DROPDOWN],
            ["FLUSH_CSV_IMMINENTLY",    self.pixiv_flush_csv_imminently,UI_TYPE.CHECK_BOX],
            ["USE_SUBMISSION_SPECIFIC_DIRECTORY", self.pixiv_use_submission_specific_dir, UI_TYPE.CHECK_BOX],

            ["MERGE_FILE",              self.pixiv_merge_files,         UI_TYPE.CHECK_BOX],
            ["MERGE_FILE_KEEP_SEPARATE",self.pixiv_merge_files_keep_copy,UI_TYPE.CHECK_BOX],

            # not implemented in UI, because im LAZY
            ["TOOL",                    "",                             UI_TYPE.VALUE],
            ["TAGS_BYPASS",             "",                             UI_TYPE.VALUE],
            ["NON_QUERY_TAG_MATCH_MODE","absolute",                     UI_TYPE.VALUE],
            ["VIEW_BOOKMARK_RATIO_BYPASS", 9999999,                     UI_TYPE.VALUE],
            ["TITLE_INCLUDE",           "",                             UI_TYPE.VALUE],
            ["TITLE_EXCLUDE",           "",                             UI_TYPE.VALUE],
            ["USER_INCLUDE",            "",                             UI_TYPE.VALUE],
            ["DESCRIPTION_EXCLUDE",     "",                             UI_TYPE.VALUE],
            ["COMPRESS",                False,                          UI_TYPE.VALUE],

            # Logger init params, we won't be using this: see libs/custom_logger.py for details
            ["LOGGER_FILE",             0,                              UI_TYPE.VALUE],
            ["LOGGER_STDOUT",           0,                              UI_TYPE.VALUE],
            ["LOGGER_NAME",             "pixiv",                        UI_TYPE.VALUE]
        ]

        self.COMBO_BOX_SETTING_NAME_TO_INDEX = {
            "SEARCH_MODE": {"s_tag_full": 0,
                            "s_tag": 1,
                            "s_tc": 2},

            "SUBMISSION_TYPE": {"all": 0,
                                "illust_and_ugoira": 1,
                                "illust": 2,
                                "manga": 3,
                                "ugoira": 4},

            "RATING":  {"all": 0,
                        "safe": 1,
                        "r18": 2},

            "SORTED_BY": {"date_d": 0,
                          "date": 1},

            "IMAGE_SIZE": {"original": 0,
                           "large": 1,
                           "medium": 2,
                           "square_medium": 3}
        }

    def bind_elements(self):
        self.pixiv_query_tags_browse.clicked.connect(
            lambda: UiConfigurationHelper.browse_file_fmt(self.pixiv_query_tags))

        self.pixiv_query_tags_exclude_browse.clicked.connect(
            lambda: UiConfigurationHelper.browse_file_fmt(self.pixiv_query_tags_exclude))

        self.pixiv_user_exclude_browse.clicked.connect(
            lambda: UiConfigurationHelper.browse_file_fmt(self.pixiv_user_exclude))

        self.pixiv_output_folder_browse.clicked.connect(
            lambda: UiConfigurationHelper.browse_dir(self.pixiv_output_folder))

        self.pixiv_view_status_detail.clicked.connect(self.show_status_window)

        self.pixiv_action_load_config.triggered.connect(self.load_config)
        self.pixiv_action_save_config.triggered.connect(self.save_config)

    def show_status_window(self):
        self._status_window.show_window()

    def show_config(self):
        self._window.show()

    def load_config(self, config_dir=None):
        ini_path = UiConfigurationHelper.browse_file()

        if not ini_path:
            return

        cfg_dict = UiConfigurationHelper.parse_ini_config(ini_path)

        UiConfigurationHelper.load_config(cfg_dict, self.UI_CONFIG_NAME_TO_NORMAL_NAME, self.COMBO_BOX_SETTING_NAME_TO_INDEX)

    def save_config(self):
        dst = UiConfigurationHelper.browse_file()
        if not dst:
            return

        config = UiConfigurationHelper.dump_config(self.UI_CONFIG_NAME_TO_NORMAL_NAME, self.COMBO_BOX_SETTING_NAME_TO_INDEX)
        UiConfigurationHelper.save_config(config, dst)
        QMessageBox.information(self._window, "Success", f"Successfully exported current configuration to:\n{dst}")

    def start_scrape(self):
        # Subprocess may be required
        pixiv_scraper = init_scraper_base(ComponentPixiv)
        pixiv_scraper.logger = UiLogger("Pixiv")  # Replace the logger, see custom_logger.py for details
        pixiv_scraper.entry_point(pixiv_scraper) # Alias for pixiv_scraper.run() if entry_point is not overridden
        self._active_scraping_process = Process(target=pixiv_scraper.entry_point, args=(pixiv_scraper, ))
        self._active_scraping_process.start()

    def terminate(self):
        self._active_scraping_process.kill()
        self._active_scraping_process = None
