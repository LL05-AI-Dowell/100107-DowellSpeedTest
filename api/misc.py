
# ------------------------FORMAT OF INFO REQUEST BODY------------------------ #

INFO_REQUEST_FORMAT = {
    "name": True,
    "logos": True,
    "address": True,
    "site_socials": {
        "all": True,
        "choices": ["facebook", "twitter", "instagram", "linkedin", "youtube", "pinterest", "tumblr", "snapchat"]
    },
    "social_media_links": {
        "all": True,
        "choices": ["facebook", "twitter", "instagram", "linkedin", "youtube", "pinterest", "tumblr", "snapchat"]
    },
    "all_phone_numbers": True,
    "all_emails": True,
    "all_links": True,
    "pages_url": ["about", "contact", "careers", "services", "products"]
}

# ----------------------------------------------------------------------------- #

# -------- CORRESPONDENCE OF INFO REQUEST KEYS TO INFO SCAREPER METHODS ------------ #
# This is used in the process method of the WebsiteInfoRequest class to map the keys 
# in the info request to the methods of the WebsiteInfoScraper class

INFO_REQUEST_SCRAPER_METHOD_CORRESPONDENCE = {
    "name": "find_website_name",
    "logos": "find_website_logos",
    "address": "find_website_address",
    "website_socials": {
        "all": "find_website_social_handles",
        "choices": "find_website_social_handles"
    },
    "social_media_links": {
        "all": "find_all_social_media_links",
        "choices": "find_all_social_media_links"
    },
    "all_phone_numbers": "find_phone_numbers",
    "all_emails": "find_emails",
    "all_links":"find_links",
    "pages_url": "find_links_related_to",
}

info_request_smc = INFO_REQUEST_SCRAPER_METHOD_CORRESPONDENCE

# --------------------------------------------------------------------------------- #
