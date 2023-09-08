from bs4_web_scraper.scraper import BS4WebScraper
from urllib3.util import parse_url
from urllib.parse import unquote_plus
from difflib import get_close_matches
from concurrent.futures import ThreadPoolExecutor

# ------------------------SOCIAL PLATFORMS------------------------ #

SOCIAL_PLATFORMS = {
    "facebook": "https://www.facebook.com/",
    "twitter": "https://twitter.com/",
    "instagram": "https://www.instagram.com/",
    "linkedin": "https://www.linkedin.com/company/",
    "youtube": "https://www.youtube.com/",
    "pinterest": "https://www.pinterest.com/",
    "tumblr": "https://www.tumblr.com/",
    "reddit": "https://www.reddit.com/user/",
    "flickr": "https://www.flickr.com/people/",
    "snapchat": "https://www.snapchat.com/add/",
    "whatsapp": "https://wa.me/",
    "telegram": "https://t.me/",
    "wechat": "https://weixin.qq.com/",
    "line": "https://line.me/R/ti/p/",
    "viber": "https://chats.viber.com/",
    "vk": "https://vk.com/",
    "tiktok": "https://www.tiktok.com/@",
    "soundcloud": "https://soundcloud.com/",
    "spotify": "https://open.spotify.com/user/",
    "medium": "https://medium.com/@",
    "quora": "https://www.quora.com/profile/",
    "twitch": "https://www.twitch.tv/",
    "behance": "https://www.behance.net/",
    "dribbble": "https://dribbble.com/",
    "deviantart": "https://www.deviantart.com/",
    "foursquare": "https://foursquare.com/",
    "goodreads": "https://www.goodreads.com/",
    "hackernews": "https://news.ycombinator.com/user?id=",
    "producthunt": "https://www.producthunt.com/@",
    "tripadvisor": "https://www.tripadvisor.com/members/",
    "yelp": "https://www.yelp.com/user_details?userid=",
    "wordpress": "https://profiles.wordpress.org/",
    "blogger": "https://www.blogger.com/profile/",
    "wix": "https://www.wix.com/dashboard/",
    "weebly": "https://www.weebly.com/editor/main.php#/site/",
    "jimdo": "https://www.jimdo.com/app/profile/",
    "squarespace": "https://www.squarespace.com/preview/",
}

# ----------------------------------------------------------------- #



class WebsiteInfoScraper:
    """
    Fetches information about a website or webpage.
    """

    engine = BS4WebScraper()

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
            raise TypeError(f"Expected scraper to be of type {BS4WebScraper.__name__}, got {type(engine)} instead.")
        self.target = web_url
        self.engine = engine if engine else self.engine
        self.maximum_search_depth = max_search_depth


    def find_website_name(self):
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
            content = tag.get("content", None) or tag.text
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
        return list(filter(lambda x : bool(x), logos))
    

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
        matches = get_close_matches(page_name, urls.keys(), n=len(urls)//2 or 1, cutoff=0.3)
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
    

    def find_website_social_handle_for(self, platform_name: str):
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
                new_finder = self.__class__(page_url, self.engine, self.maximum_search_depth)
                related_links = new_finder.find_links_related_to(platform_name)
                if related_links:
                    website_name = self.find_website_name()
                    social_handle_matches = get_close_matches(website_name, related_links, n=len(related_links)//2 or 1, cutoff=0.3)
                    if social_handle_matches:
                        return social_handle_matches[0]
            continue
        
        # If url cannot be found in those pages, resort to checking the base url for social handle.
        # This is less likely to be the correct one, but it's better than nothing.
        social_url = self.guess_page_url(platform_name)
        return social_url
    

    def find_website_social_handles(self, platform_names: list[str] = None):
        """
        Finds social media handles for the website on a list of social media platforms.

        :param platform_names: A list of social media platforms to find the social handles for. If None,\
              all the supported social media platforms are searched for.
        :return: A dictionary of the social media handles found.
        """
        platform_names = list(SOCIAL_PLATFORMS.keys()) if not platform_names else platform_names
        result = {}
        def add_result(platform_name):
            result[platform_name] = self.find_website_social_handle_for(platform_name)
        
        with ThreadPoolExecutor() as executor:
            executor.map(add_result, platform_names)

        result_items = list(result.items())
        for key, value in result_items:
            if not value:
                result.pop(key)
        return result   
    

    def find_links_related_to(self, _s: str | list[str], links: list[str] = None):
        """
        Similar to find_links, but only returns links that contain the string _s or the strings
        in list _s

        :param _s: The string or list of strings to search for in the links.
        :param links: A list of links to search in. If None, the links on the website are searched.
        :return: A list of urls of the links found.
        """
        links = self.find_links() if not links else links

        def get_matches(string: str):
            return [ link for link in links if string.lower() in link.lower() ]
        
        if isinstance(_s, str):
            return get_matches(_s)
        return list(set([ link for _s_ in _s for link in get_matches(_s_) ]))


    def find_all_social_media_links(self, platform_names: list[str] = None):
        """
        Finds all the social media links on the website.

        :param platform_names: A list of social media platforms to find the social media links for. If None,\
              all the supported social media platforms are searched for.
        :return: A dictionary of the social media links found.
        """
        website_base_url = self.engine.get_base_url(self.target)
        platform_names = list(SOCIAL_PLATFORMS.keys()) if not platform_names else platform_names
        if not platform_names:
            # Remove the website from the list of social platform url to search for. 
            # If the website its self is a social platform,
            for index, (_, value) in enumerate(SOCIAL_PLATFORMS.items()):
                if website_base_url in value:
                    platform_names.pop(index)
                    break
        result = {}
        links = self.find_links()
        def add_result(platform_name):
            result[platform_name] = self.find_links_related_to(platform_name, links)

        with ThreadPoolExecutor() as executor:
            executor.map(add_result, platform_names)

        result_items = list(result.items())
        for key, value in result_items:
            if not value:
                result.pop(key)
        return result
    
    
    def find_website_address(self):
        # Implementation not yet decided
        pass
