from rest_framework import serializers
from django.core.validators import URLValidator

from utils.misc import INFO_REQUEST_FORMAT
from utils.validators import InfoRequestValidator


class WebsiteInfoRequestSerializer(serializers.Serializer):
    """
    Quick serializer implementation for website info requests.

    For quick testing, use the following snippet in the shell:
    ```
    from website_info.api.serializers import WebsiteInfoRequestSerializer
    from website_info.api.info_request import INFO_REQUEST_FORMAT
    serializer = WebsiteInfoRequestSerializer(data={"web_url": "https://dribbble.com/", "info_request": INFO_REQUEST_FORMAT})
    serializer.is_valid(raise_exception=True)
    serializer.validated_data
    ```
    """
    web_url = serializers.URLField(validators=[URLValidator], required=True)
    max_search_depth = serializers.IntegerField(min_value=0, max_value=2, required=False)
    info_request = serializers.JSONField(write_only=True, required=True, initial=INFO_REQUEST_FORMAT, validators=[InfoRequestValidator().validate])


class PublicContactInfoRequestSerializer(serializers.Serializer):
    # page_links = serializers.ListField(child=serializers.URLField(validators=[URLValidator]), required=True)
    page_link = serializers.URLField()
class SubmitFormSerializer(serializers.Serializer):
    page_link = serializers.URLField()
    form_data = serializers.ListField()

class SubmitFileSerializer(serializers.Serializer):
    page_link = serializers.URLField()
    file = serializers.FileField()