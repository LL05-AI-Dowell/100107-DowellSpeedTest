from django.core.exceptions import ValidationError
from django.http.response import JsonResponse

from .utils import WebsiteInfoScraper
from .validators import WebsiteInfoRequestBodyValidator
from .misc import info_request_smc, INFO_REQUEST_FORMAT



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
    _errors = {}
    raise_exception = True

    def __init__(self, body: dict, **kwargs):
        """
        Initializes a WebsiteInfoRequest object.

        :param body: The request body as a dictionary.
        :param kwargs: Any other attributes to add to the object.
            :kwarg info_request_name: The name of the key in the request body that contains the info request. \
                Defaults to "info_request".
            :kwarg web_url_name: The name of the key in the request body that contains the url of the target website. \
                Defaults to "web_url".
            :kwarg max_search_depth_name: The name of the key in the request body that contains the maximum search depth. \
                Defaults to "max_search_depth".
            :kwarg raise_exception: Whether to raise exception encountered when initializing or processing request. \
                If False, the exception details are still accessible by `self.errors`
        """
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise ValueError(f"Invalid keyword argument `{key}`")
            setattr(self, key, value)
        # Set body after other kwargs have been set, because body validation may depend on them
        self._body = self.validate_body(dict(body))

 
    @property
    def body(self):
        """
        Request body
        """
        return self._body

    @body.setter
    def set_body(self, value: dict):
        """
        Sets request body
        """
        self._body = self.validate_body(value)

    @property
    def errors(self):
        """
        Errors encountered when initializing or processing request
        """
        return self._errors

    @property
    def is_valid(self):
        """
        Checks whether the request body is valid or not.
        """
        return self._is_valid


    def validate_body(self, body: dict):
        """
        Validates the request body.

        :param body: request body to validate
        :return: validated body
        :raises: ValidationError if the request body is not valid and raise_exception is True.
        """
        try:
            WebsiteInfoRequestBodyValidator(
                web_url_name=self.web_url_name,
                max_search_depth_name=self.max_search_depth_name,
                info_request_name=self.info_request_name
            ).validate(body)
        except ValidationError as exc:
            if self.raise_exception:
                raise exc
            self.errors.update(exc.error_dict)
            self._is_valid = False
        else:
            self._is_valid = True
        return body
    

    def process(self, method_correspondence: dict = info_request_smc):
        """
        Processes the request.

        :param method_correspondence: A dictionary that maps the keys in the info request to the methods of `self.scraper_class` class.
        """
        if not self.is_valid:
            raise ValidationError(
                "WebsiteInfoRequest is not valid. Cannot process request. \
                    Check self.errors for more information."
            )
        web_url = self.body.get(self.web_url_name, None)
        max_search_depth = self.body.get(self.max_search_depth_name, 0)
        info_scraper = self.scraper_class(web_url=web_url, max_search_depth=max_search_depth)
        info_request : dict = self.body.get(self.info_request_name)

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
                elif value:
                    result[key] = getattr(info_scraper, method_correspondence[key])()
        # Validate the result
        return self.validate_processed_result(result)
    
    
    def validate_processed_result(self, result: dict):
        """
        Validates the result of processing the request

        :param result: The result of processing info request.
        :return: True if the result is valid, False otherwise.
        """
        if not isinstance(result, dict):
            raise ValidationError(f"Expected `result` to be of type dict, got `{type(result).__name__}` instead")
        # Class to validate the response will be written and used here later
        for key, value in result.items():
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
        return result
            

    def get_response_dict(self):
        """
        Gets the response of the info request as dictionary.

        :return: The result of gotten from processing the request
        :rtype: dict
        """
        try:
            response_dict = self.process()
        except ValidationError as exc:
            if self.raise_exception:
                raise exc
            self.errors.update(exc.error_dict)
            return None
        return response_dict
    

    def get_http_response(self):
        """
        Returns the response of the info request as an HTTPResponse object.

        :return: The result of gotten from processing the request
        :rtype: HTTPResponse
        """
        response_dict = self.get_response_dict()
        if response_dict:
            return JsonResponse(data=response_dict,status=200)
        return JsonResponse(data={"detail": self.errors}, status=400)

