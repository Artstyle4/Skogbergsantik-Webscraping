import requests
from bs4 import BeautifulSoup
import re

def parse_site(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_imageUrl():
    gallery = []
    url = "http://www.skogbergsantik.com"
    soup = parse_site(url)
    for x in soup.find_all('a'):
        #print (x.get('href'))
        if "gallery_" in str(x):
            gallery.append(x['href'])
        
    gallery = list(dict.fromkeys(gallery))
    
    print(gallery)
    
  

get_imageUrl()
