from collections import OrderedDict
import requests
from xml.etree import ElementTree
import sys
import csv
import json
import string
import time

import nltk

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


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
    upvotes_threshold = 74
    # startepoch = 1594853155            # 15Jul2020-00:00GMT   
    # startepoch = 1595457955            # 22Jul2020-00:00GMT   
    # startepoch = 1596062555            # 29Jul2020-00:00GMT   
    # startepoch = 1596667355            # 5Aug2020-00:00GMT   
    # endepoch  =  1597449600            # 15Aug2020-00:00GMT
    timestamps_arr = [
        '1594853155',
        '1595457955',
        '1596062555',
        '1596667355',
        '1597449600',
    ]
    index_cnt = 1
    for i in range(len(timestamps_arr)-1):
        startepoch=timestamps_arr[i]
        endepoch=timestamps_arr[i+1]

        url = 'http://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=9999&numericFilters=created_at_i>'+str(startepoch)+',created_at_i<'+ str(endepoch) + ',points>' + str(upvotes_threshold)
        # url = 'http://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=9999&numericFilters=created_at_i>1594853155,created_at_i<1595457955,points>75'
        data = requests.get(url, timeout=None)
        res_size = json.loads(data.content)["nbHits"]
        print(res_size)
        items_arr = json.loads(data.content)["hits"]
        csv_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/hn_' + str(startepoch)+'->'+ str(endepoch) + '.csv'

        f = csv.writer(open(csv_file, "w"))          
        f.writerow(['ID', 'Source', 'TimeGST','TimeEpoch' ,'Upvotes', 'NumComments', 'Title', 'Url'])

        for item in items_arr:
            print(json.dumps(item, indent = 4))
            if(item["url"] is None):
                print("xxxxx Skipping Row as non-story item xxxx\n")
            else:
                f.writerow([index_cnt,
                        "HackerNews",
                        item["created_at"],
                        item["created_at_i"],
                        item["points"],
                        item["num_comments"],
                        clean_text(item["title"]),
                        item["url"]])
                index_cnt=index_cnt+1
        print("\n********************\n")
        # print(">>>>>>>>>>>>>>> Sleeping now....will wake up after an hour or so\n\n")
        # time.sleep(4000)                                # As algolia restricts 10k hits per hour
    print("\n********************** Scraping is done! *************************\n")
            
































        