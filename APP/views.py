import json
import threading
from django.conf import settings
from django.http import HttpResponse
from rest_framework import generics, status, decorators
from rest_framework.response import Response
from rest_framework.decorators import api_view

from utils.helper import cleanUrl, create_short_uuid, experienceUserDetails, serviceExperienceUSerDetails, updateUsage
from .serializers import PublicContactInfoRequestSerializer, SubmitFileSerializer, SubmitFormSerializer, WebsiteInfoRequestSerializer
from django.views.decorators.csrf import csrf_exempt

from utils.scraper import WebsiteInfoScraper
from utils.requests import WebsiteInfoRequest
from utils.misc import INFO_REQUEST_FORMAT


class ExperiencedUserDb(threading.Thread):
    def __init__(self, email, title, content):
        super(ExperiencedUserDb, self).__init__()
        self.email = email
        self.title = title
        self.content = content
        
    def run(self):
        # Your second threaded function logic goes here
        try:
            res = experienceUserDetails(self.email, self.title, self.content)
            print(res["message"])
        except Exception as e:
            print(f"An error occurred while trying to Insert Experienced User Data In DB.{e}")

class UpdateUserUsage(threading.Thread):
    def __init__(self, occurences, email):
        super(UpdateUserUsage, self).__init__()
        self.occurences = occurences
        self.email = email
        
    def run(self):
        # Your second threaded function logic goes here
        try:
            res = updateUsage(self.occurences, self.email)
            print(res["message"])
        except Exception as e:
            print(f"An error occurred while trying to update user usage.{e}")
        
class WebsiteInfoExtractionAPIView(generics.GenericAPIView):
    """
    API view for website info extraction.
    """
    serializer_class = WebsiteInfoRequestSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        param = request.GET.get("main")

        serializer = self.get_serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            # Hit experienced serviceuser details api
            if param:
                occurences = data["occurrences"]
                email =  data["email"]
                try:
                    r = serviceExperienceUSerDetails(occurences, email)
                    r = r.json()
                except Exception as e:
                    print({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
                
            # if experience returns successcontinur and retrieve website information.
            if r["success"]:
                validated_data = serializer.validated_data
                api_key = validated_data.pop('api_key', None)
                web_info_request = WebsiteInfoRequest(body=validated_data)
                response_dict = web_info_request.get_structured_response_dict(api_key)

                if response_dict:
                    # update Api usage on data website info retrival success
                    if param:
                        update_usage = UpdateUserUsage(occurences, email)
                        experienceUserDb = ExperiencedUserDb(email, title=data["web_url"], content=str(response_dict))
            
                        update_usage.start()
                        experienceUserDb.start()
                    return Response(response_dict, status=status.HTTP_200_OK)
                return Response(web_info_request.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"error": r["message"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@decorators.api_view(['GET'])
def request_format_api_view(request, *args, **kwargs):
    """
    API view for getting website info extraction request format.
    """
    if request.method == 'GET':
        return Response(INFO_REQUEST_FORMAT, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class ContactUsFormExtractorAPI(generics.GenericAPIView):
    serializer_class = PublicContactInfoRequestSerializer
    queryset = []


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            contact_us_urls = serializer.validated_data.get("page_links")

            try:
                response_dict = {}
                for i, contact_us_url in enumerate(contact_us_urls):
                    web_info_scraper = WebsiteInfoScraper(web_url=contact_us_url)
                    response_dict[i] = web_info_scraper.scrape_contact_us_page(web_url=contact_us_url)

                merged_object = {}

                for key, value in response_dict.items():
                    if isinstance(value, list):
                        for sub_dict in value:
                            merged_object.update(sub_dict)
                    else:
                        merged_object.update(value)

                return Response(merged_object, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

@csrf_exempt
@api_view(['POST'])
def submit_contact_form(request):
    try:
        contact_us_links = request.data.get("page_links")
        form_data = request.data.get("form_data")

        # initialize scraper
        serializer = SubmitFormSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            scraper = WebsiteInfoScraper()
            response_data = scraper.submit_contact_form_selenium(contact_us_links, form_data)
            return Response({"success": response_data}, status=200)
        return Response(serializer.errors)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@csrf_exempt
@api_view(['POST'])
def submit_contact_form_excel(request):
    try: 
        contact_us_links = json.loads(request.data.get("page_links"))
        file = request.FILES.get("file")

        print(contact_us_links)

        if not isinstance(contact_us_links, list):
            return Response({"error": "page_links must be a list"}, status=400)

        serializer = SubmitFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # initialize scraper
            scraper = WebsiteInfoScraper()
            # extract form data from excel file
            extracted_data = scraper.extract_excel_data(file)
            # submit form data
            post_form = scraper.submit_contact_form_selenium(contact_us_links, extracted_data)
            return Response({"success": post_form}, status=200)
        return Response(serializer.errors)

    except Exception as e:
        return Response({"error": str(e)}, status=400)



class DowloadExcelForm(generics.GenericAPIView):
    serializer_class = PublicContactInfoRequestSerializer
    queryset = []

    def post(self, request):
        file_type = request.GET.get("file_type")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            contact_us_urls = serializer.validated_data.get("page_links")

        if not contact_us_urls:
            return Response({"error": "page_links is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response_dict = {}
            for i, contact_us_url in enumerate(contact_us_urls):
                web_info_scraper = WebsiteInfoScraper(web_url=contact_us_url)
                response_dict[i] = web_info_scraper.scrape_contact_us_page(web_url=contact_us_url)
            
            merged_object = {}

            for key, value in response_dict.items():
                if isinstance(value, list):
                    for sub_dict in value:
                        merged_object.update(sub_dict)
                else:
                    merged_object.update(value)

            # Initialize your web scraper
            scraper = WebsiteInfoScraper()
            excel_data = scraper.save_form_data_to_excel(merged_object, file_type=file_type)
            file_name = create_short_uuid()
            if excel_data:
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{file_name}.{file_type}"'
                response.write(excel_data)
                return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

