from bs4 import BeautifulSoup as bs
from lxml import html
import requests
from os import path
from idm import IDMan

downloader = IDMan()

# URLs
rootUrl = "https://www2.gogoanime.ee/"
login_url = 'https://www2.gogoanime.ee/login.html'

# input variables
# file_path = 'C:\\Users\\benja\\Videos\\anime'
animeName = input("input anime name: ").lower().replace(' ', '-')
file_path = input('input download filepath: ')
firstEpd = int(input("input first episode to download: "))
lastEpd = int(input("input last episode to download: "))
print("Select your preferred  Quality")
print("1 for 360p, 2 for 480p, 3 for 720p, 4 for 1080p")
pickQuality = int(input("select quality: "))

quality = {1: "640x360", 2: "854x480", 3: "1280x720", 4: "1920x1080"}

email = 'mgb40536@nezid.com'
password = 'kevinkevin'


# download anime
def downloadLink(link, filepath, filename):
    downloader.download(link, filepath, output=filename, lflag=2)


# get download links
def getLinks(url, qualitySelected):
    # dictionary of anime quality their links
    links_dict = {}
    # get link html
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
def getAnimeUrls(start, end):
    animeUrl = {}
    for i in range(start, end + 1):
        url_list = rootUrl + animeName + '-episode-' + str(i)
        file_name = animeName + '-episode-' + str(i)
        ep_path = path.normpath(file_path + "/" + animeName)
        ep_path_and_name = ( ep_path, file_name)
        animeUrl[url_list] = ep_path_and_name
        # print(type(ep_path_and_name))
    return animeUrl


# function to download the animes
def downloadAnime(startEp, endEp, qualitySelected):
    # get selected episodes anime urls
    urls = getAnimeUrls(startEp, endEp)
    # loop through all urls and path
    for epUrl, ePathAndName in urls.items():
        downloadLinks = getLinks(epUrl, qualitySelected)
        ePath= ePathAndName[0]
        name= ePathAndName[1]
        if len(downloadLinks) == 0:
            print(f"EP {epUrl} NOT FOUND ")
            continue
        # download anime
        for link in downloadLinks.values():
            # print(f'{ePathAndName}, {link}')
            # print(name, ePath)
            print(f'about to download {name}')
            downloadLink(link, ePath, name)
            print("downloaded")


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

downloadAnime(firstEpd, lastEpd, pickQuality)

s.close()
