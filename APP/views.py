
from rest_framework import generics, status, decorators
from rest_framework.response import Response


from APP.utils import processApikey
from .requests import WebsiteInfoRequest
from .serializers import WebsiteInfoRequestSerializer
from .misc import INFO_REQUEST_FORMAT


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
            
            # Call the processApikey function to validate the API key
            api_key_response = processApikey(api_key)
            
            if api_key_response.get('success'):
                # If the API key is valid, proceed with website info extraction
                web_info_request = WebsiteInfoRequest(body=validated_data)
                response_dict = web_info_request.get_structured_response_dict(api_key)

                if response_dict:
                    return Response(response_dict, status=status.HTTP_200_OK)
                return Response(web_info_request.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # If the API key is not valid, return an error response
                return Response({"error": "Invalid API key"}, status=status.HTTP_401_UNAUTHORIZED)

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
