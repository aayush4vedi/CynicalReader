from bs4 import BeautifulSoup

def getTextFromHtml(raw_text):
    soup = BeautifulSoup(raw_text)
    return soup.get_text()