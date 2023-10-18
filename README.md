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
git clone `https://github.com/LL06-Reports-Analysis-Dowell/100056-DowellQRCodeGenertor2.0.git`

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
| POST       | api/v1/website-info-extractor/| To Get verified and unverifed emails Generated.                     |
| POST       | api/v1/contact-us-extractor/  | To retrieve the conctact-us-page
 Created     |
| POST       | api/v1/submit-contact-form/   | To Send data to contact-us-page 
 |