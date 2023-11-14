# 100107-DowellEmailExtractor

## Summary

This project involves the Scrapping web_urls through an API using
a scrapper library to extact infomation within the different website

 The API supports the Extaction data
with various options such as getting the meta_data which includes
the page_urls,phone_numbers,socil_media_links, name , logos,
company_name,emails found and the website_url

Clients can Extract data by providing a weburl,
 The API will return an extracted data with all metadata

The API also supports getting verified or unverified emails by passing
the apikey alongside getting all metadata of the site

Overall, this API provides a convenient way for clients to get data
of any site regardless of the web_url

## Prerequisites

Before you begin, make sure you have the following software installed on your computer:
    .Python 3.7+

## Step 1: Setting up the Django project in your local machine

Clone project by running the following command in your terminal:
git clone `https://github.com/LL05-AI-Dowell/100107-DowellEmailExtractor.git`

## Step 2: Run the Project in your local environment

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

## BASE_URL

`https://www.uxlive.me/`

| HTTP Verbs | Endpoints                      | Action                                               |
|------------|--------------------------------|------------------------------------------------------|
| POST       | api/website-info-extractor/    | To get meta_data by passing the web url              |
| POST       | api/v1/website-info-extractor/ | To Get verified and unverifed emails Generated.      |
| POST       | api/contact-us-extractor/      | To retrieve the conctact-us-page Created             |
| POST       | api/submit-contact-form/       | To Send data to contact-us-page
| GET        | api/download-csv/              | To download the excel file                           |
| POST       | api/submit-csv/                | To submit the csv file                               |

## Endpoints Definition(Request - Response)

## Extract metadata by scrapping

POST: `/api/website-info-extractor/`

Request Body

```json
{
    "web_url": "https://www.uxlivinglab.org/",
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
            "all": false,
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
            "addresses": [
            "150000 locations worldwide.   Experience  License CompatibilityCheck license compatibility between different software components used in a project.   Experience    Previous  NextGrow with UX Living LabGrow with  UX Living Lab We are looking for independent sales agents to distribute our software applications in various small business sectors like Schools, Hotels, Coffee shops, Salons, Corner stores and Boutiques. The agent should interact with small business owners in their area and sell the software.   Learn More  Contact UX Living LabContact  UX Living Lab Do you have any questions, or enquiries about our products"
            ],
            "emails": [],
            "links": [
            "https:///www.uxlivinglab.org",
            "https:///www.uxlivinglab.org/products/samanta_content_evaluator",
            "https:///amzn.to/44o4Zi6",
            "https:///www.uxlivinglab.org/products/dowell-workflow-ai",
            "https:///www.uxlivinglab.org/products/social-media-automation",
            "https:///www.uxlivinglab.org/products/live-stream-dashboard",
            "https:///dowellresearch.se",
            "https:///www.uxlivinglab.org/products/dowell-wifi-qr-code",
            "https:///github.com/DoWellUXLab",
            "https:///100093.pythonanywhere.com/?session_id=zbyzzqnvc1srluvgrvp4sh7poyw7orik",
            "https:///www.facebook.com/livinglabstories",
            "https:///www.uxlivinglab.org/products/open_source_license_compatibility",
            "https://www.uxlivinglab.org#content",
            "https:///www.uxlivinglab.org/products/dowell-legalzard",
            "https:///www.salesagent.dowellstore.org",
            "https:///play.google.com/store/apps/developer?id=DoWell+UX+Living+Lab&hl=en-IN",
            "https:///play.google.com/store/apps/developer?id=DoWell+UX+Living+Lab&hl=en-IN%20",
            "https:///ll07-team-dowell.github.io/Jobportal/#/?view=product&qr_id=WfV11hriuSx1&company_id=6385c0f18eca0fb652c94561&company_data_type=Real_Data&link_id=1685907997681652206",
            "https:///www.uxlivinglab.org/privacy-policy",
            "https:///search-livinglab.flutterflow.app",
            "https:///apps.apple.com/us/developer/dowell-research/id1648847971",
            "https:///100014.pythonanywhere.com",
            "https:///www.uxlivinglab.org/about-us",
            "https:///play.google.com/store/apps/developer?id=DoWell+UX+Living+Lab",
            "https:///www.uxlivinglab.org/products/digital-queue",
            "https:///dowellresearch.sg",
            "https:///www.youtube.com/channel/UC_Ftf9dTQtKHS2N0KD0duwg",
            "https:///www.uxlivinglab.org/products/team-management",
            "https:///www.uxlivinglab.org/dowell-ux-living-lab-extension",
            "https:///dowellresearch.uk",
            "https:///www.uxlivinglab.org/products/living-lab-maps",
            "https:///twitter.com/uxlivinglab",
            "https:///uk.linkedin.com/showcase/uxlivinglab",
            "https:///www.uxlivinglab.org/products/living-lab-chat",
            "https:///dowell-research.myshopify.com",
            "https:///www.uxlivinglab.org/products/dowell-living-lab",
            "https:///www.uxlivinglab.org/products/web_crawler",
            "https:///www.uxlivinglab.org/products/qr-code-generator-2",
            "https:///dowellresearch.de",
            "https://www.uxlivinglab.org",
            "https:///www.uxlivinglab.org/products",
            "https:///www.uxlivinglab.org/products/dowell-logo-scan",
            "https:///www.uxlivinglab.org/products/permutation-calculator",
            "https:///www.uxlivinglab.org/contact",
            "https:///www.uxlivinglab.org/products/dowell-cx-live",
            "https:///www.uxlivinglab.org/products/dowell-ux-live",
            "https:///ll04-finance-dowell.github.io/100088-dowellpayment",
            "https:///dowellresearch.uk/project-scenario",
            "https:///www.uxlivinglab.org/products/voice-of-customers",
            "https:///calendly.com/uxlivinglab/30?month=2023-08",
            "https:///www.instagram.com/livinglabstories"
            ],
            "logos": [
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/09/Untitled-design.jpg",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-180x180.png",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-32x32.png",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-192x192.png"
            ],
            "name": "DoWell UX Living Lab",
            "pages_url": {
            "about": "https:///www.uxlivinglab.org/about-us",
            "products": "https:///www.uxlivinglab.org/products/samanta_content_evaluator",
            "contact": "https:///www.uxlivinglab.org/contact",
            "careers": null,
            "services": null
            },
            "phone_numbers": [
            "168590799768",
            "1652206",
            "1648847971"
            ],
            "social_media_links": {
            "facebook": [
                "https:///www.facebook.com/livinglabstories"
            ],
            "twitter": [
                "https:///twitter.com/uxlivinglab"
            ],
            "instagram": [
                "https:///www.instagram.com/livinglabstories"
            ],
            "linkedin": [
                "https:///uk.linkedin.com/showcase/uxlivinglab"
            ],
            "youtube": [
                "https:///www.youtube.com/channel/UC_Ftf9dTQtKHS2N0KD0duwg"
            ],
            "pinterest": null,
            "tumblr": null,
            "snapchat": null
            },
            "website_socials": null
        },
        "company_name": "DoWell UX Living Lab",
        "phone_numbers": [
            "168590799768",
            "1652206",
            "1648847971"
        ],
        "addresses": [
            "150000 locations worldwide.   Experience  License CompatibilityCheck license compatibility between different software components used in a project.   Experience    Previous  NextGrow with UX Living LabGrow with  UX Living Lab We are looking for independent sales agents to distribute our software applications in various small business sectors like Schools, Hotels, Coffee shops, Salons, Corner stores and Boutiques. The agent should interact with small business owners in their area and sell the software.   Learn More  Contact UX Living LabContact  UX Living Lab Do you have any questions, or enquiries about our products"
        ],
        "emails_found": [],
        "logos": [
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/09/Untitled-design.jpg",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-180x180.png",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-32x32.png",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-192x192.png"
        ],
        "website_social_handles": null,
        "website_url": "https://www.uxlivinglab.org"
}
```

POST: `/api/v1/website-info-extractor/`

Request Body

```json
{   
    "api_key": "<your-api-key>",
    "web_url": "https://www.uxlivinglab.org/",
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
        "meta_data": {
            "addresses": [
            "150000 locations worldwide.   Experience  License CompatibilityCheck license compatibility between different software components used in a project.   Experience    Previous  NextGrow with UX Living LabGrow with  UX Living Lab We are looking for independent sales agents to distribute our software applications in various small business sectors like Schools, Hotels, Coffee shops, Salons, Corner stores and Boutiques. The agent should interact with small business owners in their area and sell the software.   Learn More  Contact UX Living LabContact  UX Living Lab Do you have any questions, or enquiries about our products"
            ],
            "emails": [],
            "links": [
            "https:///www.uxlivinglab.org",
            "https:///www.uxlivinglab.org/products/samanta_content_evaluator",
            "https:///amzn.to/44o4Zi6",
            "https:///www.uxlivinglab.org/products/dowell-workflow-ai",
            "https:///www.uxlivinglab.org/products/social-media-automation",
            "https:///www.uxlivinglab.org/products/live-stream-dashboard",
            "https:///dowellresearch.se",
            "https:///www.uxlivinglab.org/products/dowell-wifi-qr-code",
            "https:///github.com/DoWellUXLab",
            "https:///100093.pythonanywhere.com/?session_id=zbyzzqnvc1srluvgrvp4sh7poyw7orik",
            "https:///www.facebook.com/livinglabstories",
            "https:///www.uxlivinglab.org/products/open_source_license_compatibility",
            "https://www.uxlivinglab.org#content",
            "https:///www.uxlivinglab.org/products/dowell-legalzard",
            "https:///www.salesagent.dowellstore.org",
            "https:///play.google.com/store/apps/developer?id=DoWell+UX+Living+Lab&hl=en-IN",
            "https:///play.google.com/store/apps/developer?id=DoWell+UX+Living+Lab&hl=en-IN%20",
            "https:///ll07-team-dowell.github.io/Jobportal/#/?view=product&qr_id=WfV11hriuSx1&company_id=6385c0f18eca0fb652c94561&company_data_type=Real_Data&link_id=1685907997681652206",
            "https:///www.uxlivinglab.org/privacy-policy",
            "https:///search-livinglab.flutterflow.app",
            "https:///apps.apple.com/us/developer/dowell-research/id1648847971",
            "https:///100014.pythonanywhere.com",
            "https:///www.uxlivinglab.org/about-us",
            "https:///play.google.com/store/apps/developer?id=DoWell+UX+Living+Lab",
            "https:///www.uxlivinglab.org/products/digital-queue",
            "https:///dowellresearch.sg",
            "https:///www.youtube.com/channel/UC_Ftf9dTQtKHS2N0KD0duwg",
            "https:///www.uxlivinglab.org/products/team-management",
            "https:///www.uxlivinglab.org/dowell-ux-living-lab-extension",
            "https:///dowellresearch.uk",
            "https:///www.uxlivinglab.org/products/living-lab-maps",
            "https:///twitter.com/uxlivinglab",
            "https:///uk.linkedin.com/showcase/uxlivinglab",
            "https:///www.uxlivinglab.org/products/living-lab-chat",
            "https:///dowell-research.myshopify.com",
            "https:///www.uxlivinglab.org/products/dowell-living-lab",
            "https:///www.uxlivinglab.org/products/web_crawler",
            "https:///www.uxlivinglab.org/products/qr-code-generator-2",
            "https:///dowellresearch.de",
            "https://www.uxlivinglab.org",
            "https:///www.uxlivinglab.org/products",
            "https:///www.uxlivinglab.org/products/dowell-logo-scan",
            "https:///www.uxlivinglab.org/products/permutation-calculator",
            "https:///www.uxlivinglab.org/contact",
            "https:///www.uxlivinglab.org/products/dowell-cx-live",
            "https:///www.uxlivinglab.org/products/dowell-ux-live",
            "https:///ll04-finance-dowell.github.io/100088-dowellpayment",
            "https:///dowellresearch.uk/project-scenario",
            "https:///www.uxlivinglab.org/products/voice-of-customers",
            "https:///calendly.com/uxlivinglab/30?month=2023-08",
            "https:///www.instagram.com/livinglabstories"
            ],
            "logos": [
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/09/Untitled-design.jpg",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-180x180.png",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-32x32.png",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-192x192.png"
            ],
            "name": "DoWell UX Living Lab",
            "pages_url": {
            "about": "https:///www.uxlivinglab.org/about-us",
            "products": "https:///www.uxlivinglab.org/products/samanta_content_evaluator",
            "contact": "https:///www.uxlivinglab.org/contact",
            "careers": null,
            "services": null
            },
            "phone_numbers": [
            "168590799768",
            "1652206",
            "1648847971"
            ],
            "social_media_links": {
            "facebook": [
                "https:///www.facebook.com/livinglabstories"
            ],
            "twitter": [
                "https:///twitter.com/uxlivinglab"
            ],
            "instagram": [
                "https:///www.instagram.com/livinglabstories"
            ],
            "linkedin": [
                "https:///uk.linkedin.com/showcase/uxlivinglab"
            ],
            "youtube": [
                "https:///www.youtube.com/channel/UC_Ftf9dTQtKHS2N0KD0duwg"
            ],
            "pinterest": null,
            "tumblr": null,
            "snapchat": null
            },
            "website_socials": null
        },
        "company_name": "DoWell UX Living Lab",
        "phone_numbers": [
            "168590799768",
            "1652206",
            "1648847971"
        ],
        "addresses": [
            "150000 locations worldwide.   Experience  License CompatibilityCheck license compatibility between different software components used in a project.   Experience    Previous  NextGrow with UX Living LabGrow with  UX Living Lab We are looking for independent sales agents to distribute our software applications in various small business sectors like Schools, Hotels, Coffee shops, Salons, Corner stores and Boutiques. The agent should interact with small business owners in their area and sell the software.   Learn More  Contact UX Living LabContact  UX Living Lab Do you have any questions, or enquiries about our products"
        ],
        "emails_found": [],
        "logos": [
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/09/Untitled-design.jpg",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-180x180.png",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-32x32.png",
            "https:///www.uxlivinglab.org/wp-content/uploads/2023/08/cropped-cropped-Livinglab-192x192.png"
        ],
        "website_social_handles": null,
        "website_url": "https://www.uxlivinglab.org"
}
```

POST: `/api/contact-us-extractor/`

Request body

```json
    {
        "page_link": "https://ineuron.ai/contact-us"
    }
```

Note:
This endpoint api is used to extract contact-us-api of the page_link provided

Response - 200

```json
[
      {
            "form_index": 0,
            "name": "text",
            "email": "email",
            "tel": "tel",
            "message": "textarea"
      },
     {
            "form_index": 1,
            "name": "text",
            "orgName": "text",
            "email": "email",
            "tel": "tel",
            "message": "textarea"
     }
]
```

POST: `/api/submit-contact-form/`

Request body

```json
 {
    "page_link": "https://giantmillers.co.ke/contact/",
    "form_data": [
        {
            "form_index": 1,
            "your-name": "John Namu",
            "your-email": "namu@gmail.com",
            "phonenumber": "+254743923232",
            "your-subject": "Maize",
            "your-message": "Maize Meal"
        }
    ]
}
```

Note:
This endpoint api is used to POST data to the contact us page of the given url

Response - 200

```json
   {
    "success": [
        "Form 1 submitted successfully."
    ]
}
```

POST:`/api/download-csv/?web_url=https://ineuron.ai/contact-us&file_type=xlsx`

Note:
This endpoint api is used to Download data to the contact us page of the given url

PARAMS:

```json
    {
        web_url : "https://ineuron.ai/contact-us"
        file_type : xlsx | csv
    }
```

Response - 200

If the Response is 200 it will return the xml file code digits

POST: `/api/submit-csv/`

Request body

```json
 {
    "page_link": "https://ineuron.ai/contact-us",
 }
```

Note:
This endpoint api is used to SUBMIT the csv excel form file extracted from downloading the contact-us csv file

Response - 200

```json
   {
    "success": [
        "Form 1 submitted successfully."
    ]
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
