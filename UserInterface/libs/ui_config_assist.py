from PyQt5 import QtCore, QtGui, QtWidgets
import configparser

from Scraper.libs.cfgBuilder import ConfigurationBuilder

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
    def load_config(source_config: dict, ui_name_to_normal_name: list, combox_cfg_name_to_index: dict) -> list:
        for e in ui_name_to_normal_name:
            element_type = e[2]
            if element_type == UI_TYPE.TEXT_INPUT:
                e[1].setText(source_config[e[0].lower()])
                continue

            if element_type == UI_TYPE.SPIN_BOX:
                try:
                    e[1].setValue(float(source_config[e[0].lower()]))
                except ValueError:
                    e[1].setValue(0)
                continue

            if element_type == UI_TYPE.CHECK_BOX:
                e[1].setChecked(ConfigurationBuilder.boolean(source_config[e[0].lower()]))
                continue

            if element_type == UI_TYPE.DROPDOWN:
                source_value = source_config[e[0].lower()]
                config_name_2_index = combox_cfg_name_to_index[e[0]]
                e[1].setCurrentIndex(config_name_2_index[source_value])

            if element_type == UI_TYPE.DATE_INPUT:
                continue

            # TODO: Edit the list directly, but warning maybe required
            if element_type == UI_TYPE.VALUE:  # Don't have a ui element for it
                continue

    @staticmethod
    def set_combo_box_item(combo_box, original_name, readable_name_to_org_name):
        pass

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
    def browse_file(change_var=None) -> str:
        dst = QtWidgets.QFileDialog.getOpenFileName()
        if (change_var):
            change_var.setText(dst)
        return dst

    @staticmethod
    def parse_ini_config(cfg) -> dict:
        parser = configparser.ConfigParser()
        if not parser.read(cfg, encoding="utf-8"): return {}
        cfg = {}
        for sections in parser.sections():
            for keys in parser[sections]:
                cfg.update({keys: parser[sections][keys]})
        return cfg
