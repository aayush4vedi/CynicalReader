import string
import requests
import re 
from urlextract import URLExtract
from readability import Document

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from bs4 import BeautifulSoup


def contentfromhtml(response):
    """
        get meaningful content from article page.Uses `readability` pkg
        INPUT: http response object.E.g: `response = requests.get(url,verify=False,timeout=30)`
        OUTPUT: single string of text
    """

    ## original starts=======
    article = Document(response.text)
    html = article.summary()
    soup = BeautifulSoup(html)
    ## ==========oring ends

    ############### Trying out bs4 approach
    # soup = BeautifulSoup(response)
    # html =  soup.get_text() 
    # print("-------------------html---------------\n {} \n ========================\n".format(html))
    ### ============END trying 
    
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
        INPUT: http response object.E.g: `response = requests.get(url,verify=False,timeout=30)`
        OUTPUT: single string of text
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
    return weightedcontent

def clean_text(text):
    """Clean raw text using different methods :
       1. tokenize text
       2. lower text
       3. remove punctuation
       4. remove non-alphabetics char
       5. remove stopwords
       6. lemmatize
       INPUT: string
       OUTPUT: string
    """
    #initialize wordnet
    wordnet = WordNetLemmatizer()

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

"""
    given raw text; finds all the useful words in urls; stiches them into a string & retursn that string.
    Mainly to be put in weightedcontent
"""
def getUrlString(intxt):
    common_url_words = ['http', 'https', 'www', 'com']
    extractor = URLExtract()
    urls = extractor.find_urls(intxt)
    urlstring = ' '.join(urls)
    clean_url_string = re.sub('[^A-Za-z0-9]+', ' ', urlstring)
    print("clean_url_string: ",clean_url_string)
    clean_url_list = [w for w in clean_url_string.split()]
    print("clean_url_list: ",clean_url_list)
    new_list = [word for word in clean_url_list if word not in common_url_words]
    return ' '.join(new_list)