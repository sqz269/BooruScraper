from Scraper.libs.logger import init_logging
from Scraper.libs.utils import Utils
from Scraper.libs.cfgBuilder import ConfigurationBuilder
from Scraper.libs.singleton import Singleton

from logging import Logger


class MatchMode:
    INCLUDE = 0  # Matches element in each list using == operator (sv == v)
    EXCLUDE = 1
    SUPER_INCLUDE = 10  # Matches element in each list using in operator (sv in v)
    SUPER_EXCLUDE = 11

    GREATER = 2
    SMALLER = 3
    EQUAL = 4

    # VARY    = 5


class BaseComponent(Utils, metaclass=Singleton):
    CONFIG_REQUIRED_FIELDS = [
        "save_path", "filename_string", "csv_entry_string", "master_directory_name_string",
        "max_concurrent_thread", "delay_start", "logger_stdout", "logger_file", "logger_name",
        "merge_file", "merge_file_keep_separate"
    ]

    def __init__(self, config_path: str, load_config_from_abs_path=False, init_verbose=False):
        """Performs Initialization for the most basic component required

        Arguments:
            config_path {str} -- the name/abs path for config file that will be loaded (depends on paramater 'load_config_from_abs_path')

        Keyword Arguments:
            load_config_from_abs_path {bool} -- true if you want to load a configuration file from a specific path not Scraper/config/* (default: {False})
            init_verbose {bool} -- print out debug infomation during the initialization process (before logger is created) (default: {False})

        Raises:
            SystemExit: Raises when the configuration failed to be read
        """
        self.init_verbose = init_verbose
        self.config: ConfigurationBuilder = None
        self.logger: Logger = None

        self.debug_print("[*] Initalizing basic components")

        self.init_config(config_path, load_config_from_abs_path)

        self.init_logger()

        self.logger.info("Basic Component Initialized")
        super().__init__(self.logger)

    def validate_basic_config_requirements(self) -> list:
        """check if required config fields exists

        Returns:
            list -- list of missing config fields, empty if no required fields are missing
        """
        required = self.CONFIG_REQUIRED_FIELDS.copy()
        for key, _ in self.config.configuration.items():
            try:
                required.remove(key)
            except ValueError:
                pass
        return required

    def init_config(self, config_path, load_config_from_abs_path):
        self.config = ConfigurationBuilder()
        self.debug_print(f"[*] Reading Configuration file at: {config_path}")

        # Load Configuration
        cfg_loader = self.config.parse_cfg_from_path if load_config_from_abs_path else self.config.parse_cfg_from_module_directory
        self.debug_print(
            f"[*] Loading configuration via: {'absolute path' if load_config_from_abs_path else 'configuration directory'}")
        if not cfg_loader(config_path):
            print(f"[!] Failed to parse config file at location: {config_path}. File does not exist or inaccessible")
            input("[-] Base Component Initialization Failed; Press Enter to Exit")
            raise SystemExit("Failed to load Config")
        self.debug_print("[+] Configuration loaded")

        self.debug_print("[*] Validating Configuration")
        missing_keys = self.validate_basic_config_requirements()  # returns empty list if nothing is missing
        if missing_keys:
            print(f"[-] Invalid Config, Required fields are missing. Missing Keys: {missing_keys}")
            input("Invalid configuration file detected. Press Enter to exit")
            raise SystemExit("Invalid Configuration")

    def init_logger(self):
        self.debug_print(
            f"[*] Preparing Loggers; Logger name: {self.config['logger_name']}; File Level: {self.config['logger_file']}; Console Level: {self.config['logger_stdout']}")
        self.logger = init_logging(
            level_stdout=self.config["logger_stdout"],
            level_IO=self.config["logger_file"],
            name=self.config["logger_name"]
        )
        self.logger.debug("Logger Initalized")

    def debug_print(self, msg: str):
        if self.init_verbose:
            print(msg)

    def exit(self, code=0):
        self.logger.warning("Function \"exit_handler(code)\" was not overridden")
        input("Press Enter to Exit")
        raise SystemExit(code)

    def automated_requirements_verification(self, data_to_config_dict: dict, data_dict: dict,
                                            short_circut=False) -> list:
        requirements_missed = []
        for k, v in data_to_config_dict.items():
            if not self._validate_requirement(self.config[k], *v, data=data_dict):
                if short_circut: return [k]
                requirements_missed.append(k)
        return requirements_missed

    def _validate_requirement(self, standard_value, value, v_type: Union[int, str, list, bool],
                              mode: MatchMode, separater=",", data=None) -> bool:
        """Validates a requirement (duh)

        Arguments:
            standard_value {<T>} -- the value being compared (left side of the comparison operand)
            value {str} -- the key to access the value of the image_data that we are going to compare.
            v_type {Union[int, str, list, bool]} -- the value's data type we are comparing
            mode {MatchMode} -- how we are comparing this value

        Keyword Arguments:
            separater {str} -- the separater we using if we are compairing list but value is a string and need split (default: {","})
            data {dict} -- Image data for accessing value (default: {None})

        Returns:
            bool -- is the value matches MatchMode requirements (comparison operand returns true, or value in/excludes the value in standard_value)
        """
        value = data[value]
        if v_type == int:
            value = int(value)
            if mode in [MatchMode.EXCLUDE, MatchMode.INCLUDE]:
                self.logger.error("Unsupported matchmode of [EXCLUDE, INCLUDE] for type int")
                return False

            if mode == MatchMode.EQUAL:
                return standard_value == value

            if mode == MatchMode.GREATER:
                return standard_value > value

            if mode == MatchMode.SMALLER:
                return standard_value < value

        if v_type == str:
            if mode in [MatchMode.GREATER, MatchMode.SMALLER]:
                self.logger.error("Unsupported matchmode of [GREATER, SMALLER] for type str")
                return False

            if mode == MatchMode.EQUAL:
                return standard_value == value

            if mode == MatchMode.INCLUDE:
                return standard_value in value  # TODO: Reverse compairson or something like that

            if mode == MatchMode.EXCLUDE:
                return standard_value not in value

        if v_type == bool:
            if mode in [MatchMode.GREATER, MatchMode.SMALLER, MatchMode.EXCLUDE, MatchMode.INCLUDE]:
                self.logger.error(
                    "Unsupported matchmode of [GREATER, SMALLER, EXCLUDE, INCLUDE, VARY] for type bool. Only mode Equal is supported")
                return False

            if (standard_value == "" or
                standard_value.lower() == "ignore" or
                standard_value.lower() == "none"):
                return True

            return standard_value == value

        if v_type == list:
            if mode in [MatchMode.GREATER, MatchMode.SMALLER, MatchMode.EQUAL]:
                self.logger.error("Unsupported matchmode of [GREATER, SMALLER, VARY, EQUAL] for type list")
                return False

            if isinstance(value, str):
                value = value.split(separater)

            if mode == MatchMode.SUPER_INCLUDE:
                for elements in standard_value:
                    for v_elements in value:
                        if elements in v_elements: break
                    else:
                        return False
                return True

            if mode == MatchMode.SUPER_EXCLUDE:
                for elements in standard_value:
                    for v_elements in value:
                        if elements in v_elements: return False
                return True

            if mode == MatchMode.INCLUDE:
                for elements in standard_value:
                    if not (elements in value): return False
                return True

            if mode == MatchMode.EXCLUDE:
                for elements in standard_value:
                    if (elements in value): return False
                return True

            # if mode == MATCH_MODE.EQUAL:

        self.logger.warning(f"No Know Operation with type: {v_type}. Match Mode: {mode}")

    @staticmethod
    def strict_type_check(var, t_type, v_name):
        assert isinstance(var, t_type), f"Variable: {v_name}. Expected: {t_type}; Actual: {type(var)}"

    @staticmethod
    def entry_point(scraper_framework_base):
        # THIS SHOULD BE OVERRIDDEN BY OTHER CLASSES
        scraper_framework_base.logger.warning("Function: \"entry_point(scraper_framework_base)\" was not overridden")
        scraper_framework_base.run([])
        return 0
