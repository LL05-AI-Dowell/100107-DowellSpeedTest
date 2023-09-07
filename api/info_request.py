import gzip
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.core.validators import URLValidator


from .validators import is_valid_url
from .utils import WebsiteInfoScraper

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


class InfoRequestValidator:
    """
    Serializer validator to validate the requested website info
    """

    def __init__(self, field_name: dict = "info_request"):
        self.field_name = field_name


    def validate(self, info_request: dict):
        if not info_request:
            return INFO_REQUEST_FORMAT
        if info_request:
            if not isinstance(info_request, dict):
                raise ValidationError(
                    f"`{self.field_name}` must be a valid JSON object"
                )
            allowed_keys = list(INFO_REQUEST_FORMAT.keys())
            for key in info_request.keys():
                if key not in allowed_keys:
                    raise ValidationError(
                        f"Invalid key `{key}` in `{self.field_name}`"
                    )
            for key, value in info_request.items():
                try:
                    getattr(self, f"validate_{type(INFO_REQUEST_FORMAT[key]).__name__}")(value, key)
                except AttributeError:
                    raise ValidationError(
                        f"Invalid key `{key}` in `{self.field_name}`"
                    )
        return info_request
    
    
    def validate_dict(self, _dict: dict, _dict_name: str):
        for key, value in _dict.items():
            try:
                getattr(self, f"validate_{type(INFO_REQUEST_FORMAT[_dict_name][key]).__name__}")(value, key)
            except (AttributeError, KeyError):
                raise ValidationError(
                    f"Invalid key `{key}` in `{self.field_name}.{_dict_name}`"
                )
    

    def validate_list(self, _list: list, _list_name: str):
        for item in _list:
            if not isinstance(item, str):
                raise ValidationError(
                    f"Invalid value `{item}` in `{self.field_name}.{_list_name}`.\
                        Value must be a string value"
                )


    def validate_bool(self, _bool: bool, _bool_name: str):
        if not isinstance(_bool, bool):
            raise ValidationError(
                f"Invalid value `{_bool}` in `{self.field_name}.{_bool_name}`.\
                    Value must be a boolean value"
            )
        


class InfoResponseValidator:
    pass
        


class WebsiteInfoRequest:
    """
    Object to represent a request to find information about a website.
    """

    _is_valid = False
    _body = None
    info_request_name = "info_request" 
    web_url_name = "web_url"
    max_search_depth_name = "max_search_depth"
    scraper_class = WebsiteInfoScraper

    def __init__(self, request_body: dict, **kwargs) -> None:
        """
        Initializes a WebsiteInfoRequest object.

        :param request_body: The request body as a dictionary.
        :param kwargs: Any other attributes to add to the object.
            :kwarg info_request_name: The name of the field in the request body that contains the info request. \
                Defaults to "info_request".
            :kwarg web_url_name: The name of the field in the request body that contains the url of the target website. \
                Defaults to "web_url".
            :kwarg max_search_depth_name: The name of the field in the request body that contains the maximum search depth. \
                Defaults to "max_search_depth".
        """
        self._body = dict(request_body)
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise ValueError(f"Invalid keyword argument `{key}`")
            setattr(self, key, value)
            

    @property
    def body(self):
        """
        Request body
        """
        if not self.is_valid:
            raise Exception("WebsiteInfoRequest is not valid. Request body might have not been validated yet")
        return self._body
    
    @property
    def is_valid(self):
        """
        Checks whether the request body is valid or not.
        """
        return self._is_valid


    def validate(self, raise_exception: bool = False):
        """
        Validates the request body.

        :param raise_exception: Whether to raise an exception if the request body is not valid.
        :return: True if the request body is valid, False otherwise.
        :raises: ValidationError if the request body is not valid and raise_exception is True.
        """
        try:
            InfoRequestValidator(self.info_request_name).validate(self._body.get(self.info_request_name))
        except ValidationError as exc:
            if raise_exception:
                raise exc
            self._is_valid = False
        else:
            self._is_valid = True
        return None
    

    def process(self, method_correspondence: dict = info_request_smc):
        """
        Processes the info request.

        :param method_correspondence: A dictionary that maps the keys in the info request to the methods of the WebsiteInfoScraper class.
        """
        if not self.is_valid:
            raise ValidationError("WebsiteInfoRequest is not valid. Call the validate method first to see why.")
        web_url = self.body.get(self.web_url_name, None)
        max_search_depth = self.body.get(self.max_search_depth_name, 0)
        if not is_valid_url(web_url):
            raise ValueError(f"Expected `{self.web_url_name}` to be a valid url, got {web_url} instead.")
        info_scraper = self.scraper_class(web_url=web_url, max_search_depth=max_search_depth)
        info_request = self.body.get(self.info_request_name)
        result = {}
        for key, value in info_request.items():
            if key in method_correspondence:
                if isinstance(value, dict):
                    if value.get("all", False):
                        result[key] = getattr(info_scraper, method_correspondence[key]["all"])()
                    elif value.get("choices", None):
                        result[key] = getattr(info_scraper, method_correspondence[key]["choices"])(value["choices"])
                elif isinstance(value, list):
                    result[key] = getattr(info_scraper, method_correspondence[key])(value)
                else:
                    result[key] = getattr(info_scraper, method_correspondence[key])()
        return result
    
    
    def validate_response(self, response: dict):
        """
        Validates the response of the info request.

        :param response: The response of the info request.
        :return: True if the response is valid, False otherwise.
        """
        if not self.is_valid:
            raise ValidationError("WebsiteInfoRequest is not valid. Call the validate method first to see why.")
        
        # Class to validate the response will be written and used here later
        for key, value in response.items():
            if key not in INFO_REQUEST_FORMAT:
                raise ValidationError(f"Invalid key `{key}` in response")
            if isinstance(value, dict):
                if value and not all([ isinstance(val[0], str) for val in value.values() if val and isinstance(val, list) ]):
                    raise ValidationError(f"Expected all items in value of key `{key}` to be of type str, got `{type(list(value.values())[0]).__name__}` instead")
            elif isinstance(value, list):
                if value and not all([ isinstance(item, str) for item in value ]):
                    raise ValidationError(f"Expected all items in value of key `{key}` to be of type str, got `{type(value[0]).__name__}` instead")
            elif isinstance(value, str):
                pass
        return None
            

    def get_response(self, raise_exception: bool = True):
        """
        Gets the response of the info request.

        :param raise_exception: Whether to raise an exception if any error occurs. Defaults to True
        :return: The response of the info request.
        :rtype: bytes
        :raises: ValidationError
        """
        try:
            response = self.process()
            self.validate_response(response)
        except ValidationError as exc:
            if raise_exception:
                raise exc
            return None
        if response.__sizeof__() > 1024:
            return gzip.compress(str(response).encode())
        return str(response).encode()   



class WebsiteInfoRequestSerializer(serializers.Serializer):
    """
    Quick serializer implementation for website info requests.

    For quick testing, use the following snippet in the shell:
    ```
    from website_info.api.serializers import WebsiteInfoRequestSerializer
    from website_info.api.info_request import INFO_REQUEST_FORMAT
    serializer = WebsiteInfoRequestSerializer(data={"web_url": "https://dribbble.com/", "info_request": INFO_REQUEST_FORMAT})
    serializer.is_valid(raise_exception=True)
    serializer.validated_data
    ```
    """
    web_url = serializers.URLField(validators=[URLValidator], required=True)
    max_search_depth = serializers.IntegerField(min_value=0, max_value=2, required=False)
    info_request = serializers.JSONField(write_only=True, required=True, initial=INFO_REQUEST_FORMAT, validators=[InfoRequestValidator().validate])

