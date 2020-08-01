from bs4 import BeautifulSoup
import pandas as pd
import requests 
import os
import re

def getparentURLs():
    parent_url = r"https://en.wikipedia.org/wiki/Country_code"
    page = requests.get(parent_url).text
    soup = BeautifulSoup(page, "lxml")
    a_list = soup.findAll('a')
    codepages = []
    for aitem in a_list:
        if 'href' in aitem.attrs:
            href = aitem['href']
            #print(href)
            if r"/wiki/Country_codes" in href and href not in codepages:
                codepages.append(href)
    #print(codepages)
    return codepages

def scrape_country_codes(pageURL):
    pageURL = r"https://en.wikipedia.org" + pageURL
    page = requests.get(pageURL).text
    soup = BeautifulSoup(page, "lxml")
    headerlist = soup.find("div", class_="mw-parser-output").findAll('h2', recursive=False)
    dictlist = []
    for count in headerlist:
        countryname = count.find("a").text
        countryname = re.sub(r"[—–†]", "",countryname)
        cdict = {"country":countryname}
        if cdict["country"] != 'edit':
            content = count.next_sibling.next_sibling
            content = content.findAll("td")
            for conttype in content:
                srctype = conttype.a.text
                srctype = re.sub(r"[ -.]", r"_",srctype)
                srctype = re.sub(r"[^a-zA-Z0-9_]", "",srctype)
                srctype = re.sub(r"[—–†]", "",srctype)
                textval = conttype.find("b").text
                textval = re.sub(r"[—–†]", "",textval)
                cdict[srctype] = textval
            dictlist.append(cdict)
    #print(dictlist)
    return dictlist

if __name__ == "__main__":
    urllist = getparentURLs()
    dictlist = []
    for url in urllist:
        retdict = scrape_country_codes(url)
        dictlist += retdict
    df = pd.DataFrame(dictlist)
    thisdir = os.path.dirname(os.path.abspath(__file__)) + "\\"
    df.to_csv(thisdir + "CountryCodes.csv", encoding='latin-1')