# 100107-DowellEmailExtractor

## Summary
This project involves the Scrapping web_urls through an API using 
a scrapper library to extact infomation within the different website

To use this API, clients can send HTTP requests to create, retrieve, 
update, or delete QR codes. The API supports the Extaction data
with various options such as getting the meta_data which includes 
the page_urls,phone_numbers,socil_media_links, name , logos, 
company_name,emails found and the website_url

Clients can Extract data by providing a weburl, 
 The API will return an extracted data with all metadata 
image of the QR code that can be used in various contexts such as 
websites, printed materials, or mobile apps.

The API also supports getting verified or unverified emails by passing
the apikey alongside getting all metadata of the site

Overall, this API provides a convenient way for clients to get data 
of any site regardless of the web_url



## Prerequisites

Before you begin, make sure you have the following software installed on your computer:
    .Python 3.7+

## Step 1: Setting up the Django project in your local machine.
    
Clone project by running the following command in your terminal:
git clone `https://github.com/LL05-AI-Dowell/100107-DowellEmailExtractor.git`

## Step 2: Run the Project in your local environment.

- Get into the projects directory by running:
cd /100107-DowellEmailExtractor

- Create a virtual enviroment and activate it in the terminal using

- python3 -m venv venve
source venve/bin/activate - linux


- Install the requirements
pip install -r requirements.txt

- Run the project:
python3 manage.py runserver

## API Documentation 



| HTTP Verbs | Endpoints                      | Action                                               |
|------------|--------------------------------|------------------------------------------------------|
| POST       | api/website-info-extractor/   | To get meta_data by passing the web url          |
| POST       | api/website-info-extractor/   | To Get verified and unverifed emails Generated.                     |
| POST       | api/contact-us-extractor/     | To retrieve the conctact-us-page
 Created     |
| POST       | api/v1/submit-contact-form/   | To Send data to contact-us-page 
 |


##  Endpoints Definition(Request - Response)

## Extract metadata by scrapping

POST: `/api/website-info-extractor/`

Request Body

```json
{
    "web_url": "https://www.sstream.co.ke/",
    "info_request": {
        "addresses": true,
        "emails": true,
        "links": true,
        "logos": true,
        "name": true,
        "pages_url": [
            "about",
            "contact",
            "careers",
            "services",
            "products"
        ],
        "phone_numbers": true,
        "social_media_links": {
            "all": true,
            "choices": [
                "facebook",
                "twitter",
                "instagram",
                "linkedin",
                "youtube",
                "pinterest",
                "tumblr",
                "snapchat"
            ]
        },
        "website_socials": {
            "all": true,
            "choices": [
                "facebook",
                "twitter",
                "instagram",
                "linkedin",
                "youtube",
                "pinterest",
                "tumblr",
                "snapchat"
            ]
        }
    }
}
```
Note:

This endpoint is used to extract infomation of the given url and return a response
if the response is 200 .This does not mandate implementation of api-key

Response - 200 

```json
    {
    "meta_data": {
        "addresses": null,
        "emails": [
            "hello@sstream.co",
            "On@sstream.ke"
        ],
        "links": [
            "https:///www.sstream.co.ke/contact",
            "https:///www.sstream.co.ke/events-1",
            "mailto:///hello@sstream.co.ke",
            "https:///www.sstream.co.ke/about-1",
            "http:///www.facebook.com/sstreamke",
            "https:///www.linkedin.com/in/sstreamkenya",
            "https:///www.sstream.co.ke",
            "http:///instagram.com/sstream.ke",
            "https:///www.tiktok.com/@sstreamke",
            "https:///www.sstream.co.ke/blog",
            "https:///twitter.com/SstreamK",
            "https:///www.sstream.co.ke/shop",
            "https:///www.sstream.co.ke/privacy"
        ],
        "logos": [
            "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_192%2Ch_192%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png",
            "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png",
            "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_180%2Ch_180%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png"
        ],
        "name": "Sstream",
        "pages_url": {
            "about": "https:///www.sstream.co.ke/about-1",
            "contact": "https:///www.sstream.co.ke/contact",
            "products": null,
            "services": "https://www.sstream.co.ke/events-1",
            "careers": null
        },
        "phone_numbers": [],
        "social_media_links": {
            "facebook": [
                "http:///www.facebook.com/sstreamke"
            ],
            "twitter": [
                "https:///twitter.com/SstreamK"
            ],
            "instagram": [
                "http:///instagram.com/sstream.ke"
            ],
            "linkedin": [
                "https:///www.linkedin.com/in/sstreamkenya"
            ],
            "youtube": null,
            "reddit": null,
            "snapchat": null,
            "whatsapp": null,
            "telegram": null,
            "wechat": null,
            "tiktok": [
                "https:///www.tiktok.com/@sstreamke"
            ],
            "soundcloud": null,
            "spotify": null,
            "medium": null,
            "quora": null,
            "twitch": null
        },
        "website_socials": null
    },
    "company_name": "Sstream",
    "phone_numbers": [],
    "addresses": null,
    "emails_found": [
        "hello@sstream.co",
        "On@sstream.ke"
    ],
    "logos": [
        "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_192%2Ch_192%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png",
        "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png",
        "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_180%2Ch_180%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png"
    ],
    "website_social_handles": null,
    "website_url": "https://www.sstream.co.ke"
    }
```

POST: `/api/v1/website-info-extractor/`

Request Body

```json
{
    "web_url": "https://www.sstream.co.ke/",
    "api_key": "2455e5e-9utewwq5r776-yree",
    "info_request": {
        "addresses": true,
        "emails": true,
        "links": true,
        "logos": true,
        "name": true,
        "pages_url": [
            "about",
            "contact",
            "careers",
            "services",
            "products"
        ],
        "phone_numbers": true,
        "social_media_links": {
            "all": true,
            "choices": [
                "facebook",
                "twitter",
                "instagram",
                "linkedin",
                "youtube",
                "pinterest",
                "tumblr",
                "snapchat"
            ]
        },
        "website_socials": {
            "all": true,
            "choices": [
                "facebook",
                "twitter",
                "instagram",
                "linkedin",
                "youtube",
                "pinterest",
                "tumblr",
                "snapchat"
            ]
        }
    }
}
```
Note:

This endpoint is used to extract infomation of the given url and api-key and return a response
if the response is 200 .This does prompt mandate implementation of api-key

Response - 200 

```json
    {
    "success": true,
    "message": "The information was successfully extracted",
    "data": {
        "meta_data": {
            "addresses": null,
            "emails": [
                "hello@sstream.co"
            ],
            "links": [
                "https:///twitter.com/SstreamK",
                "https:///www.sstream.co.ke/blog",
                "https:///www.sstream.co.ke/contact",
                "https:///www.sstream.co.ke/shop",
                "https:///www.sstream.co.ke/about-1",
                "http:///www.facebook.com/sstreamke",
                "https:///www.linkedin.com/in/sstreamkenya",
                "https:///www.sstream.co.ke/events-1",
                "https:///www.sstream.co.ke/privacy",
                "https:///www.sstream.co.ke",
                "http:///instagram.com/sstream.ke",
                "https:///www.tiktok.com/@sstreamke",
                "mailto:///hello@sstream.co.ke"
            ],
            "logos": [
                "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png",
                "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_180%2Ch_180%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png",
                "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_192%2Ch_192%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png"
            ],
            "name": "Sstream",
            "pages_url": {
                "about": "https:///www.sstream.co.ke/about-1",
                "contact": "https:///www.sstream.co.ke/contact",
                "careers": null,
                "services": "https://www.sstream.co.ke/events-1",
                "products": null
            },
            "phone_numbers": [],
            "social_media_links": {
                "facebook": [
                    "http:///www.facebook.com/sstreamke"
                ],
                "twitter": [
                    "https:///twitter.com/SstreamK"
                ],
                "instagram": [
                    "http:///instagram.com/sstream.ke"
                ],
                "linkedin": [
                    "https:///www.linkedin.com/in/sstreamkenya"
                ],
                "youtube": null,
                "reddit": null,
                "snapchat": null,
                "whatsapp": null,
                "telegram": null,
                "wechat": null,
                "tiktok": [
                    "https:///www.tiktok.com/@sstreamke"
                ],
                "soundcloud": null,
                "spotify": null,
                "medium": null,
                "quora": null,
                "twitch": null
            },
            "website_socials": null
        },
        "company_name": "Sstream",
        "phone_numbers": [],
        "addresses": null,
        "emails_found": [
            "hello@sstream.co"
        ],
        "verified_emails": [],
        "unverified_emails": [
            "hello@sstream.co"
        ],
        "logos": [
            "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_32%2Ch_32%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png",
            "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_180%2Ch_180%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png",
            "https:///static.wixstatic.com/media/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png/v1/fill/w_192%2Ch_192%2Clg_1%2Cusm_0.66_1.00_0.01/e1eb7c_573c09c5b1e24cc6bac97e0a85786494%7Emv2.png"
        ],
        "website_social_handles": null,
        "website_url": "https://www.sstream.co.ke"
    },
    "credits": 60
}
```



### Technologies Used

- [Python](https://nodejs.org/) is a programming language that lets you work more quickly and integrate your systems
  more effectively.
- [Storage] ()
- [Django](https://www.djangoproject.com/) is a high-level Python web framework that encourages rapid development and
  clean, pragmatic design.
- [Django Rest Framework](https://www.django-rest-framework.org/) Django REST framework is a powerful and flexible
  toolkit for building Web APIs.
- [MongoDB](https://www.mongodb.com/) is a free open source NOSQL document database with scalability and flexibility.
  Data are stored in flexible JSON-like documents.

### License

This project is available for use under
the [Apache](https://github.com/LL05-AI-Dowell/100107-DowellEmailExtractor.git0/blob/main/LICENSE) License.

