#!/usr/bin/python3
import sys

import requests
from bs4 import BeautifulSoup

baseUrl = "https://www.justiz.nrw"

f = open("data/links.txt", "r")
fContent = f.readlines()
f.close()

def extactMain(content):
    soup = BeautifulSoup(content)
    
    paragraphs = soup.find_all("p", {"class": "absatzLinks"})

    text = ""
    for paragraph in paragraphs:
        par = paragraph.get_text()
        
        text += par + "\n"

    return text

lineStart = sys.argv[1]
lineEnd = sys.argv[2]

for lineNr in range(lineStart, lineEnd):
    link = fContent[lineNr].rstrip("\n")
    url = baseUrl + link

    content = requests.get(url).text

    text = extactMain(content)

    fName = "data/urteile/" + link.replace("/", "_")

    with open(fName, "w") as outfile:
        outfile.write(text)

    print("Saved file " + str(lineNr) + " of " + str(lineEnd - lineStart))

fc = open("data/complete.txt", "a")
fc.write(str(lineStart) + "\t" + str(lineEnd) + "\n")
fc.close()
