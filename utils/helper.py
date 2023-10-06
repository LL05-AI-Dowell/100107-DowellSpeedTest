import json
import re
import requests
from typing import Iterable, List

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
