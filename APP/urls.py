from django.urls import path
from . import views
from .views import submit_contact_form

# app_name = "api"

urlpatterns = [
    path('submit-contact-form/', submit_contact_form, name='submit_contact_form'),
    path('contact-us-extractor/', views.ContactUsAPI.as_view(), name='contact-us-extractor'),

    path('download-csv/', views.download_csv_form, name='download_csv_form'),

    path('website-info-extractor/', views.website_info_extraction_api_view, name='info-extraction-api'),
    path('website-info-extractor/request-format/', views.request_format_api_view, name='info-extraction-request-format-api')
]
