# -*- coding: utf-8 -*-

import requests
import string
from bs4 import BeautifulSoup

import ph_tags_data

if __name__ == '__main__':
    # url = 'https://www.producthunt.com/topics'
    rawHTML = ph_tags_data.ph_tags_html_data
    soup = BeautifulSoup(rawHTML, 'lxml')
    # soup = BeautifulSoup(data.text, 'lxml')
    divs = soup.findAll("div", class_="item_56e23")
    for div in divs:
            # print(div) 
            span1 = div.find('a', {'class': 'info_d7201'}).contents[0]
            tag = span1.contents[0]
            span2 = div.find('a', {'class': 'info_d7201'}).contents[1]
            about = ''
            if(len(span2)>0):
                about = span2.contents[0]
            print('* {} - {}'.format(tag,about))