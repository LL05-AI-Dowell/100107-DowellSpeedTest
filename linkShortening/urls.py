from django.urls import path
from .views import *

urlpatterns = [
    path('server-status/', serverStatus.as_view(), name="server_status"),

    path('qr-code/', codeqr.as_view(), name="create_link"),
    path('update-qr-code/<str:id>', codeqrupdate.as_view(), name="update_link"),

    path('get-links/', getLinks, name="get_links"),
    path('<str:word>/<str:word2>/<str:word3>', Links.as_view(), name="master_link"),
]