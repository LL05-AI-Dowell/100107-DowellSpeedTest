from django.urls import path
from .views import *

urlpatterns = [
    path('server-status/', serverStatus.as_view()),

    path('qr-code/', codeqr.as_view()),
    path('update-qr-code/<str:id>', codeqrupdate.as_view()),

    path('get-links/', getLinks, name="get_links"),
    path('<str:word>/<str:word2>/<str:word3>', Links.as_view(), name="master_link"),
]