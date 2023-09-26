from typing import Dict
from django.core.exceptions import ValidationError
from django.http.response import JsonResponse

from .utils import WebsiteInfoScraper, sort_emails_by_validity
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
        self._body = dict(body)

    
    def __setattr__(self, __name: str, __value):
        """
        Sets the value of an attribute.
        """
        if __name == "_body":
            __value = self.validate_body(__value)
            self._url = __value.get(self.web_url_name, None)
            self._max_search_depth = __value.get(self.max_search_depth_name, 0)
            self._request = __value.get(self.info_request_name, {})
        return super().__setattr__(__name, __value)

 
    @property
    def body(self) -> Dict:
        """
        Request body
        """
        return self._body

    @body.setter
    def body(self, value: dict):
        """
        Sets request body
        """
        self._body = dict(value)
        
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
    
    @property
    def url(self) -> str:
        """
        Url of the target website
        """
        try:
            return self._url
        except AttributeError:
            raise ValidationError("Request body has not been set yet.")
    
    @property
    def max_search_depth(self) -> int:
        """
        Maximum search depth
        """
        try:
            return self._max_search_depth
        except AttributeError:
            raise ValidationError("Request body has not been set yet.")
        
    @property
    def request(self) -> Dict:
        """
        Info request
        """
        try:
            return self._request
        except AttributeError:
            raise ValidationError("Request body has not been set yet.")


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
            self._errors.update(exc.error_dict)
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
        info_scraper = self.scraper_class(web_url=self.url, max_search_depth=self.max_search_depth)
        result = {}
        for key, value in self.request.items():
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
            self._errors.update(exc.error_dict)
            return None
        return response_dict
    

    def get_json_response(self, api_key: str = None):
        """
        Returns a structured response of the info request as a `django.http.response.JsonResponse` object.
        If api_key is provided, the emails are sorted into verified and unverified emails.

        :param api_key: Dowell API key
        :return: The structured result gotten from processing the request
        :rtype: JsonResponse
        """
        response_dict = self.get_structured_response_dict(api_key=api_key)
        if response_dict:
            return JsonResponse(data=response_dict, status=200)
        return JsonResponse(data={"detail": self.errors}, status=400)


    def get_structured_response_dict(self, api_key: str = None):
        """
        Restructure the response dict for API response.
        If api_key is provided, the emails are sorted into verified and unverified emails.

        :param api_key: Dowell API key
        :return: Restructured response dict
        """
        response_dict = self.get_response_dict()
        if not response_dict:
            return None
        structured_dict = {}
        structured_dict["meta_data"] = response_dict
        emails = response_dict.get('emails', [])
        if emails and api_key:
            valid_emails, invalid_emails = self.sort_emails_by_validity(emails, api_key)
            structured_dict['verified_emails'] = valid_emails
            structured_dict['unverified_emails'] = invalid_emails
        structured_dict['company_name'] = response_dict.get('name', None)
        structured_dict['phone_numbers'] = response_dict.get('phone_numbers', None)
        structured_dict['addresses'] = response_dict.get('addresses', None)
        structured_dict["emails_found"] = response_dict.get("emails", None)
        structured_dict["logos"] = response_dict.get("logos", None)
        structured_dict["website_social_handles"] = response_dict.get("website_socials", None)
        structured_dict['website_url'] = self.scraper_class(web_url=self.url).engine.get_base_url(self.url)
        return structured_dict

