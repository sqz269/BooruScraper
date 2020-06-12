from typing import List, Tuple


class IComponents:
    """All methods in this class should be overridden by it's child
    """
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
