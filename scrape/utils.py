from lxml import html
from lxml.html import HtmlElement
import requests


class WebScraper():
    def get_tree(self, url: str) -> HtmlElement:
        """
        Returns HTML content from URL
        """
        page = requests.get(url)
        return html.fromstring(page.content)
