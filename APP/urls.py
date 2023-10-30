from django.urls import path
from . import views
from .views import submit_contact_form, ContactUsFormExtractorAPI, WebsiteInfoExtractionAPIView

# app_name = "api"

urlpatterns = [
    path('submit-contact-form/', submit_contact_form, name='submit_contact_form'),
    path('contact-us-extractor/', ContactUsFormExtractorAPI.as_view(), name='contact-us-extractor'),

    path('download-csv/', views.download_csv_form, name='download_csv_form'),
    path('submit-csv/', views.submit_contact_form_excel, name='submit_excel_file'),

    path('website-info-extractor/', WebsiteInfoExtractionAPIView.as_view(), name='info-extraction-api'),
    path('website-info-extractor/request-format/', views.request_format_api_view, name='info-extraction-request-format-api')
]
