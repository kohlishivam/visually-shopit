from django.shortcuts import render
import base64
import sys
from django.http import HttpResponse
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import service_account
from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup as BS
import os


## handle the image uploads
@csrf_exempt
def handleUpload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        image = request.FILES.get('file')
        image_read = image.read()
        project_id = "essential-haiku-218118"
        model_id = "ICN747416880257459356"
        response = get_prediction(image_read, project_id,  model_id)
        keywords_arr = []
        for result in response.payload:
            keywords_arr.append(result.display_name)
        print(keywords_arr)
        keywords = ""
        for i in keywords_arr:
            keywords = keywords+"-"+i
        keywords = str(keywords)
        return HttpResponse(scrapper(keywords))
 

# direct google function to get the prediction
def get_prediction(content, project_id, model_id):
    credentials = service_account.Credentials.from_service_account_file('essential-haiku-218118-d43dfbd3f752.json')
    prediction_client = automl_v1beta1.PredictionServiceClient(credentials=credentials)
    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request


def test(request):
    return render(request,'main/test.html')


# to initialte the driver 
# chrome driver is used for this selenium
def setup_webdriver():
    # prefs = {"profile.default_content_setting_values.notifications" : 2}
    # chrome_options.add_experimental_option("prefs",prefs)
    # path = os.path.dirname(os.path.abspath('chromedriver'))
    # driver = webdriver.Chrome(executable_path="/main/chromedriver", chrome_options=chrome_options)
    # return driver
    # chrome_options = Options()
    chrome_exec_shim = "chromedriver"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_exec_shim
    chrome_options.add_argument('--disable-gpu');
    chrome_options.add_argument('--no-sandbox');
    chrome_options.add_argument('headless');
    # chrome_options.add_argument('--disable-dev-shm-usage');
    driver = webdriver.Chrome(executable_path=chrome_exec_shim, chrome_options=chrome_options)
    return driver


# scrapper for myntra
# the results that are returned is the img url and the buy url
# top 9 results are given
def scrapper(keywords):
    driver=setup_webdriver()
    url = "https://www.myntra.com/" + keywords
    driver.get(url)
    data = driver.page_source
    soup = BS(data,"html.parser")
    divdata = soup.find_all('ul', {"class": "results-base"})
    arr = []
    for i in range(9):
        item = {}
        for img in divdata[0].find_all("img"):
            item['img'] = img["src"]
        for href in divdata[0].find_all("a"):
            item['href'] = "https://www.myntra.com/" + href["href"]
        arr.append(item)
    driver.close()
    return arr
