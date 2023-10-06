
# ------------------------FORMAT OF INFO REQUEST BODY------------------------ #

INFO_REQUEST_FORMAT = {
    "name": True,
    "logos": True,
    "addresses": True,
    "website_socials": {
        "all": True,
        "choices": ["facebook", "twitter", "instagram", "linkedin", "youtube", "pinterest", "tumblr", "snapchat"]
    },
    "social_media_links": {
        "all": True,
        "choices": ["facebook", "twitter", "instagram", "linkedin", "youtube", "pinterest", "tumblr", "snapchat"]
    },
    "phone_numbers": True,
    "emails": True,
    "links": True,
    "pages_url": ["about", "contact", "careers", "services", "products"]
}

# ----------------------------------------------------------------------------- #

# -------- CORRESPONDENCE OF INFO REQUEST KEYS TO INFO SCAREPER METHODS ------------ #
# This is used in the process method of the WebsiteInfoRequest class to map the keys 
# in the info request to the methods of the WebsiteInfoScraper class

INFO_REQUEST_SCRAPER_METHOD_CORRESPONDENCE = {
    "name": "find_website_name",
    "logos": "find_website_logos",
    "addresses": "find_addresses",
    "website_socials": {
        "all": "find_website_social_handles",
        "choices": "find_website_social_handles"
    },
    "social_media_links": {
        "all": "find_all_social_media_links",
        "choices": "find_all_social_media_links"
    },
    "phone_numbers": "find_phone_numbers",
    "emails": "find_emails",
    "links":"find_links",
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

# --------------- SOME COMMON TEXT THAT CAN BE FOUND IN ADDRESSES ------------- #

common_address_components = [
    'Street', 'St.',
    'Avenue', 'Ave.',
    'Road', 'Rd.',
    'Lane', 'Ln.',
    'Boulevard', 'Blvd.',
    'Way', 'Driveway', 'Dr.',
    'Court', 'Ct.',
    'Place', 'Pl.',
    'Square', 'Sq.',
    'Terrace', 'Ter.',
    'Circle', 'Cir.',
    'Plaza', 'Plz.',
    'Highway', 'Hwy.',
    'Expressway', 'Expwy.',
    'Route', 'Rte.',
    'Trail', 'Trl.',
    'Path', 'Pth.',
    'Manor', 'Mnr.',
    'Row', 'Rw.',
    'Crescent', 'Cres.',
    'Park', 'Pk.',
    'Gardens', 'Gdns.',
    'Mews', 'Commons',
    'Close', 'Crossing',
    'Parkway', 'Pkwy.',
    'Alley', 'Aly.',
    'Gate', 'Gt.',
    'Ridge', 'Rdg.',
    'Hill', 'Hl.',
    'Valley', 'Vly.',
    'Cove', 'Cv.',
    'Cul-de-Sac', 'CdS.', 'Court', 'Ct.',
    'Station', 'Stn.',
    'Building', 'Bldg.',
    'Apartment', 'Apt.',
    'Suite', 'Unit',
    'Room', 'Rm.',
    'Floor', 'Fl.',
    'Office', 'Ofc.',
    'Department', 'Dept.',
    'Block', 'Blk.',
    'Lot',
    'Condo', 'Cndo.', 'Cd.',
    'Tower', 'Twr.',
    'School', 'Sch.',
    'University', 'Univ.',
    'Library', 'Lib.',
    'Church', 'Ch.',
    'Temple', 'Tmp.',
    'Mosque', 'Mq.', 'Synagogue', 'Syn.', 'Post Office', 'PO', 'City', 'Town', 'Village', 'District', 'County', 'Co.', 'State', 'Province', 'Country', 'Nation', 'Region', 'Territory', 'Postal Code', 'ZIP Code', 'Postcode', 'PO Box',
]

# --------------------------------------------------------------------------------- #
