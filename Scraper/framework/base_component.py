from Scraper.libs.logger import init_logging
from Scraper.libs.utils import Utils
from Scraper.libs.cfgBuilder import ConfigurationBuilder
from Scraper.libs.singleton import Singleton

from logging import Logger


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
        for key, value in self.config.configuration.items():
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
        self.debug_print(f"[+] Configuration loaded")

        self.debug_print(f"[*] Validating Configuration")
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

    @staticmethod
    def strict_type_check(var, t_type, v_name):
        assert isinstance(var, t_type), f"Variable: {v_name}. Expected: {t_type}; Actual: {type(var)}"

    @staticmethod
    def entry_point(scraper_framework_base):
        # THIS SHOULD BE OVERRIDDEN BY OTHER CLASSES
        scraper_framework_base.logger.warning("Function: \"entry_point(scraper_framework_base)\" was not overridden")
        scraper_framework_base.run([])
        return 0
