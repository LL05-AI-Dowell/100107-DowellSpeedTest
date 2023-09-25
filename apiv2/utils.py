import json
import re
from bs4_web_scraper.scraper import BS4WebScraper
from urllib3.util import parse_url
from urllib.parse import unquote_plus
from difflib import get_close_matches
from concurrent.futures import ThreadPoolExecutor
import requests
from typing import Iterable, List, Dict

from .misc import SOCIAL_PLATFORMS, common_address_components


class WebsiteInfoScraper:
    """
    Fetches information about a website or webpage.
    """

    engine = BS4WebScraper(log_to_console=False)

    def __init__(self, web_url: str, max_search_depth: int = 0, engine: BS4WebScraper = None):
        """
        Initializes a WebsiteInfoScraper object.

        :param web_url: The url of the website or webpage to find information about.
        :param engine: The web scraper to use to find information about the website. \
        Should be of type BS4WebScraper.
        :param max_search_depth: The maximum depth to search for information on the website. \
        The higher the depth, the longer it takes to find information. \
        Defaults to 0, which means only the base url is searched.\
        If set to 1, the base url and all the links on the base url are searched. \
        If set to 2, the base url, all the links on the base url and all the links on the links on the base url are searched and so on
        """
        if engine and not isinstance(engine, BS4WebScraper):
            raise TypeError(f"Expected engine to be of type {BS4WebScraper.__name__}, got {type(engine)} instead.")
        self.target = web_url
        self.engine = engine if engine else self.engine
        self.maximum_search_depth = max_search_depth


    def find_website_name(self) -> str | None:
        """
        Find website name.

        :return: Website name if found else None
        """
        base_url = self.engine.get_base_url(self.target)
        set_1 = self.engine.find_all_tags(
            url=base_url,
            target="meta",
            attrs={
                "name": ["application-name", "apple-mobile-web-app-title"],
            },
            depth=self.maximum_search_depth
        )
        set_2 = self.engine.find_all_tags(
            url=base_url,
            target="meta",
            attrs={
                "property": ["og:site_name", "og:title"],
            },
            depth=self.maximum_search_depth
        )
        set_3 = self.engine.find_all_tags(
            url=base_url,
            target="meta",
            attrs={
                "itemprop": ["name"],
            },
            depth=self.maximum_search_depth
        )
        set_4 = self.engine.find_all_tags(
            url=base_url,
            target="title",
            depth=self.maximum_search_depth
        )
        tags = set_1 + set_2 + set_3 + set_4
        results = []
        for tag in tags:
            content = tag.get("content", None) or tag.text.split()[0]
            if content:
                results.append(content)
        names = set(results)
        host = parse_url(base_url).host
        matches = get_close_matches(host, names, n=len(names)//2 or 1, cutoff=0.3)
        return matches[0] if matches else None
    

    def find_emails(self):
        """
        Finds all the emails on the website.

        :return: A list of emails found.
        """
        result = self.engine.find_emails(url=self.target, depth=self.maximum_search_depth)
        return list(set(result))
    

    def find_phone_numbers(self):
        """
        Finds all the phone numbers on the website.

        :return: A list of phone numbers found.
        """
        result = self.engine.find_phone_numbers(url=self.target, depth=self.maximum_search_depth)
        return list(set(result))
        

    def find_links(self):
        """
        Finds all the links on the website.

        :return: A list of urls of the links found.
        """
        return self.engine.find_links(url=self.target, depth=self.maximum_search_depth)


    def find_website_logos(self):
        """
        Finds the logos of the website. 
        
        Checks the Favicons, Apple Touch Icons because they are more likely to be the correct ones.
        :return: A list of urls of the logos found.
        """
        logo_tags = self.engine.find_all_tags(
            url=self.target, 
            target="link",
            attrs={
                "rel": ["icon", "shortcut icon", "apple-touch-icon", "apple-touch-icon-precomposed"]
            },
            depth=self.maximum_search_depth
        )
        # Get image urls from meta tags on the websites home page
        image_meta_tags = self.engine.find_all_tags(
            url=self.engine.get_base_url(self.target), 
            target="meta",
            attrs={
                "property": ["og:image", "twitter:image", "twitter:image:src"]
            },
            depth=self.maximum_search_depth
        )
        logo_tags.extend(image_meta_tags)
        logos = [ self.engine.get_tag_rra(tag, download=False) for tag in logo_tags ]
        return list(set(filter(lambda x : bool(x), logos)))
    

    def guess_page_url(self, page_name: str):
        """
        Tries to guess the correct url of a page on the website based on the page name.

        :param page_name: The name of the page to guess the url of. \
            Can be the name of an external page or a page on the website\
                  as long as it can related to a url on the website.
        :return: url of the page if found, None otherwise.
        """
        base_url = self.engine.get_base_url(self.target)
        links = self.engine.find_links(
            url=base_url,
            depth=self.maximum_search_depth
        )
        # Try and find a close match
        urls = {unquote_plus(link) : link for link in links}
        matches = get_close_matches(page_name.lower(), urls.keys(), n=len(urls)//2 or 1, cutoff=0.5)
        match = urls.get(matches[0]) if matches else None
        if match:
            return match
        # If no close match, try and find a link with the page name in it
        for link in links:
            if page_name.lower() in link.lower() or page_name.strip().lower() in link.lower():
                return link
        # If still no match, try and find a link with the page name in its text
        link_tags = self.engine.find_all_tags(
            url=base_url,
            target='a',
            depth=self.maximum_search_depth
        )
        for tag in link_tags:
            if page_name.lower() in tag.text.lower():
                return tag.get("href", None)
        return None
    

    def guess_pages_urls(self, page_names: list[str]):
        """
        Tries to guess the correct urls of a list of pages on the website based on the page names.

        :param page_names: A list of page names to guess the urls of. \
            Can be the names of external pages or pages on the website\
                  as long as they can related to a url on the website.
        :return: A dictionary of the urls of the pages found.
        """
        r = {}
        def add_result(page_name):
            r[page_name] = self.guess_page_url(page_name)

        with ThreadPoolExecutor() as executor:
            executor.map(add_result, page_names)
        return r
    

    def find_website_social_handle(self, platform_name: str) -> str:
        """
        Finds social media handle for the website on a social media platform.

        This checks the contact and about pages first for social handle,
        because the one on the website details page is more likely to be the correct one.
        If the social handle is not found on those pages, it checks the base url for any link related to the social media platform.

        :param platform_name: The name of the social media platform to find the social handle for.
        :return: The social handle if found, None otherwise.
        """
        # Check contact and about pages first for social handle, 
        # because the one on the website details page is more likely to be the correct one.
        for page_name in ("contact", "about"):
            page_url = self.guess_page_url(page_name)
            if page_url and parse_url(page_url).scheme in ["http", "https"]:
                new_finder = self.__class__(
                    web_url=page_url, 
                    max_search_depth=self.maximum_search_depth,
                    engine = self.engine
                )
                social_url = new_finder.guess_page_url(platform_name)
                if social_url:
                    return social_url
                else:
                    related_links = new_finder.find_links_related_to(platform_name)
                    if related_links:
                        return related_links[0]
            continue
        
        # If url cannot be found in those pages, resort to checking the base url for social handle that matches the website's name
        # This is less likely to be the correct one, but it's better than nothing.
        website_name = self.find_website_name()
        related_links = self.find_links_related_to(platform_name)
        if related_links and website_name:
            matches = get_close_matches(website_name.lower(), related_links, n=len(related_links)//2 or 1, cutoff=0.3)
            if matches:
                return matches[0]
        if related_links:
            return related_links[0]
        return None
    

    def find_website_social_handles(self, platform_names: list[str] = None):
        """
        Finds social media handles for the website on a list of social media platforms.

        :param platform_names: A list of social media platforms to find the social handles for. If None,\
              all the supported social media platforms are searched for.
        :return: A dictionary of the social media handles found.
        """
        website_base_url = self.engine.get_base_url(self.target)
        platform_names = list(SOCIAL_PLATFORMS.keys()) if not platform_names else [ name.lower() for name in platform_names ]
        if not platform_names:
            # Remove the website from the list of social platform url to search for. 
            # If the website its self is a social platform,
            for index, (_, value) in enumerate(SOCIAL_PLATFORMS.items()):
                if website_base_url in value:
                    platform_names.pop(index)
                    break
        r = {}
        def add_result(platform_name):
            r[platform_name] = self.find_website_social_handle(platform_name)

        with ThreadPoolExecutor() as executor:
            executor.map(add_result, platform_names)
        return r or None
    

    def find_links_related_to(self, _s: str | list[str], links: list[str] = None):
        """
        Similar to `guess_pages_urls` method, but is more general and can return single or multiple results.
        For more accurate multiple results, use `guess_pages_urls` method instead.
        For more accurate single results, use `guess_page_url` method instead.
        For better performance, use this method.

        :param _s: The string or list of strings to search for in the links.
        :param links: A list of links to search in. If None, the links on the website are searched.
        :return: A list of urls of the links found or a dictionary of each result if `_s` is a list.
        """
        links = self.find_links() if not links else links

        def get_matches(string: str):
            return [ link for link in links if string.lower() in link.lower() ] or None
        
        if isinstance(_s, str):
            return get_matches(_s)
        return { _s_ : get_matches(_s_) for _s_ in _s }


    def find_all_social_media_links(self, platform_names: list[str] = None):
        """
        Finds all the social media links on the website.

        :param platform_names: A list of social media platforms to find the social media links for. If None,\
              all the supported social media platforms are searched for.
        :return: A dictionary of the social media links found.
        """
        website_base_url = self.engine.get_base_url(self.target)
        platform_names = list(SOCIAL_PLATFORMS.keys()) if not platform_names else [ name.lower() for name in platform_names ]
        if not platform_names:
            # Remove the website from the list of social platform url to search for. 
            # If the website its self is a social platform,
            for index, (_, value) in enumerate(SOCIAL_PLATFORMS.items()):
                if website_base_url in value:
                    platform_names.pop(index)
                    break
        return self.find_links_related_to(platform_names)
    
    
    def find_addresses(self):
        """Finds all addresses on website. Results are not guaranteed to be accurate."""
        address_regex = r"(\d{2,5}[-;\.\|:]*)+(\s*[\w\.\s,]+){1,3}[\.|\s]*(\w{2,3})?[\.|\s]*(\d{5}|\w{2,3})?"
        results = self.engine.find_pattern(
            url=self.target,
            regex=address_regex,
        )
        addresses = []
        for result in results:
            for c in common_address_components:
                if c in result:
                    result = re.sub(r"\n+", " ", result).strip()
                    addresses.append(result)
                    break
        return addresses or None



def is_email(address: str):
    """
    Checks if the address provided is a valid email address

    :param address: email address to be checked
    :return: True if address is an email address else false
    """
    match = re.match(r'[-|\w\.]+@\w+.\w{2,}', address)
    return match != None


email_api_url = lambda api_key: f"https://100085.pythonanywhere.com/api/v1/mail/{api_key}/"


def validate_email(email_address: str, dowell_api_key: str) -> bool:
    """
    Check is the email address provided is a valid and active email address using Dowell Email API.

    :param email_address: email address to validate
    :param dowell_api_key: user's dowell client admin api key.
    :return: True if valid else False
    """
    if not is_email(email_address):
        raise ValueError("email_address value is not valid")
    response = requests.post(
        url=email_api_url(dowell_api_key),
        data={"email": email_address}, 
        params={"type": "validate"}
    )
    if response.status_code != 200:
        response.raise_for_status()
    return response.json()["success"]


def sort_emails_by_validity(self, emails: Iterable[str], dowell_api_key: str) -> tuple[List[str], List[str]]:
    """
    Sorts a list of emails into valid and invalid emails.
    Uses Dowell Email API to determine email validity.

    NOTE: Make sure Dowell Email service is activated for API key else all emails will be classified as invalid

    :param emails: A list of emails to sort.
    :param dowell_api_key: user's dowell client admin api key.
    :return: A tuple of two lists. The first list contains valid emails and the second list contains invalid emails.
    """
    valid = []
    invalid = []
    if not isinstance(emails, Iterable):
        raise TypeError("Expected emails to be an iterable of strings")
    for email in emails:
        try:
            if validate_email(email, dowell_api_key):
                valid.append(email)
            else:
                invalid.append(email)
        except Exception:
            invalid.append(email)
    return valid, invalid


def processApikey(api_key):
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    payload = {
        "service_id": "DOWELL10007"
    }
    response = requests.post(url, json=payload)
    response_text = json.loads(response.text)
    return response_text