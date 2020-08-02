import pandas as pd 
import requests 
from bs4 import BeautifulSoup, Comment
import re
import os
from hurry.filesize import size
from datetime import datetime

def getparentlist(savehere=None):
    """Scrape the base website with links to all the datasets for further scraping."""

    parent_url = r"http://archive.ics.uci.edu/ml/datasets.php"
    page = requests.get(parent_url).text
    soup = BeautifulSoup(page, "lxml")
    tbl = soup.find('table' , attrs={'border':'1'}) #grab table needed
    rows = tbl.findAll('tr') #find all rows
    colnames = []
    rowdata = []
    for i,r in enumerate(rows):
        cols = r.findAll('td') #for each column
        currow = {}
        # if i > 0:
        #     comment = soup.find(text=lambda text:isinstance(text, Comment))
        for ci, c in enumerate(cols):
            if i == 0: #if it's the first row, get the column names
                colnames.append(c.text)
            else: #otherwise grab values in the cell, remove whitespace
                currow[str(ci)] = c.text.replace(u'\xa0', u' ')
            if ci == 0: #the first column is the URL, we need that labeled
                currow['URL'] = c.find('a')['href']
        if len(currow.keys())>4: #if there's at least 4 columns of data, add to the pile
            rowdata.append(currow)
    #print(colnames)
    df = pd.DataFrame(rowdata)
    if savehere:
        df.to_csv(savehere)
    return df

def get_dataset_url(x):
    """ """
    rootURL = r"http://archive.ics.uci.edu/ml"
    x = x.replace("..", rootURL)
    #print(x)
    soup = BeautifulSoup(requests.get(x).text, "lxml")
    tag = soup.find_all("a")
    urls = [t['href'] for t in tag if "Parent" not in t.text]
    output = []
    for u in urls:
        try:
            head = requests.head(x+u).headers
            addme = [u, size(int(head['Content-Length'])), head['Content-Length']]
            print(addme)
            output.append(addme)
        except: 
            print("                                       no good")
    if not output:
        return "|"
    output = "|".join([",".join(o) for o in output])
    #print(output)
    return output

def getchildpages(src_df, savehere=None):
    """ """
    
    urllist = list(set(src_df['URL'].to_list()))

    getpagedata = []
    for ul, real_url in enumerate(urllist):
        burl = real_url
        real_url = r"http://archive.ics.uci.edu/ml/" + real_url
        try: 
            thispage = {'URL': real_url, 'ID': ul}
            page = requests.get(real_url).text
            soup = BeautifulSoup(page, "lxml").find('table' , attrs={'cellpadding':'2'}).find('td')
        except:
            print("                            no luck")
            continue
        head = soup.find('span', class_='heading')
        if head:
            thispage['header'] = head.text
        datafsd = [x for x in soup.findAll("span",class_="normal") if 'Data Folder' in x.text]
        if datafsd:
            datafsd = datafsd[0]
            datafsd = datafsd.find("a")['href']
            thispage['data_folder'] = datafsd
            datafsd_clear = datafsd.replace(r'../machine-learning-databases/', "").replace("/", "")
            possibletextchar = re.sub(r"(datasets\/|[+,\.]|\%\d+)","",burl)
            possibletextchar = re.sub(r"[\+]","-",possibletextchar)
            possibletextchar2 = possibletextchar[:15] + re.sub("[a-z]", "", possibletextchar[15:])
            possibletextchar = possibletextchar2 if len(possibletextchar) >25 else possibletextchar
            if datafsd_clear[1:-1].isnumeric() or len(datafsd_clear)>25:
                thispage['shortname'] = possibletextchar
            else:
                thispage['shortname'] = datafsd_clear
            print(thispage['shortname'])
            thispage['data_ext_url'] = get_dataset_url(datafsd)
        attrtbl = soup.find('table' , attrs={'cellpadding':'6'})
        if attrtbl:
            attrtbl = attrtbl.findAll("td")
            attrtbl = iter([x.text for x in attrtbl])
            attrtbl = {re.sub(r'(\xa0|:| |\?)', '',x, re.UNICODE): next(attrtbl) for x in attrtbl}
            thispage.update(attrtbl)
        
        try:
            for d in soup("table"):
                d.decompose()
            paragraphs = soup.findAll("p")
            paragraphs = iter([x.text for x in paragraphs])
            paragraphs = {re.sub(r'(\xa0|:| |\?)', '',x, re.UNICODE): next(paragraphs) for x in paragraphs}
            thispage.update(paragraphs)
        except:
            pass
        getpagedata.append(thispage)
        #print("success")
            

    df2 = pd.DataFrame(getpagedata) #.set_index('ID')
    if not savehere:
        return df2
    else:
        df2.to_csv(savehere)

if __name__ == '__main__':   
    start_time = datetime.now()
    save_data = r"UC_Irvine_ML_datasets.csv"
    parent_list_df = getparentlist()
    # print(parent_list_df)

    child_page_df = getchildpages(parent_list_df, savehere=save_data)

    # pd.set_option("display.max_rows", None, "display.max_columns", None)
    # childpageurl = "http://archive.ics.uci.edu/ml/datasets/Wine+Quality"
    # df = pd.DataFrame([[childpageurl]], columns=['URL'])
    # scrape_child = getchildpages(df)
    # scrape_child = scrape_child.to_dict()
    # print(len(scrape_child.keys()))
    # print(scrape_child)
    
    print("--- %s seconds ---" % (datetime.now() - start_time))