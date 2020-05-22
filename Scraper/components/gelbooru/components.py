from Scraper.framework.components_basic import ComponentBasic

from bs4 import BeautifulSoup
import requests

class ComponentGelbooru(ComponentBasic):

    def __init__(self):
        super().__init__("gelbooru.ini")

    def generate_urls(self):
        return super().generate_urls()

    def process_page(self, url):
        return super().process_page(url)

    def are_requirements_satisfied(self, data):
        return super().are_requirements_satisfied(data)
