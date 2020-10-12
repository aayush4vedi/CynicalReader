import requests
import sys
import csv
import json
import string
import time
from readability import Document

import nltk

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from bs4 import BeautifulSoup


def hello():
    print("hello\n")

def contentfromhtml(response):
    """
        get meaningful content from article page.Uses `readability` pkg
    """

    article = Document(response.text)
    html = article.summary()
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    return text


def weightedcontentfromhtml(response):
    """
        get emphasised words from meaningful content from article page
    """
    article = Document(response.text)
    html = article.summary()
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
    """Clean raw text using different methods :
       1. tokenize text
       2. lower text
       3. remove punctuation
       4. remove non-alphabetics char
       5. remove stopwords
       6. lemmatize
    """
    
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

    # csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/hn_sample.csv'
    # csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/hn_sample_with_content.csv'
    # csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/hn_1581724800->1584230400.csv'
    # csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/hn_1581724800->1584230400_with_content.csv'
    
    for i in range(len(timestamps_arr)-1):
        startepoch=timestamps_arr[i]
        endepoch=timestamps_arr[i+1]
        csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/hn15Feb_15Aug/hn'+str(i)+'_' + str(startepoch)+'->'+ str(endepoch) + '.csv'
        csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/hn15Feb_15Aug/with_content/hn'+str(i)+'_' + str(startepoch)+'->'+ str(endepoch) + 'wc.csv'

        f = csv.writer(open(csv_dest_file, "w"))          # Flush the old file
        f.writerow(['ID', 'Source', 'TimeGST','TimeEpoch' ,'Upvotes', 'NumComments', 'Title', 'Url','ProcessdedTitle', 'WeightedContent','Content'])

        with open(csv_src_file, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Headers are {", ".join(row)}')
                    line_count += 1
                url = row["Url"]
                print("sleeping for 0.1 second ZZZZZZZZZZzzzzzzzzzzzzzzzzz.........................................\n")
                time.sleep(0.1) 
                try:
                    response = requests.get(url,verify=False,timeout=30)
                    if response.status_code == 200:
                        article = Document(response.text)
                        title = article.title()
                        rawcontent = article.summary()
                        content = contentfromhtml(response)  
                        weightedcontent = weightedcontentfromhtml(response)  
                        line_count += 1

                        f = csv.writer(open(csv_dest_file, "a"))          
                        f.writerow([
                                row["ID"],
                                row["Source"],
                                row["TimeGST"],
                                row["TimeEpoch"],
                                row["Upvotes"],
                                row["NumComments"],
                                row["Title"],
                                row["Url"],
                                clean_text(row["Title"]),
                                clean_text(weightedcontent),
                                clean_text(content)])
                        print("============== [ID]: {} \n".format(row["ID"]))
                        print("\t=====> Title: {}\n".format(title))
                    else:
                        print("\txxxxx Found Error code: {} , SKIPPING...\n".format(response.status_code))
                except Exception as e:
                    print(" === XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ======\n >> [ID]= {} Skipping...Failed due to: {} \n".format(row["ID"], e))
                    pass
    print("\n\n********************** All the Scraping is Complete ***********************\n\n")
    