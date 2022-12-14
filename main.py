from bs4 import BeautifulSoup as bs
from decouple import config
from lxml import html
import requests
from os import path
from idm import IDMan
import time
import re

downloader = IDMan()

# input first URL
print('Input the link of the first anime episode you wish to download')
animeUrl = input('first episode of url: ')

# URLs
# get the root url
rootUrl = re.search(
    r"[A-Za-z0-9]+://[A-Za-z0-9]+\.[a-zA-Z]+/", animeUrl).group(0)
# the login url
login_url = rootUrl + 'login.html'

# get name of anime from link
animeNameFromLink = re.search(
    r"([A-Za-z0-9]+(-[A-Za-z0-9]+)+)", animeUrl).group(0)
animeName = re.sub(r"-episode-\d+$", "", animeNameFromLink)

# create the download url
downloadUrl = re.sub(r"\d+$", "", animeUrl)

# create download filepath
filePathAnimeName = re.sub(r"-episode-\d+$", "", animeNameFromLink)


# input variables
file_path = input('input download filepath: ')
firstEpd = int(input("input first episode to download: "))
lastEpd = int(input("input last episode to download: "))
print("Select your preferred  Quality")
print("1 for 360p, 2 for 480p, 3 for 720p, 4 for 1080p")
pickQuality = int(input("select quality: "))

quality = {1: "640x360", 2: "854x480", 3: "1280x720", 4: "1920x1080"}

email = config('EMAIL')
password = config('PASSWORD')


# function to download anime
def downloadLink(link, filepath, filename):
    downloader.download(link, filepath, output=filename, lflag=2)


# get download links
def getLinks(url, qualitySelected):
    # dictionary of anime quality their links
    links_dict = {}
    # get html
    r = s.get(url)
    soup = bs(r.text, 'html.parser')
    links = soup.find_all("div", class_="cf-download")

    selected_quality = selectQuality(qualitySelected)

    # get the download links from the html
    for link in links:
        # loops through all quality links
        for a in link.find_all('a', href=True):
            # get selected quality link
            if selected_quality == a.text.strip():
                urls = (a['href'])
                links_dict[a.text] = urls
    return links_dict


# get the selected quality
def selectQuality(qualitySelected):
    for x, y in quality.items():
        if qualitySelected == x:
            return y


# get the episode urls and download path of the anime
def getAnimeUrls(start, end, v_quality):
    animeUrl = {}
    quality_selected = selectQuality(v_quality)
    for i in range(start, end + 1):
        url_list = downloadUrl + str(i)
        # filename has to match the name of the episode sent by the server else idm would prompt for rename
        file_name = f'({quality_selected}-gogoanime)' + \
            animeName + '-episode-' + str(i) + '.mp4'
        ep_path = path.normpath(file_path + "/" + filePathAnimeName)
        ep_path_and_name = (ep_path, file_name)
        animeUrl[url_list] = ep_path_and_name
    return animeUrl


# function to download the animes
def downloadAnime(startEp, endEp, qualitySelected):
    # get selected episodes anime urls
    urls = getAnimeUrls(startEp, endEp, qualitySelected)

    # loops through all urls
    for epUrl, ePathAndName in urls.items():
        downloadLinks = getLinks(epUrl, qualitySelected)
        # path to save the anime on your system
        epPath = ePathAndName[0]
        # name the anime is saved with
        name = ePathAndName[1]

        if len(downloadLinks) == 0:
            print(f"EP {epUrl} NOT FOUND ")
            continue

        # download anime
        for link in downloadLinks.values():
            # delay next download function call
            if epUrl != list(urls.keys())[-1]:
                print(f'about to download {name}')
                downloadLink(link, epPath, name)
                print('not last anime')
                time.sleep(20)
            elif epUrl == list(urls.keys())[-1]:
                print(f'last anime {name}')
                downloadLink(link, epPath, name)
            print("downloading")


def main(firstEpd, lastEpd, pickQuality):
    downloadAnime(firstEpd, lastEpd, pickQuality)

s = requests.Session()
result = s.get(login_url)

tree = html.fromstring(result.text)
# extract hidden token
token = list(set(tree.xpath("//input[@name='_csrf']/@value")))[0]

payload = {
    'email': email,
    'password': password,
    '_csrf': token
}
p = s.post(login_url, data=payload)

main(firstEpd, lastEpd, pickQuality)

s.close()
