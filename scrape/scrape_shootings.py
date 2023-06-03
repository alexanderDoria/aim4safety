from utils import WebScraper
from lxml.html import HtmlElement
import pandas as pd

scraper = WebScraper()
wiki_shootings_url = "https://en.wikipedia.org/wiki/List_of_mass_shootings_in_the_United_States"


def process_int(value: str) -> int:
    """
    Processes integer values which may contain estimation e.g. 50-100.
    Casts to an integer.
    """
    if value.endswith('+'):
        return value.replace('+', '')
    if '–' in value:
        return (int(value.split('–')[0]) + int(value.split('–')[1])) // 2
    return int(value)


def fetch_details(url: str):
    """
    Retrieves details such as lat / long, weapons, etc
    """
    details = {
        'weapons': None,
        'lat': None,
        'long': None
    }
    tree = scraper.get_tree(url)


def parse_row(row: HtmlElement) -> dict:
    """
    Parses cell information from HTML row
    """
    cells = row.xpath('.//td')

    date = cells[0].text_content().replace('\n', '')
    location = cells[1].text_content().replace('\n', '')
    dead = cells[2].text_content().split('[')[0].replace('\n', '')
    injured = cells[3].text_content().split('[')[0].replace('\n', '')
    casualty = cells[4].text_content().split('[')[0].replace('\n', '')
    description = cells[5].text_content().replace('\n', '')
    wiki_url = cells[5].xpath('.//a/@href')[0]

    return {
        'date': date,
        'location': location,
        'dead': dead,
        'injured': injured,
        'casualty': casualty,
        'description': description,
        'wiki_url': wiki_url,
    }


tree = scraper.get_tree(wiki_shootings_url)
rows = tree.xpath('//*[contains(@class, "wikitable")]//tr')

rows = [row for row in rows if ',' in row.text_content()]
data = [parse_row(row) for row in rows]

data = pd.DataFrame(data)
