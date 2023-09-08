from rest_framework import generics, status
from rest_framework.response import Response

from .requests import WebsiteInfoRequest
from .serializers import WebsiteInfoRequestSerializer



class WebsiteInfoExtractionAPIView(generics.GenericAPIView):
    serializer_class = WebsiteInfoRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            web_info_request = WebsiteInfoRequest(body=serializer.validated_data)
            response = web_info_request.get_http_response()
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


website_info_extraction_api_view = WebsiteInfoExtractionAPIView.as_view()
