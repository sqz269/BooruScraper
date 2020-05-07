from Scraper.framework._framework import init_scraper_base

from Scraper import AVAILABLE_MODULES

def module_selection():
    module_names = AVAILABLE_MODULES.keys()

    is_input_valid = False
    while not is_input_valid:
        for index, name in enumerate(module_names):
            print(f"{index}: {name}")
        module_index = int(input(f"Select Module (0 - {len(module_names) - 1}): "))

        if (module_index >= 0 and module_index <= len(module_names) -1):
            is_input_valid = True

        print()

    print(f"Using Module: {list(module_names)[module_index]}")
    return AVAILABLE_MODULES[(list(module_names)[module_index])]


if __name__ == "__main__":
    base_module = module_selection()
    scraper_base = init_scraper_base(base_module)
    scraper_base.entry_point(scraper_base)
