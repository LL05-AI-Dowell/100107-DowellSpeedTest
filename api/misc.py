
# ------------------------FORMAT OF INFO REQUEST BODY------------------------ #

INFO_REQUEST_FORMAT = {
    "name": True,
    "logos": True,
    "address": True,
    "website_socials": {
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
    "pages_url": "guess_pages_urls",
}

info_request_smc = INFO_REQUEST_SCRAPER_METHOD_CORRESPONDENCE

# --------------------------------------------------------------------------------- #

# ------------------------SOCIAL PLATFORMS------------------------ #

_SOCIAL_PLATFORMS = {
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
}

SOCIAL_PLATFORMS = {
    "facebook": "https://www.facebook.com/",
    "twitter": "https://twitter.com/",
    "instagram": "https://www.instagram.com/",
    "linkedin": "https://www.linkedin.com/company/",
    "youtube": "https://www.youtube.com/",
    "reddit": "https://www.reddit.com/user/",
    "snapchat": "https://www.snapchat.com/add/",
    "whatsapp": "https://wa.me/",
    "telegram": "https://t.me/",
    "wechat": "https://weixin.qq.com/",
    "tiktok": "https://www.tiktok.com/@",
    "soundcloud": "https://soundcloud.com/",
    "spotify": "https://open.spotify.com/user/",
    "medium": "https://medium.com/@",
    "quora": "https://www.quora.com/profile/",
    "twitch": "https://www.twitch.tv/",
}


# ----------------------------------------------------------------- #
