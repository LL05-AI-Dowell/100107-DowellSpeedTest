from django.urls import path

from . import views

# app_name = "api"

urlpatterns = [
    path('website-info-extractor/', views.website_info_extraction_api_view, name='info-extraction-api'),
    path('website-info-extractor/request-format/', views.request_format_api_view, name='info-extraction-request-format-api')
]
