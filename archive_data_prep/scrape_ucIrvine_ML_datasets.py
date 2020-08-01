import pandas as pd 
import requests 
from bs4 import BeautifulSoup, Comment
import re
import os
from hurry.filesize import size

def getparentlist(savehere=None):
    parent_url = r"http://archive.ics.uci.edu/ml/datasets.php"
    page = requests.get(parent_url).text
    soup = BeautifulSoup(page, "lxml")
    tbl = soup.find('table' , attrs={'border':'1'})
    rows = tbl.findAll('tr')
    colnames = []
    rowdata = []
    for i,r in enumerate(rows):
        cols = r.findAll('td')
        currow = {}
        if i > 0:
            comment = soup.find(text=lambda text:isinstance(text, Comment))
            print(comment)
            quit()
        for ci, c in enumerate(cols):
            if i == 0:
                colnames.append(c.text)
            else:
                currow[str(ci)] = c.text
            if ci == 0:
                currow['URL'] = c.find('a')['href']
        rowdata.append(currow)
    print(colnames)
    df = pd.DataFrame(rowdata)
    if savehere:
        df.to_csv(savehere)
    return df

def getchildpages(src_df, savehere):

    urllist = list(set(src_df['URL'].to_list()))

    getpagedata = []
    for ul, real_url in enumerate(urllist):
        print(real_url)
        try:
            thispage = {'URL': real_url, 'ID': ul}
            page = requests.get(real_url).text
            soup = BeautifulSoup(page, "lxml").find('table' , attrs={'cellpadding':'2'}).find('td')
            thispage['header'] = soup.find('span', class_='heading').text
            datafsd = [x for x in soup.findAll("span",class_="normal") if 'Data Folder' in x.text][0]
            thispage['DataFolder'] = datafsd.find("a")['href']

            attrtbl = soup.find('table' , attrs={'cellpadding':'6'}).findAll("td")
            attrtbl = iter([x.text for x in attrtbl])
            attrtbl = {re.sub(r'(\xa0|:| |\?)', '',x, re.UNICODE): next(attrtbl) for x in attrtbl}
            thispage.update(attrtbl)
            
            for d in soup("table"):
                d.decompose()
            paragraphs = soup.findAll("p")
            paragraphs = iter([x.text for x in paragraphs])
            paragraphs = {re.sub(r'(\xa0|:| |\?)', '',x, re.UNICODE): next(paragraphs) for x in paragraphs}
            thispage.update(paragraphs)
            getpagedata.append(thispage)
            print("success")
        except:
            print("no luck")

    df2 = pd.DataFrame(getpagedata).set_index('ID')
    df2.to_csv(savehere)

def grab_data_file_URL(df):
    rootURL = r"http://archive.ics.uci.edu/ml"

    def get_dataset_url(x):
        x = x.replace("..", rootURL)
        #print(x)
        soup = BeautifulSoup(requests.get(x).text, "lxml")
        tag = soup.find_all("a")
        urls = [t['href'] for t in tag if "Parent" not in t.text]
        output = []
        for u in urls:
            try:
                head = requests.head(x+u).headers
                addme = [u, size(int(head['Content-Length']))]
                print(addme)
                output.append(addme)
            except: 
                print("                                       no good")
        return output

    df['data_ext_url'] = df['DataFolder'].apply(get_dataset_url)
    return df

if __name__ == '__main__':   
    thisfilesdir = os.path.dirname(os.path.realpath(__file__)) + "\\"
    save_data = r"UC_Irvine_ML_datasets.csv"
    #parent_list_df = getparentlist()
    #child_page_df = getchildpages(parent_list_df, save_data)
    df = pd.read_csv(thisfilesdir + save_data)
    df = grab_data_file_URL(df)
    df.to_csv("getdatasetURLs.csv")
