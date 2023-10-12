from rest_framework import generics, status, decorators
from rest_framework.response import Response
from .serializers import ContactInfoRequestSerializer, WebsiteInfoRequestSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from utils.scraper import WebsiteInfoScraper
from utils.requests import WebsiteInfoRequest
from utils.misc import INFO_REQUEST_FORMAT
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json


class WebsiteInfoExtractionAPIView(generics.GenericAPIView):
    """
    API view for website info extraction.
    """
    serializer_class = WebsiteInfoRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            api_key = validated_data.pop('api_key', None)
            web_info_request = WebsiteInfoRequest(body=validated_data)
            response_dict = web_info_request.get_structured_response_dict(api_key)

            if response_dict:
                return Response(response_dict, status=status.HTTP_200_OK)
            return Response(web_info_request.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@decorators.api_view(['GET'])
def request_format_api_view(request, *args, **kwargs):
    """
    API view for getting website info extraction request format.
    """
    if request.method == 'GET':
        return Response(INFO_REQUEST_FORMAT, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


website_info_extraction_api_view = WebsiteInfoExtractionAPIView.as_view()


class ContactUsAPI(generics.GenericAPIView):
    serializer_class = ContactInfoRequestSerializer
    queryset = []
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            contact_us_url = serializer.data.get("contact_us_url")
            # validated_data = serializer.validated_data
            web_info_scraper = WebsiteInfoScraper(web_url=contact_us_url)
            response_dict = web_info_scraper.scrape_contact_us_page(web_url=contact_us_url)

            # print(response_dict)

            # if response_dict:
            return Response(response_dict, status=status.HTTP_200_OK)
            # return Response("Error" , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
contact_us_api_view = ContactUsAPI.as_view()




@csrf_exempt
def submit_contact_form(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            contact_us_link = request_data.get("contact_us_link")
            first_name = request_data.get("first-name")
            last_name = request_data.get("last-name")
            email = request_data.get("email")
            message = request_data.get("textarea_comp-laapwo6d")
            # Initialize Chrome WebDriver in headless mode
            chrome_options = Options()
            # chrome_options.add_argument("--headless")  # Run in headless mode
            chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
            chrome_options.add_experimental_option("useAutomationExtension", False) 
            # if browser.lower() == "chrome":
            # Add similar blocks for other browsers (e.g., Firefox, Edge) if needed
            driver = webdriver.Chrome(options=chrome_options)
            # chrome_options = Options()
            # chrome_options.add_argument("--headless")
            # driver = webdriver.Chrome(options=chrome_options)
            # Open the contact_us_link
            driver.get(contact_us_link)
            # Fill in the form fields
            driver.find_element(By.NAME, "first-name").send_keys(first_name)
            driver.find_element(By.NAME, "last-name").send_keys(last_name)
            driver.find_element(By.NAME, "email").send_keys(email)
            driver.find_element(By.ID , "textarea_comp-laapwo6d").send_keys(message)
            # Submit the form (replace 'submit_button_name' with the actual button name)
            # driver.find_element(By.NAME, "submit_button_name").click()
            driver.find_element(By.CLASS_NAME, "wixui-button").click()
            # Optionally, you can wait for some time for the response page to load
            driver.implicitly_wait(5)
            # Get the response status code
            response_code = driver.execute_script("return document.readyState")
            # Close the WebDriver
            driver.quit()
            return JsonResponse({"status_code": response_code}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)
