import requests
from bs4 import BeautifulSoup
import time
from util.config import retryBackoff, reqSleep

def extractLinks(url):
    time.sleep(reqSleep)
    newLinks = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=headers)
        except:
            return []
    soup = BeautifulSoup(page.text, 'lxml')
    mylinks = soup.findAll("a", { "class" : "ga_w2gi_lp" })
    for i in range(len(mylinks)):
        link = mylinks[i]
        if(len(link['href'])<=len(url) or link['href'] in newLinks):
            continue
        newLinks.append(link['href'])

    return newLinks

def extractStoreInfo(url):
    time.sleep(reqSleep)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=headers)
        except:
            return ['Error', 'Error', 'Error', 'Error', 'Error', 'Error', 'Error', 'Error', 'Error']
    soup = BeautifulSoup(page.text, 'lxml')
    storeNum = url.split('/')[-2]
    city = url.split('/')[-3]
    state = url.split('/')[-4]
    name = soup.find("title").text.strip()
    try:
        phoneNumber = soup.findAll("div", { "class" : "phone desktopPhone" })[-1].text
    except:
        phoneNumber = ""

    try:
        address = soup.find("span", { "itemprop" : "address" }).text.strip()
    except:
        address = ""

    try:
        latitude = soup.find("meta", { "property" : "place:location:latitude" })['content']
    except:
        latitude = ""

    try:
        longitude = soup.find("meta", { "property" : "place:location:longitude" })['content']
    except:
        longitude = ""
    
    return [name, storeNum, phoneNumber, address, url, longitude, latitude, city, state]