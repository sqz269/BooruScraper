import configparser
import os

import parse

from Scraper.libs.singleton import Singleton


class ConfigurationBuilder(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.parser = configparser.ConfigParser()

        self.configuration = {

        }

    def get_configuration(self) -> dict:
        return self.configuration

    @staticmethod
    def boolean(value: str) -> bool:
        true_booleans = ["yes", "ok", "true", "yea", "yep", "on", "y", "1"]
        false_boolean = ["no", "naw", "false", "nope", "nah", "off", "n", "0"]

        if value.lower().strip() in true_booleans:
            return True

        if value.lower().strip() in false_boolean:
            return False

        raise ValueError("Value is not a valid boolean")

    @staticmethod
    def logger_value(value: str) -> int:
        logger_lvl = {
            "critical": 50,
            "fatal": 50,
            "error": 40,
            "warning": 30,
            "warn": 30,
            "info": 20,
            "infomation": 20,
            "debug": 10
        }

        if value.lower().strip() in logger_lvl.keys():
            return logger_lvl[value.lower().strip()]

        raise ValueError("Value is not a valid logging level")

    @staticmethod
    def file_value(value) -> list:
        base_format_string = "file<{encoding}><{separator}>: {path}"
        file_info: list = value.strip().split(":")

        if not (len(file_info) == 2 and file_info[0][:4] == "file"):
            raise AssertionError("value does not point to file")

        encoding, separator, path = parse.parse(base_format_string, value).named.values()

        print(
            f"Following configuration's file at path: {path}, with encoding: {encoding}, and splitting with separator: {separator}")

        if separator == "\\n": separator = "\n"

        with open(path, "r", encoding=encoding) as file:
            return file.read().strip() if separator.lower() == "none" else file.read().strip().split(separator)

    @staticmethod
    def get_value(value: str) -> type:
        try:
            return ConfigurationBuilder.file_value(value)
        except (AssertionError, ValueError):
            pass

        try:
            if (float(value).is_integer()): return int(value)
            return float(value)
        except ValueError:
            pass

        try:
            return ConfigurationBuilder.boolean(value)
        except ValueError:
            pass

        try:
            return ConfigurationBuilder.logger_value(value)
        except ValueError:
            pass

        return value

    def cvt_str_list(self, cvt_keys: list, separator=",") -> None:
        for keys in cvt_keys:
            if not isinstance(keys, str): continue
            try:
                self.configuration[keys] = [i for i in self.configuration[keys].replace(" ", "").split(separator) if i]
            except AttributeError as e:
                print("[!] Error, Failed to convert key: {} to list. Error Details: {}".format(keys, e))

    def parse_cfg_from_path(self, cfg_path: str) -> bool:
        # configParser.read returns paths of the config file if it was was valid, else it will return empty list
        if not self.parser.read(cfg_path, encoding="utf-8"): return False
        for sections in self.parser.sections():
            for keys in self.parser[sections]:
                self.configuration.update({keys: ConfigurationBuilder.get_value(self.parser[sections][keys])})
        return True

    def parse_cfg_from_module_directory(self, config_name: str) -> bool:
        for root, _, files in os.walk("."):
            for item in files:
                if item == ".config_directory":
                    file_path = str(os.path.abspath(os.path.join(root, config_name)))
                    return self.parse_cfg_from_path(file_path)

        print(
            "[-] Unable to parse config. No configuration directory found. please create a file with name \".config_directory\" in your configuration folder. At or below level of main.py")
        return False

    def validate_cfg(self):
        for key, values in self.configuration.items():
            if not values:
                return (False, key, values)
        return (True, None, None)

    def get_config_dict(self):
        return self.configuration

    def __getitem__(self, x):
        return self.configuration[x]


if __name__ == "__main__":
    cfg = ConfigurationBuilder()
    cfg.prase_cfg_complete(input("Enter config Path: "))
    print(cfg.configuration)
    input("Press Enter to Exit")
