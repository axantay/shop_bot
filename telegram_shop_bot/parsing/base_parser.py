from bs4 import BeautifulSoup
import requests
import json


class BaseParser:
    def __init__(self, category):
        self.URL = "https://asaxiy.uz/product/"
        self.category = category

    def get_html(self):
        html = requests.get(self.URL + self.category)
        if html.status_code == 200:
            html = html.text
            return html
        else:
            return 'Qatelik'

    def get_soup(self):
        html = self.get_html()
        if html == 'Qatelik':
            pass
        else:
            soup = BeautifulSoup(html, 'html.parser')
            return soup
