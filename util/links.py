import requests
from bs4 import BeautifulSoup

def extractLinks(url):
    newLinks = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    mylinks = soup.findAll("a", { "class" : "ga_w2gi_lp" })
    for i in range(len(mylinks)):
        link = mylinks[i]
        if(len(link['href'])<=len(url) or link['href'] in newLinks):
            continue
        newLinks.append(link['href'])
        if(i>2):
            break

    return newLinks

def extractStoreInfo(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    storeNum = url.split('/')[-2]
    city = url.split('/')[-3]
    state = url.split('/')[-4]
    name = soup.find("title").text.strip()
    phoneNumber = soup.findAll("div", { "class" : "phone desktopPhone" })[-1].text
    address = soup.find("span", { "itemprop" : "address" }).text.strip()
    latitude = soup.find("meta", { "property" : "place:location:latitude" })['content']
    longitude = soup.find("meta", { "property" : "place:location:longitude" })['content']
    
    return [name, storeNum, phoneNumber, address, url, longitude, latitude, city, state]