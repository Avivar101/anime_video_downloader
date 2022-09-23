from bs4 import BeautifulSoup as bs
from lxml import html
from pprint import pprint
import sys
from pySmartDL import SmartDL
import requests
from os import path

login_url = 'https://www2.gogoanime.ee/login.html'
anime_url = 'https://www2.gogoanime.ee/isekai-meikyuu-de-harem-wo-uncensored-episode-12'

email = 'mgb40536@nezid.com'
password = 'kevinkevin'


# download anime
def downloadLink(link, filepath):
    obj = SmartDL(link, filepath)
    obj.start()


# get download links
def getLinks(url):
    links_dict = {}
    r = s.get(url)
    soup = bs(r.text, 'html.parser')

    links = soup.find_all("div", class_="cf-download")

    for link in links:
        for a in link.find_all('a', href=True):
            urls = (a['href'])
            links_dict[a.text] = urls
    pprint(links_dict)
    return links_dict


s = requests.Session()
result = s.get(login_url)

tree = html.fromstring(result.text)
token = list(set(tree.xpath("//input[@name='_csrf']/@value")))[0]

payload = {
    'email': email,
    'password': password,
    '_csrf': token
}
p = s.post(login_url, data=payload)

getLinks(anime_url)
s.close()
