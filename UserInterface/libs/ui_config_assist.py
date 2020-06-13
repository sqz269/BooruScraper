from PyQt5 import QtCore, QtGui, QtWidgets
import configparser

from PyQt5.QtWidgets import QMessageBox

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
    def dump_config(ui_name_to_normal_name: list, combo_box_config_to_index: dict, key_to_lower=True) -> dict:
        data = {}
        for e in ui_name_to_normal_name:
            element_type = e[2]
            key = e[0].lower() if key_to_lower else e[0]
            if element_type == UI_TYPE.TEXT_INPUT:
                data.update({key: e[1].text()})
                continue

            if element_type == UI_TYPE.SPIN_BOX:
                data.update({key: e[1].value()})
                continue

            if element_type == UI_TYPE.CHECK_BOX:
                data.update({key: e[1].isChecked()})
                continue

            if element_type == UI_TYPE.DROPDOWN:
                setting_2_index = combo_box_config_to_index[e[0]]  # use the original variable to keep consistency
                current_ind = e[1].currentIndex()

                normal_value = None
                for k, v in setting_2_index.items():
                    if v == current_ind:
                        normal_value = k
                        break
                else:
                    QMessageBox.critical(None, "Error", "Failed to dump configuration."\
                                                        f"\nCannot find key associated with index {current_ind}"
                                                        f"Configuration Name: {e[0]}")
                    raise SystemExit(1)

                data.update({key: normal_value})
                continue

            if element_type == UI_TYPE.DATE_INPUT:
                data.update({key: e[1].date().toPyDate()})
                continue

            if element_type == UI_TYPE.VALUE:
                data.update({key: e[1]})
                continue

        return data

    @staticmethod
    def load_config(source_config: dict, ui_name_to_normal_name: list, combox_cfg_name_to_index: dict) -> None:
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
    def save_config(config_dict: dict, config_path: str):
        cfg_parser = configparser.ConfigParser()
        cfg_parser["SCRAPER_CONFIGURATION"] = config_dict
        with open(config_path, "w", encoding="utf-8") as file:
            cfg_parser.write(file)

    @staticmethod
    def set_combo_box_item(combo_box, original_name, readable_name_to_org_name):
        pass

    @staticmethod
    def browse_dir(change_var=None) -> str:
        dst = QtWidgets.QFileDialog.getExistingDirectory()
        if change_var:
            change_var.setText(dst)
        return dst

    @staticmethod
    def browse_file_fmt(change_var) -> str:
        dst = QtWidgets.QFileDialog.getOpenFileName()[0]
        file_string = "file<{encoding}><{separator}>: {path}"
        fs = file_string.format(encoding="utf-8", separator=",", path=dst)
        change_var.setText(fs)
        return fs

    @staticmethod
    def browse_file(change_var=None) -> str:
        dst = QtWidgets.QFileDialog.getOpenFileName()[0]
        if change_var:
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
