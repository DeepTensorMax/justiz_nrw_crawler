#!/usr/bin/python3

import os
import requests
from bs4 import BeautifulSoup

url = "https://www.justiz.nrw/BS/nrwe2/index.php"

def buildRequest(page, pageSize):
    stringPage = "page" + str(page)

    request = {
            stringPage : str(page),
            "gerichtstyp": "",
            "gerichtsbarkeit": "",
            "gerichtsort": "",
            "entscheidungsart": "",
            "date": "",
            "von": "",
            "bis": "",
            "validFrom": "",
            "von2": "",
            "bis2": "",
            "aktenzeichen": "",
            "schlagwoerter": "",
            "q": "*",
            "method": "stem",
            "qSize": str(pageSize),
            "sortieren_nach": "relevanz",
            "advanced_search": "true"
            }

    return request

def extractLinks(content):
    soup = BeautifulSoup(content)
    linksHtml = soup.find("div", {"class": "alleErgebnisse"}).find_all("a", href=True)

    links = []
    for link in linksHtml:
        links.append(link["href"])

    return links

def writeToFile(links):
    with open("data/links.txt", "a") as f:
        for link in links:
            f.write(link + "\n")



pageSize = 1000
linkCount = 191246
pageCount = linkCount // pageSize + 1

print("Fetching " + str(pageCount) + " pages!")

for page in range(1, pageCount + 1):
    req = buildRequest(page, pageSize)
    htmlPage = requests.post(url, req)
    links = extractLinks(htmlPage.text)
    writeToFile(links)
    print("Saved page " + str(page) + " from " + str(pageCount))

