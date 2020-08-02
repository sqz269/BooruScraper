import sys
from traceback import format_tb

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from Analyser import tags_analyser
from UserInterface.Ui_Scripts.tags_analyser_ui import Ui_TagAnalyser
from UserInterface.libs.ui_config_assist import UiConfigurationHelper


class TagsAnalyser(Ui_TagAnalyser):

    def __init__(self):
        self._window = QtWidgets.QMainWindow()
        # Instantiate window elements to the new MainWindow instance we just created
        self.setupUi(self._window)

        self.bind_freq_tag_element()
        self.bind_tag_diff_element()

    def bind_freq_tag_element(self):
        self.freq_csv_path_browse.clicked.connect(lambda: UiConfigurationHelper.browse_file(self.freq_csv_path))
        self.freq_output_csv_path_browse.clicked.connect(
            lambda: UiConfigurationHelper.browse_file(self.freq_output_csv_path))
        self.freq_process_target.clicked.connect(self.freq_tag_start)

    def bind_tag_diff_element(self):
        self.tag_diff_csv_path_browse.clicked.connect(lambda: UiConfigurationHelper.browse_file(self.tag_diff_csv_path))
        self.tag_diff_file_dir_browse.clicked.connect(lambda: UiConfigurationHelper.browse_dir(self.tag_diff_file_dir))
        self.tag_diff_output_csv_path_browse.clicked.connect(
            lambda: UiConfigurationHelper.browse_file(self.tag_diff_output_csv_path))
        self.tag_diff_process_target.clicked.connect(self.tag_diff_start)

    def freq_tag_start(self):
        dst_csv = self.freq_csv_path.text()
        src_csv = self.freq_output_csv_path.text()
        threshold = self.freq_tag_threshold.value()
        tags_col_name = self.freq_tag_col_name.text()
        delimiter = self.freq_csv_delimiter.text()
        tags_analyser.find_most_frequent_tags(src_csv, dst_csv, threshold, delimiter, tags_col_name)

    def tag_diff_start(self):
        dst_csv = self.tag_diff_output_csv_path.text()  # TODO: Handle cases where path is inaccessible or doesn't exist
        files_dir = self.tag_diff_file_dir.text()
        src_csv = self.tag_diff_csv_path.text()
        threshold = self.tag_diff_tag_threshold.value()
        tags_col_name = self.tag_diff_tag_col_name.text()
        delimiter = self.tag_diff_csv_delimiter.text()
        file_format_string = self.tag_diff_file_format_string.text()
        image_id_col_name = self.tag_diff_image_id_col_name.text()
        tags_analyser.find_diff_del(src_csv, files_dir, dst_csv, file_format_string, threshold, delimiter,
                                    image_id_col_name, tags_col_name)

    def show_window(self):
        self._window.show()


def exc_hook(exctype, value, traceback):
    tb = "\n".join(format_tb(traceback))
    QMessageBox.critical(None, "Unhandled Exception",
                         f"Exception Type: {exctype.__name__}\nException Message: {value}\n\n"
                         f"---------------\nTraceback:\n {tb}---------------\n\n\nPress OK to Exit")
    raise SystemExit(1)


if __name__ == "__main__":
    sys.excepthook = exc_hook
    app = QtWidgets.QApplication(sys.argv)

    module_selection_handler = TagsAnalyser()
    module_selection_handler.show_window()

    sys.exit(app.exec_())
