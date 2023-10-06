from rest_framework import generics, status, decorators
from rest_framework.response import Response

from .serializers import ContactInfoRequestSerializer, WebsiteInfoRequestSerializer

from utils.scraper import WebsiteInfoScraper
from utils.requests import WebsiteInfoRequest
from utils.misc import INFO_REQUEST_FORMAT


class WebsiteInfoExtractionAPIView(generics.GenericAPIView):
    """
    API view for website info extraction.
    """
    serializer_class = WebsiteInfoRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            api_key = validated_data.pop('api_key', None)
            web_info_request = WebsiteInfoRequest(body=validated_data)
            response_dict = web_info_request.get_structured_response_dict(api_key)

            if response_dict:
                return Response(response_dict, status=status.HTTP_200_OK)
            return Response(web_info_request.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@decorators.api_view(['GET'])
def request_format_api_view(request, *args, **kwargs):
    """
    API view for getting website info extraction request format.
    """
    if request.method == 'GET':
        return Response(INFO_REQUEST_FORMAT, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


website_info_extraction_api_view = WebsiteInfoExtractionAPIView.as_view()


class ContactUsAPI(generics.GenericAPIView):
    serializer_class = ContactInfoRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            contact_us_url = serializer.data.get("contact_us_url")
            # validated_data = serializer.validated_data
            web_info_scraper = WebsiteInfoScraper(web_url=contact_us_url)
            response_dict = web_info_scraper.scrape_contact_us_page(web_url=contact_us_url)

            # if response_dict:
            return Response(response_dict, status=status.HTTP_200_OK)
            # return Response("Error" , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
contact_us_api_view = ContactUsAPI.as_view()