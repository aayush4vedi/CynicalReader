from collections import OrderedDict
import requests
from xml.etree import ElementTree
import sys
import csv
import string

import nltk

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def clean_text(text):
    """Clean raw text using different methods :
       1. tokenize text
       2. lower text
       3. remove punctuation
       4. remove non-alphabetics char
       5. remove stopwords
       6. lemmatize
    
    Arguments:
        text {string} -- raw text
    
    Returns:
        [string] -- clean text
    """

    # split into words
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    stemmed = [wordnet.lemmatize(word) for word in words]

    return ' '.join(stemmed)


def get_entries(xml_root, cat_main):
    entries = []
    i = 1
    for r in xml_root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = r.find('{http://www.w3.org/2005/Atom}title').text
        summary = r.find('{http://www.w3.org/2005/Atom}summary').text.replace('\n', ' ')
        entries.append({'ID': i,
                        'Topic': cat_main,
                        'Title': clean_text(title),
                        'Content': clean_text(summary)})
        i = i+1
        # print(" ------------>> Title: {}\n".format(title))
        # print(" ------------>> Summary: {}\n".format(summary))
    return entries




if __name__ == '__main__':
    wordnet = WordNetLemmatizer()

    """
        POC: Only for 5 categories:
        1. Computer Science(Software Development)
        2. Finance
        3. Statistics
        4. Biology
        5. Mathematics
    """

    CATEGORIES = OrderedDict([
        ("cs*", "ComputerScience"),
        ("q-fin*","Finance"),
        ("stat*", "Statistics"),
        ("q-bio*", "Biology"),
        ("math*", "Mathematics")
    ])

    start = 0
    end = 1000
    for key, val in CATEGORIES.items():
        url = 'http://export.arxiv.org/api/query?search_query=cat:' + \
                  str(key) + '&start=' + str(start) + '&max_results=' + str(end)

        print(" \n \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ Scraping.... for {}  ///////////////////////////////// \n".format(val))
        # url = 'http://export.arxiv.org/api/query?search_query=cat:\cs*&start=0&max_results=10'
        data = requests.get(url, timeout=None)
        root = ElementTree.fromstring(data.content)
        entries = get_entries(root, val)
        print("\n========================= Len(entries)===================================\n")
        print(len(entries))
        print("\n========================= *********** ===================================\n")

        csv_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/'+ str(val) + '_arxiv.csv'
        csv_headers = ['ID','Topic','Title','Content']

        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
                writer.writeheader()
                for e in entries:
                    writer.writerow(e)
        except IOError:
            print( " \n>>>>>>>>>>>> ERROR in Writing to CSV file for {} <<<<<<<<<<<<\n".format(val) )

        print("\n==============  Done Writing in CSV file for {} ====================\n".format(val))

































        