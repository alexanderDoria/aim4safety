from utils import WebScraper
from lxml.html import HtmlElement
import pandas as pd

scraper = WebScraper()
wiki_domain = "https://en.wikipedia.org"
wiki_shootings_url = f"{wiki_domain}/wiki/List_of_mass_shootings_in_the_United_States"


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

    tree = scraper.get_tree(url)
    rows = tree.xpath('//*[contains(@class, "infobox")]//tr')
    # filter for rows that have both th and td cells
    rows = [row for row in rows if row.xpath('.//td') and row.xpath('.//th')]

    return parse_infobox_rows(rows)


def parse_infobox_rows(rows: HtmlElement) -> dict:
    """
    Parses cell information from HTML infobox row in shooting-specifc URL
    """
    details = {}

    for row in rows:
        key = row.xpath('.//th')[0].text_content().lower()
        if key == 'date':
            details['datetime'] = row.xpath(
                './/td')[0].text_content().replace('\xa0', ' ')
        elif key == 'coordinates':
            lat, long = row.xpath('.//td//*//span')[0].text_content().split()
            details['latitude'] = lat
            details['longitude'] = long
        elif key == 'weapons':
            weapons = row.xpath('.//td')[0].text_content().split('\n')
            weapons = [weapon for weapon in weapons if weapon]
            weapons = ','.join(weapons)
            details['weapons'] = weapons
        elif key == 'deaths' or key == 'injured':
            details[f"{key}_details"] = row.xpath('.//td')[0].text_content()
        else:
            details[key] = row.xpath('.//td')[0].text_content()
    return details


def parse_wikitable_row(row: HtmlElement) -> dict:
    """
    Parses cell information from HTML wikitable row in wiki_shootings_url
    """
    cells = row.xpath('.//td')

    date = cells[0].text_content().replace('\n', '')
    location = cells[1].text_content().replace('\n', '')
    dead = cells[2].text_content().split('[')[0].replace('\n', '')
    injured = cells[3].text_content().split('[')[0].replace('\n', '')
    casualty = cells[4].text_content().split('[')[0].replace('\n', '')
    description = cells[5].text_content().replace('\n', '')
    wiki_url = f"{wiki_domain}{cells[5].xpath('.//a/@href')[0]}"
    print('scraping: ', wiki_url)
    details = fetch_details(wiki_url)
    time.sleep(1.5)

    main_info = {
        'day': date,
        'location': location,
        'dead': dead,
        'injured': injured,
        'casualty': casualty,
        'description': description,
        'wiki_url': wiki_url,
    }

    main_info.update(details)

    return main_info


def fetch_data() -> pd.DataFrame:
    """
    Returns complete data source for shooting information
    """
    tree = scraper.get_tree(wiki_shootings_url)
    rows = tree.xpath('//*[contains(@class, "wikitable")]//tr')

    # filter for rows that have a comma i.e. text content
    rows = [row for row in rows if ',' in row.text_content()]
    data = [parse_wikitable_row(row) for row in rows]
    return pd.DataFrame(data)


data = fetch_data()
