from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .misc import INFO_REQUEST_FORMAT


def is_valid_url(url):
    """
    Check if the url is valid
    """
    try:
        URLValidator()(url)
        return True
    except Exception:
        return False


class InfoRequestValidator:
    """
    Validator to validate the requested website info
    """

    def __init__(self, info_request_name: str = "info_request"):
        self.info_request_name = info_request_name


    def validate(self, info_request: dict):
        """
        Run validations on the info request passed

        :param info_request: The info request to validate
        :raises ValidationError
        """
        if not info_request:
            return INFO_REQUEST_FORMAT
        
        if not isinstance(info_request, dict):
            raise ValidationError(
                f"`{self.info_request_name}` must be a valid JSON object"
            )
        allowed_keys = list(INFO_REQUEST_FORMAT.keys())
        for key in info_request.keys():
            if key not in allowed_keys:
                raise ValidationError(
                    f"Invalid key `{key}` in `{self.info_request_name}`"
                )
        for key, value in info_request.items():
            try:
                getattr(self, f"validate_{type(INFO_REQUEST_FORMAT[key]).__name__}")(value, key)
            except AttributeError:
                raise ValidationError(
                    f"Invalid key `{key}` in `{self.info_request_name}`"
                )
        return info_request
    
    
    def validate_dict(self, _dict: dict, _dict_name: str):
        for key, value in _dict.items():
            try:
                getattr(self, f"validate_{type(INFO_REQUEST_FORMAT[_dict_name][key]).__name__}")(value, key)
            except (AttributeError, KeyError):
                raise ValidationError(
                    f"Invalid key `{key}` in `{self.info_request_name}.{_dict_name}`"
                )
    

    def validate_list(self, _list: list, _list_name: str):
        for item in _list:
            if not isinstance(item, str):
                raise ValidationError(
                    f"Invalid value `{item}` in `{self.info_request_name}.{_list_name}`. Value must be a string."
                )


    def validate_bool(self, _bool: bool, _bool_name: str):
        if not isinstance(_bool, bool):
            raise ValidationError(
                f"Invalid value `{_bool}` in `{self.info_request_name}.{_bool_name}`. Value must be a boolean."
            )
        

class WebsiteInfoRequestBodyValidator:
    """
    Validator for WebsiteInfoRequest body
    """
    web_url_name = "web_url"
    max_search_depth_name = "max_search_depth"
    info_request_name = "info_request"

    def __init__(self, **kwargs):
        """
        Initializes a WebsiteInfoRequestBodyValidator object.

        :param kwargs: Any other attributes to add to the object.
            :kwarg info_request_name: The name of the key in the request body that contains the info request. \
                Defaults to "info_request".
            :kwarg web_url_name: The name of the key in the request body that contains the url of the target website. \
                Defaults to "web_url".
            :kwarg max_search_depth_name: The name of the key in the request body that contains the maximum search depth. \
                Defaults to "max_search_depth".
        """
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise ValueError(f"Invalid keyword argument `{key}`")
            setattr(self, key, value)


    def validate(self, request_body: dict):
        """
        Run validations on the request body passed

        :param request_body: The request body to validate
        :raises ValidationError
        """
        if not isinstance(request_body, dict):
            raise ValidationError("Expected dict object for request body")
        
        web_url = request_body.get(self.web_url_name, None)
        if not web_url:
            raise ValidationError(f"Expected `{self.web_url_name}` to be present in request body")
        if not is_valid_url(web_url):
            raise ValidationError(f"Expected `{self.web_url_name}` to be a valid url, got {web_url} instead.")
        
        max_search_depth = request_body.get(self.max_search_depth_name, 0)
        if not isinstance(max_search_depth, int):
            raise ValidationError(f"Expected `{self.max_search_depth_name}` to be of type int, got {type(max_search_depth).__name__} instead")
        
        info_request = request_body.get(self.info_request_name, None)
        if not info_request:
            raise ValidationError(f"Expected `{self.info_request_name}` to be present in request body")
        else:
            InfoRequestValidator(self.info_request_name).validate(info_request)
        return request_body
        
        
