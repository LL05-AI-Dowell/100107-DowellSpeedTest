from utils.scraper import WebsiteInfoScraper

from urllib.parse import urljoin

def normalize_links(links):
    # Replace three slashes with two slashes
    normalized_links = [link.replace(':///', '://') for link in links]

    return normalized_links


def getPages():
    scraper = WebsiteInfoScraper("https://uxlivinglab.com")
    urls = normalize_links(scraper.find_links())
    return urls

v = getPages()
print(v)