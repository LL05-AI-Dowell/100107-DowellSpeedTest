from rest_framework import generics, status
from rest_framework.response import Response

from .info_request import WebsiteInfoRequest, WebsiteInfoRequestSerializer



class WebsiteInfoExtractionAPIView(generics.GenericAPIView):
    serializer_class = WebsiteInfoRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            web_info_request = WebsiteInfoRequest(request_body=serializer.validated_data)
            web_info_request.validate(raise_exception=True)
            response = web_info_request.get_response()
            if response:
                return Response(response, status=status.HTTP_200_OK, headers={'Content-Type': 'application/json'})
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


website_info_extraction_api_view = WebsiteInfoExtractionAPIView.as_view()
