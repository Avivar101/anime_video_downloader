from bs4 import BeautifulSoup as bs
from lxml import html
from pprint import pprint
import sys
from pySmartDL import SmartDL
import requests
from os import path
import json

login_url = 'https://www2.gogoanime.ee/login.html'
anime_url = 'https://www2.gogoanime.ee/isekai-meikyuu-de-harem-wo-uncensored-episode-12'
download_link = 'https://gogodownload.net/download.php?url=aHR0cHM6LyAdrefsdsdfwerFrefdsfrersfdsrfer363435349URASDGHUSRFSJGYfdsffsderFStewthsfSFtrftesdfjZG4xOS5hbmljYWNoZS5uZXQvdXNlcjEzNDIvZTk2MzM0ZTZhODJkYmNmYmViNDBjNWE1NmFhNDcyN2MvRVAuMS52MS4xNjM5NDk4NTYxLjM2MHAubXA0P3Rva2VuPTg4VkFiTVJFb2dTWncxQzFfV0Z4a1EmZXhwaXJlcz0xNjY0MDE0ODg3JmlkPTM4NDA0JnRpdGxlPSg2NDB4MzYwLWdvZ29hbmltZSlzY2hvb2wtZGF5cy0tZXBpc29kZS0xLm1wNA=='
file_path = 'C:\\Users\\benja\\Videos\\anime'
output_name = "Last Dungeon Boonies"
ep_path = path.normpath(file_path + "/" + output_name + '.mp4')
rootUrl = "https://www2.gogoanime.ee/"
animeName = input("input anime name").lower().replace(' ', '-')
quality = {1: "640x360", 2: "854x480", 3: "1280x720", 4: "1920x1080"}

email = 'mgb40536@nezid.com'
password = 'kevinkevin'


# download anime
def downloadLink(link, filepath):
    obj = SmartDL(link, filepath)
    obj.start()


# get download links
def getLinks(url, qualitySelected):
    links_dict = {}
    r = s.get(url)
    soup = bs(r.text, 'html.parser')

    links = soup.find_all("div", class_="cf-download")
    selected_quality = selectQuality(qualitySelected)

    for link in links:
        for a in link.find_all('a', href=True):
            if selected_quality == a.text.strip():
                urls = (a['href'])
                links_dict[a.text] = urls
            else: print("not-found", selected_quality, "and", a.text.replace(" ", ""), "false")
    pprint(links_dict)
    return links_dict


def selectQuality(qualitySelected):
    for x, y in quality.items():
        if qualitySelected == x:
            print(y)
            return y


# get the episode urls of the anime
def getAnimeUrls(start, end):
    animeUrl = []
    for i in range(start, end + 1):
        urlList = rootUrl + animeName + '-episode-' + str(i)
        animeUrl.append(urlList)
    return animeUrl


# function to download the animes
def downloadAnime(startEp, endEp, qualitySelected):
    urls = getAnimeUrls(startEp, endEp)
    for epUrl in urls:
        downloadLinks = getLinks(epUrl, qualitySelected)
        if len(downloadLinks) == 0:
            print(f"EP {epUrl} NOT FOUND ")
            continue
        pprint(downloadLinks)


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

downloadAnime(1, 4, 2)
s.close()
