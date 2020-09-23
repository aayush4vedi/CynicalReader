from collections import OrderedDict
import requests
from xml.etree import ElementTree
import sys
import csv
import json
import string
import time

from readability import Document
from bs4 import BeautifulSoup

import nltk

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def run():
    print("hello!")

def contentfromhtml(html):
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    return text


def weightedcontentfromhtml(html):
    soup = BeautifulSoup(html)
    whitelist = [
        'h1',
        'h2',
        'h3',
        'h4',
        'strong',
        'title',
        'u',
        'a',
        # other elements,
        ]
    weightedcontent = ' '.join(t for t in soup.find_all(text=True) if t.parent.name in whitelist) 
    # imgaltcontent = ' '.join(img.get('alt') for img in soup.find_all('img') if soup.find_all('img') ) # FIXME: not working: TypeError: sequence item 0: expected str instance, NoneType found
    # return weightedcontent + imgaltcontent
    return weightedcontent

def clean_text(text):
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    stemmed = [wordnet.lemmatize(word) for word in words]
    return ' '.join(stemmed)


if __name__ == '__main__':
    wordnet = WordNetLemmatizer()
    upvotes_threshold = 74      #TODO: change this
    # startepoch = 1594853155            # 15Jul2020-00:00GMT   
    # startepoch = 1595457955            # 22Jul2020-00:00GMT   
    # startepoch = 1596062555            # 29Jul2020-00:00GMT   
    # startepoch = 1596667355            # 5Aug2020-00:00GMT   


    # endepoch  =  1581724800            # 15Feb2020-00:00GMT
    # endepoch  =  1583020800            # 1Mar2020-00:00GMT
    # endepoch  =  1584230400            # 15Mar2020-00:00GMT
    # endepoch  =  1585699200            # 1Apr2020-00:00GMT
    # endepoch  =  1586908800            # 15Apr2020-00:00GMT
    # endepoch  =  1588291200            # 1May2020-00:00GMT
    # endepoch  =  1589500800            # 15May2020-00:00GMT
    # endepoch  =  1590969600            # 1Jun2020-00:00GMT
    # endepoch  =  1592179200            # 15Jun2020-00:00GMT
    # endepoch  =  1594771200            # 1Jul2020-00:00GMT
    # endepoch  =  1596240000            # 15Jul2020-00:00GMT
    # endepoch  =  1597449600            # 15Aug2020-00:00GMT
    timestamps_arr = [
        '1581724800',
        '1583020800',
        '1584230400',
        '1585699200',
        '1586908800',
        '1588291200',
        '1589500800',
        '1590969600',
        '1592179200',
        '1594771200',
        '1596240000',
        '1597449600',
    ]
    index_cnt = 1
    for i in range(len(timestamps_arr)-1):
        startepoch=timestamps_arr[i]
        endepoch=timestamps_arr[i+1]

        url = 'http://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=9999&numericFilters=created_at_i>'+str(startepoch)+',created_at_i<'+ str(endepoch) + ',points>' + str(upvotes_threshold)
        print(url)
        # url = 'http://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=9999&numericFilters=created_at_i>1594853155,created_at_i<1595457955,points>75'
        data = requests.get(url, timeout=None)
        res_size = json.loads(data.content)["nbHits"]
        print("====> Item count: {}\n".format(res_size))
        items_arr = json.loads(data.content)["hits"]
        csv_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/hn15Feb_15Aug/hn'+str(i)+'_' + str(startepoch)+'->'+ str(endepoch) + '.csv'

        f = csv.writer(open(csv_file, "w"))          
        f.writerow(['ID', 'Source', 'TimeGST','TimeEpoch' ,'Upvotes', 'NumComments', 'Title', 'Url'])

        for item in items_arr:
            # print(json.dumps(item, indent = 4))
            if(item["url"] is None):
                print("xxxxx Skipping Row as non-story item xxxx\n")
            else:
                f.writerow([index_cnt,
                        "HackerNews",
                        item["created_at"],
                        item["created_at_i"],
                        item["points"],
                        item["num_comments"],
                        item["title"],              
                        item["url"]])
                index_cnt=index_cnt+1

        print("\n***** Done for i={}- scraping w/o content*******\n".format(i))

        # t = time.localtime()
        # current_time = time.strftime("%H:%M:%S", t)
        # print(">>>>>>>>>>>>>>> [yet_to_do= {} ]:: Sleeping now @ {} ....will wake up after an hour or so\n\n".format(len(timestamps_arr)-1,current_time))
        # time.sleep(2000)                                    # As algolia restricts 10k hits per hour
    print("\n********************** Scraping is done! *************************\n")
            
































        