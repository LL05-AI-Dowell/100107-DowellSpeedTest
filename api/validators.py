from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def is_valid_url(url):
    """
    Check if the url is valid
    """
    try:
        URLValidator()(url)
        return True
    except Exception:
        return False
