from PyQt5 import QtCore, QtGui, QtWidgets

class UI_TYPE:
    TEXT_INPUT = 0
    DROPDOWN = 1
    SPIN_BOX = 2
    CHECK_BOX = 3
    DATE_INPUT = 4

    VALUE = -1  # Use to assign a static value to the field, if it's not implemented by the UI

class UiConfigurationHelper:

    @staticmethod
    def dump_config(ui_name_to_normal_name: list) -> dict:
        data = {}
        for e in ui_name_to_normal_name:
            element_type = e[2]
            if element_type == UI_TYPE.TEXT_INPUT:
                data.update({e[0]: e[1].text()})
                continue

            if element_type == UI_TYPE.SPIN_BOX:
                data.update({e[0]: e[1].value()})
                continue

            if element_type == UI_TYPE.CHECK_BOX:
                data.update({e[0]: e[1].isChecked()})
                continue

            if element_type == UI_TYPE.DROPDOWN:
                data.update({e[0]: e[1].currentText()})
                continue

            if element_type == UI_TYPE.DATE_INPUT:
                data.update({e[0]: e[1].date().toPyDate()})
                continue

            if element_type == UI_TYPE.VALUE:
                data.update({e[0]: e[1]})
                continue

        return data

    @staticmethod
    def browse_dir(change_var) -> str:
        dst = QtWidgets.QFileDialog.getExistingDirectory()
        change_var.setText(dst)
        return dst

    @staticmethod
    def browse_file_fmt(change_var) -> str:
        dst = QtWidgets.QFileDialog.getOpenFileName()
        file_string = "file<{encoding}><{separator}>: {path}"
        fs = file_string.format(encoding="utf-8", separator=",", path=dst[0])
        change_var.setText(fs)
        return fs

    @staticmethod
    def browse_file(change_var) -> str:
        dst = QtWidgets.QFileDialog.getOpenFileName()
        change_var.setText(dst)
        return dst

    @staticmethod
    def load_config(source_config: dict, ui_name_to_normal_name: list) -> None:
        for e in ui_name_to_normal_name:
            element_type = e[2]
            if element_type == UI_TYPE.TEXT_INPUT:
                ui_name_to_normal_name[1].setText(source_config[e[0]])
                continue

            if element_type == UI_TYPE.SPIN_BOX:
                ui_name_to_normal_name[1].setValue(source_config[e[0]])
                continue

            if element_type == UI_TYPE.CHECK_BOX:
                ui_name_to_normal_name[1].setChecked(source_config[e[0]])
                continue

            # TODO: require special processing
            if element_type == UI_TYPE.DROPDOWN:
                continue

            # TODO
            if element_type == UI_TYPE.DATE_INPUT:
                continue

            # TODO: Edit the list directly, but warning maybe required
            if element_type == UI_TYPE.VALUE:  # Don't have a ui element for it
                continue
