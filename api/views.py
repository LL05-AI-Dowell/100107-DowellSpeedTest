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
            response_dict = web_info_request.get_response_dict()
            if response_dict:
                return Response(response_dict, status=status.HTTP_200_OK)
            serializer.errors.update(web_info_request.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


website_info_extraction_api_view = WebsiteInfoExtractionAPIView.as_view()
