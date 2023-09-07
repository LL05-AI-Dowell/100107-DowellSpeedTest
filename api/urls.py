from django.urls import path

from . import views

urlpatterns = [
    path('website-info-extractor/', views.website_info_extraction_api_view, name='info-extraction-api'),
]
