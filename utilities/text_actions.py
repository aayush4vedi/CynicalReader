import string
import requests
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
    wordnet = WordNetLemmatizer()
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    stemmed = [wordnet.lemmatize(word) for word in words]
    return ' '.join(stemmed)


def getTextFromHtml(raw_text):
    soup = BeautifulSoup(raw_text)
    return soup.get_text()