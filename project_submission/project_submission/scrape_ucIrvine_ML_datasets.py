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
    df = pd.DataFrame(rowdata)
    if savehere:
        df.to_csv(savehere)
    return df

def get_dataset_url(x):
    """sub-function to grab the URL and file size of datasets available"""
    rootURL = r"http://archive.ics.uci.edu/ml/machine-learning-databases"
    x = x.replace("..", rootURL) # clean presented value and replace w root
    # scrape the dataset page
    soup = BeautifulSoup(requests.get(x).text, "lxml") 
    tag = soup.find_all("a")
    # find the URLs given in the page
    urls = [t['href'] for t in tag if "Parent" not in t.text]
    output = []
    for u in urls:
        try:
            # try to request the size of each file available using HTTP
            head = requests.head(x+u).headers
            addme = [u, size(int(head['Content-Length'])), head['Content-Length']]
            print(addme)
            output.append(addme)
        except: 
            print("                                       no good")
    if not output:
        return "|"
    # delimit outputs for easy breakdown later
    output = "|".join([",".join(o) for o in output])
    return output

def getchildpages(src_df, savehere=None):
    """scrape each dataset page for relevant information"""
    
    # create list of URLs to scrape
    urllist = list(set(src_df['URL'].to_list()))

    # container for gathering info for all pages
    getpagedata = []
    for ul, real_url in enumerate(urllist):
        burl = real_url
        real_url = r"http://archive.ics.uci.edu/ml/" + real_url
        try: 
            # if it's a valid URL, scrape it
            thispage = {'URL': real_url, 'ID': ul}
            page = requests.get(real_url).text
            soup = BeautifulSoup(page, "lxml").find('table' , attrs={'cellpadding':'2'}).find('td')
        except:
            # if the URL can't be reached, say so and move on to next loop
            print("                            no luck")
            continue

        # try to get header span to extract
        head = soup.find('span', class_='heading')
        if head:
            thispage['header'] = head.text
        # find all spans to scrape in a loop
        datafsd = [x for x in soup.findAll("span",class_="normal") if 'Data Folder' in x.text]

        if datafsd:
            # grab hyperlinks and shorten the outputs
            datafsd = datafsd[0]
            datafsd = datafsd.find("a")['href']
            thispage['data_folder'] = datafsd.replace("../machine-learning-databases", "")
            datafsd_clear = datafsd.replace(r'../machine-learning-databases/', "").replace("/", "")
            # see if we can shorten the text for a usable name
            # first remove extraneous characters
            # then convert plus signs to dashes
            # then create shortened version removing lowercase letters after 15 char
            possibletextchar = re.sub(r"(datasets\/|[+,\.]|\%\d+)","",burl)
            possibletextchar = re.sub(r"[\+]","-",possibletextchar)
            possibletextchar2 = possibletextchar[:15] + re.sub("[a-z]", "", possibletextchar[15:])
            # if the long version is under 25 char, use it, otherwise shortened
            possibletextchar = possibletextchar2 if len(possibletextchar) >25 else possibletextchar

            # if a short text value is used for the 
            # dataset URL, just use that as ID, otherwise version above
            if datafsd_clear[1:-1].isnumeric() or len(datafsd_clear)>25:
                thispage['Dataset_ID'] = possibletextchar
            else:
                thispage['Dataset_ID'] = datafsd_clear
            print(thispage['Dataset_ID'])
            thispage['data_ext_url'] = get_dataset_url(datafsd)

        # scrape the attribute table
        attrtbl = soup.find('table' , attrs={'cellpadding':'6'})
        if attrtbl:
            # find all cells and make iterable
            attrtbl = attrtbl.findAll("td")
            attrtbl = iter([x.text for x in attrtbl])
            # since they are sequential, clean data and create list of dicts
            attrtbl = {re.sub(r'(\xa0|:| |\?)', '',x, re.UNICODE): next(attrtbl) for x in attrtbl}
            # add directly to this page's dict
            thispage.update(attrtbl)
        
        try:
            # remove d items, they were making trouble
            for d in soup("table"):
                d.decompose()
            # grab all p items, and do like for "td" cells above
            paragraphs = soup.findAll("p") 
            paragraphs = iter([x.text for x in paragraphs])
            paragraphs = {re.sub(r'(\xa0|:| |\?)', '',x, re.UNICODE): next(paragraphs) for x in paragraphs}
            thispage.update(paragraphs)
        except:
            pass
        # add this page's data to the accumulating list
        getpagedata.append(thispage)
            
    # convert list of dicts to data frame and save to CSV if specified
    df2 = pd.DataFrame(getpagedata)
    if not savehere:
        return df2
    else:
        df2.to_csv(savehere)

if __name__ == '__main__':   
    start_time = datetime.now()
    save_data = r"UC_Irvine_ML_datasets.csv"

    parent_list_df = getparentlist()
    child_page_df = getchildpages(parent_list_df, savehere=save_data)
    
    print("--- %s seconds ---" % (datetime.now() - start_time))