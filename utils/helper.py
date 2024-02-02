import base64
import json
import re
import time
import uuid
import requests
from typing import Iterable, List
from urllib.parse import urlparse

from config import settings


def updateUsage(occurences, email):
    url = "https://100105.pythonanywhere.com/api/v3/experience_database_services/"
    params = {
        "type": "update_user_usage",
        "product_number": "UXLIVINGLAB005",
        "email": email,
        "occurrences": occurences
    }
    response = requests.get(url, params=params)
    return response.json()

def experienceUserDetails(email, title, content):
    url = "https://100105.pythonanywhere.com/api/v3/experience_database_services/"
    payload = {
        "product_name":"WEBSITE CRAWL",
        "email": email,
        "experienced_data":{
            "Title": title,
            "Content": content,
            "email": email
        }
    }
    params = {
        "type": "experienced_user_details"
    }
    response = requests.post(url, json=payload, params=params)
    return response.json()

def serviceExperienceUSerDetails(occurences, email,product_number ):
    url = settings.EXPERIENCED_SERVICE_USER_DETAILS_API
    payload = {
        "email": email,
        "product_number": product_number,
        "occurrences": occurences
    }
    response = requests.post(url, json=payload)
    return response


def processApikey(api_key):
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    payload = {
        "service_id": "DOWELL10045"
    }
    response = requests.post(url, json=payload)
    response_text = json.loads(response.text)
    return response_text


def is_email(address: str):
    """
    Checks if the address provided is a valid email address

    :param address: email address to be checked
    :return: True if address is an email address else false
    """
    match = re.match(r'[-|\w\.]+@\w+.\w{2,}', address)
    return match != None


email_api_url = lambda api_key: "https://100085.pythonanywhere.com/api/uxlivinglab/verify-email/"


def validate_email(email_address: str) -> bool:
    """
    Check is the email address provided is a valid and active email address using Dowell Email API.

    :param email_address: email address to validate
    :param api_key: user's dowell client admin api key.
    :return: True if valid else False
    """
    email = email_address

    if not is_email(email_address):
        raise ValueError("email_address value is not valid")
    response = requests.post(
        data={"email": email_address}, 
    )
    if response.status_code != 200:
        response.raise_for_status()
    return response.json()["success"]




def sort_emails_by_validity(emails: Iterable[str]) -> tuple[List[str], List[str]]:
    """
    Sorts a list of emails into valid and invalid emails.
    Uses Dowell Email API to determine email validity.

    NOTE: Make sure Dowell Email service is activated for API key else all emails will be classified as invalid

    :param emails: A list of emails to sort.
    :param api_key: user's dowell client admin api key.
    :return: A tuple of two lists. The first list contains valid emails and the second list contains invalid emails.
    """
    valid = []
    invalid = []
    if not isinstance(emails, Iterable):
        raise TypeError("Expected emails to be an iterable of strings")
    for email in emails:
        try:
            if validate_email(email):
                valid.append(email)
            else:
                invalid.append(email)
        except Exception:
            invalid.append(email)
    return valid, invalid

def cleanUrl(url):
    parsed_url = urlparse(url)
    cleaned_url = parsed_url.netloc
    return cleaned_url


def create_short_uuid():
    uuid_value = uuid.uuid4().bytes
    base64_encoded = base64.urlsafe_b64encode(uuid_value).rstrip(b'=')

    # Get the current timestamp (in seconds) and convert it to base64
    current_timestamp = int(time.time())
    timestamp_bytes = str(current_timestamp).encode('utf-8')
    # timestamp_base64 = base64.urlsafe_b64encode(timestamp_bytes).rstrip(b'=')
    # Combine the short UUID and timestamp component
    combined_uuid = base64_encoded[:4] + base64_encoded[-4:]
    return combined_uuid.decode('utf-8')  # Convert bytes back to string
