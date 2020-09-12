from collections import OrderedDict
import requests
from xml.etree import ElementTree
import sys
from csv import writer
import json
import string
import time
from datetime import datetime, timedelta
import sqlite3

from utilities import csv_functions, text_actions, web_requests
from utilities import print_in_color as pc

def run(ts):
    """
        Scrapes Algolia's HN api for last 7 days & puts data in WC-DB.
            * max number of entries in algolia's single api call = 1000. So scrape for one day at a time
            * Link to documentation: https://hn.algolia.com/api
        Note:
            1. For AskHN entries put `` tag & separate threshold
            1. For ShowHN entries put `` tag & separate threshold
            1. For Jobs@HN entries put `` tag => later as these entries dont have upvotes/comments
        Input: ts (format: 1598692058.887741)
    """
    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    pc.printSucc('@[{}] >>>>>> Started HN-scraper ................... => TABLE: {}\n'.format(datetime.fromtimestamp(ts),wc_table))
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < HN_SCRAPER: DB Connection Opened > ---------------------------------------------\n")
    stratTime = time.time()

    """
        here is how you add day to `ts`:

        from datetime import datetime, timedelta
        newts = datetime.fromtimestamp(ts) + timedelta(days=1) # 2020-08-30 16:02:34.352094
        newts.timestamp() # 1598783633.284871
        datetime.fromtimestamp(ts) #2020-08-29 17:15:32
    """

    """ ts_arr has last 7 days(including today's) (non-decimal stype)timestamps strings 
        TIP: use `datetime.fromtimestamp(int(t))` to convert to human readable format
    """
    ts_arr = [str(int(ts))]

    for i in range(6):
        new_ts = datetime.fromtimestamp(int(ts_arr[-1])) + timedelta(days=-1)
        new_ts = new_ts.timestamp()
        ts_arr.append(str(int(new_ts)))

    # for t in ts_arr:
    #     print("timestamp: {} \t date: {}".format(t,datetime.fromtimestamp(int(t))))

    STORY_UP_TH  = 50     #TODO: change this
    SHOWHN_UP_TH = 10     #TODO: change this
    ASKHN_UP_TH  = 10     #TODO: change this
    # csv_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    # f = csv.writer(open(csv_file, 'a',newline=''))  
    index = 1
    TOTAL_ENTRIES_YET = 0

    for i in range(len(ts_arr)-1):
        startepoch = ts_arr[i]
        endepoch   = ts_arr[i+1]
        pc.printMsg(" ................. scraping for interval: start= {} -> end = {} .................\n".format(startepoch,endepoch))

        """ getting stories(articles) with upvotes_count > upvotes_threshold 
            Also including:
            1. TellHN (<discuss>)
            2. LaunchHN (<startup>)
        """
        pc.printWarn(" \t............. scraping stories .............")

        url_story = 'http://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=9999&numericFilters=created_at_i>'+str(endepoch)+',created_at_i<'+ str(startepoch) + ',points>' + str(STORY_UP_TH)
        data = web_requests.hitGetWithRetry(url_story)
        res_size = json.loads(data.content)["nbHits"]

        pc.printMsg("\t\t\t\t====> Item count: {}".format(res_size))

        TOTAL_ENTRIES_YET += res_size
        items_arr = json.loads(data.content)["hits"]

        for item in items_arr:
            # print(json.dumps(item, indent = 4))
            url = 'https://news.ycombinator.com/item?id='+str(item["objectID"])
            sourceTag = ''
            content = ''
            sourceSite = 'HN'
            if(item["url"] is None): #as all ShowHNs may not have an url ...hihi...
                # print( '------------------------- found null urled value ---------------------\n-----[STORY]url: {}'.format(url))
                # print(json.dumps(item, indent = 4))
                if(item["story_text"] is not None):
                    content = text_actions.getTextFromHtml(item["story_text"])
                if("Launch HN:" in item["title"]):                                    # 1. LaunchHN
                    sourceTag = 'startup'
                    sourceSite += '/launch'
                if("Tell HN:" in item["title"]):                                      # 2. TellHN
                    sourceTag = 'discuss'
                    sourceSite += '/tell'
            else:
                url = item["url"] 
            entry = [
                index,
                sourceSite,
                datetime.fromtimestamp(ts),
                int(ts),
                item["created_at"],
                item["title"],              
                url,
                sourceTag,
                '',
                item["points"],
                item["num_comments"],
                '',
                '',
                text_actions.clean_text(content)
                ]
            c.execute('INSERT INTO ' + wc_table + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', entry)
            # csv_functions.putToCsv(csv_file,entry)
            index=index+1

        pc.printMsg("\t\t\t ====>> TOTAL_ENTRIES_YET = {}".format(TOTAL_ENTRIES_YET))

        """ getting ShowHNs """

        pc.printWarn("\t............. scraping showHNs .............")
        url_show = 'http://hn.algolia.com/api/v1/search_by_date?tags=show_hn&hitsPerPage=9999&numericFilters=created_at_i>'+str(endepoch)+',created_at_i<'+ str(startepoch) + ',points>' + str(SHOWHN_UP_TH)
        # data = requests.get(url_show, timeout=None)
        data = web_requests.hitGetWithRetry(url_show)
        res_size = json.loads(data.content)["nbHits"]

        pc.printMsg("\t\t\t\t====> Item count: {}".format(res_size))
        
        TOTAL_ENTRIES_YET += res_size
        items_arr = json.loads(data.content)["hits"]

        for item in items_arr:
            content = ''
            sourceSite = 'HN/show'
            if(item["url"] is None): #as all ShowHNs may not have an url ...hihi...
                url = 'https://news.ycombinator.com/item?id='+str(item["objectID"])
                # print( '-------------------------- found null urled value ---------------------\n-----[SHOW]url: {}'.format(url))
                # print(json.dumps(item, indent = 4))
                if(item["story_text"] is not None):
                    content = text_actions.getTextFromHtml(item["story_text"])
            else:
                url = item["url"] 
            entry = [
                index,
                sourceSite,
                datetime.fromtimestamp(ts),
                int(ts),
                item["created_at"],
                item["title"],              
                url,
                'selfproj',
                '',
                item["points"],
                item["num_comments"],
                '',
                '',
                text_actions.clean_text(content)
                ]
            # csv_functions.putToCsv(csv_file,entry)
            c.execute('INSERT INTO ' + wc_table + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', entry)
            index=index+1

        pc.printWarn("\t\t\t ====>> TOTAL_ENTRIES_YET = {}".format(TOTAL_ENTRIES_YET))

        """ getting AskHNs """

        pc.printWarn("\t............. scraping askHNs .............")
        url_ask = 'http://hn.algolia.com/api/v1/search_by_date?tags=ask_hn&hitsPerPage=9999&numericFilters=created_at_i>'+str(endepoch)+',created_at_i<'+ str(startepoch) + ',points>' + str(ASKHN_UP_TH)
        # data = requests.get(url_ask, timeout=None)
        data = web_requests.hitGetWithRetry(url_ask)
        res_size = json.loads(data.content)["nbHits"]

        pc.printWarn("\t\t\t\t====> Item count: {}".format(res_size))

        TOTAL_ENTRIES_YET += res_size
        items_arr = json.loads(data.content)["hits"]
        

        for item in items_arr:
            content = ''
            sourceSite = 'HN/ask'
            # print(json.dumps(item, indent = 4))
            if(item["url"] is None): #as AskHNs dont have any url ...hihi...
                url = 'https://news.ycombinator.com/item?id='+str(item["objectID"])
                # print( '-------------------------- found null urled value ---------------------\n-----[ASK]url: {}'.format(url))
                # print(json.dumps(item, indent = 4))
                if(item["story_text"] is not None):
                    content = text_actions.getTextFromHtml(item["story_text"])
            else:
                url = item["url"] 
            entry = [
                index,
                sourceSite,
                datetime.fromtimestamp(ts),
                int(ts),
                item["created_at"],
                item["title"],              
                url,
                'query',
                '',
                item["points"],
                item["num_comments"],
                '',
                '',
                text_actions.clean_text(content)
                ]
            c.execute('INSERT INTO ' + wc_table + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', entry)
            # csv_functions.putToCsv(csv_file,entry)
            index=index+1
        pc.printWarn("\t\t\t ====>> TOTAL_ENTRIES_YET = {}".format(TOTAL_ENTRIES_YET))
    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < HN_SCRAPER: DB Connection Closed > ---------------------------------------------\n")
    pc.printSucc("\n\n***************************** HN Url Scraping is Complete. TABLE: {} ******************".format(wc_table))
    pc.printSucc("| \t\t TOTAL URLS FETCHED                    \t\t | \t\t {} \t\t |".format(TOTAL_ENTRIES_YET))
    pc.printSucc("| \t\t TIME TAKEN FOR URL SCRAPING           \t\t | \t\t {}  \t\t |".format(int(endTime - stratTime)))
    pc.printSucc("*************************************************************************************************\n\n")
