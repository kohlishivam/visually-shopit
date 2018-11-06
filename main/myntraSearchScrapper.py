from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup as BS

def setup_webdriver():
	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_setting_values.notifications" : 2}
	chrome_options.add_experimental_option("prefs",prefs)
	driver = webdriver.Chrome(executable_path="/Users/sk/Desktop/shopit/chromedriver", chrome_options=chrome_options)
	return driver
	
# driver=setup_webdriver()
url = "https://www.myntra.com/long-red-dress"
# driver.get(url)
# data = driver.page_source
r = requests.get(url) 
data = r.content
# print(data)
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
print(arr)
