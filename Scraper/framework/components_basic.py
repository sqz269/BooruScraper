from Scraper.libs.cfgBuilder import ConfigurationBuilder
from Scraper.framework.base_component import BaseComponent

from typing import List, Tuple


class ComponentBasic(BaseComponent):
    """All methods in this class should be overridden by it's child
    """

    def __init__(self, *args, **kwargs):
        self.url_as_referer: bool = None
        self.request_header: dict = {}
        self.request_cookie: dict = {}

        # Arguments: config_path: str, load_config_from_abs_path=False, init_verbose=False
        super().__init__(*args, **kwargs)  # Load the configuration file from this path

        self.logger.debug(f"Using User-Agent for header: {self.config['user_agent']}")
        self.request_header.update({"User-Agent": self.config["user_agent"]})

    def generate_urls(self) -> List[Tuple[str, str]]:
        self.logger.fatal("Function: \"generate_urls(self)\" was not overridden")
        raise NotImplementedError("Function \"generate_urls()\" was not overridden")

    def process_page(self, url: str) -> dict:
        self.logger.fatal("Function: \"process_page(self, url: str)\" was not overridden")
        raise NotImplementedError("Function \"process_page()\" was not overridden")

    def are_requirements_satisfied(self, data: dict) -> bool:
        self.logger.fatal("Function: \"are_requirements_satisfied(self, data: dict)\" was not overridden")
        raise NotImplementedError("Function \"are_requirements_satisfied()\" was not overridden")


if __name__ == "__main__":
    print("Run main.py to execute the script")
