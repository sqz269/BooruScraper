from Scraper.framework._components_basic import ComponentBasic

class ComponentsDanbooru(ComponentBasic):


    def __init__(self, *args, **kwargs):
        # See _base_component->BaseComponent's constructor for argument details
        super().__init__(*args, **kwargs)


    def generate_urls(self):
        return super().generate_urls()


    def process_page(self, url):
        return super().process_page(url)


    def are_requirements_satisfied(self, data):
        return super().are_requirements_satisfied(data)


    def entry_point(scraper_framework_base):
        return super().entry_point(scraper_framework_base)
