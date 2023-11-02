from django.urls import path

from .views import WebsiteInfoExtractionAPIView, PrivateContactUsFormExtractorAPI, request_format_api_view


urlpatterns = [
    path('website-info-extractor/', WebsiteInfoExtractionAPIView.as_view(), name='info-extraction-api'),
    path('website-info-extractor/request-format/', request_format_api_view, name='info-extraction-request-format-api'),
    path('contact-us-extractor/', PrivateContactUsFormExtractorAPI.as_view(), name='contact-us-extractor'),

]