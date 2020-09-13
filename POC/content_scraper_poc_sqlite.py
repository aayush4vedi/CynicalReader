import csv
import os
import string
import time
from datetime import datetime, timedelta
import asyncio
from aiohttp import ClientSession, TCPConnector
import ssl
import re 
from urlextract import URLExtract

import sqlite3


ENTRIES_TO_BE_WRITTEN = 0                               # total entries in original file
WRITTEN_ENTRIES_ASYNC_DIRECT = 0                        # for every entry written- just copied from prev file
WRITTEN_ENTRIES_ASYNC_SCRAPED = 0                       # for every entry written- fetched by scraping
WRITTEN_ENTRIES_ASYNC_NO_CONTENT_IN_SCRAPING = 0        # when no url after scraping,dont waste the precious article
WRITTEN_ENTRIES_ASYNC_ON_URL_ERROR = 0                  # when unable to hit url,dont waste the precious article
WRITTEN_ENTRIES_ASYNC_TRIED_ERR = 0                     # any other error(try/catch) in scraping,dont waste the precious article
FAILED_ASYNC = 0                                        # other failures

from readability import Document
from bs4 import BeautifulSoup

def contentfromhtml(response):
    """
        get meaningful content from article page.Uses `readability` pkg
        INPUT: http response object.E.g: `response = requests.get(url,verify=False,timeout=30)`
        OUTPUT: single string of text
    """

    ## original starts=======
    article = Document(response)
    # article = Document(response.text)
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
    article = Document(response)
    # article = Document(response.text)
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
    #FIXME: also keeps words like `com` , dates/time, full_length_urls, garbage words .Remove them
    weightedcontent = ' '.join(t for t in soup.find_all(text=True) if t.parent.name in whitelist) 
    return weightedcontent


def getUrlString(intxt):
    common_url_words = ['http', 'https', 'www', 'com', 'html']
    extractor = URLExtract()
    urls = extractor.find_urls(intxt)
    urlstring = ' '.join(urls)
    clean_url_string = re.sub('[^A-Za-z0-9]+', ' ', urlstring)
    clean_url_list = [w for w in clean_url_string.split()]
    new_list = [word for word in clean_url_list if (word not in common_url_words and word.isalpha())]   # remove numbers from url
    return ' '.join(new_list)


async def fetchWithRetry(row, session):

    status = 400
    retry_cnt = 2
    sleep_time = 10
    TIMEOUT = 10

    while retry_cnt > 0 and status != 200:
        async with session.get(row["Url"],ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH), timeout = TIMEOUT) as response: 
            res = await response.text()
            status = response.status
            if( status == 200 and len(res) != 0):
                print("\t\t <ID = {}><src= {} > ============== Scraping Done....... \t NOW: {}".format(row["ID"],row["SourceSite"],time.strftime("%H:%M:%S", time.localtime())))
                urlstrings = getUrlString(row["Content"])
                row["WeightedContent"] = weightedcontentfromhtml(res) + row["Title"] 
                row["Content"] = contentfromhtml(res)  + urlstrings
                if (len(row["Title"]) !=0):
                    # if len(row["Content"]) == 0:          
                    #     row["WeightedContent"] = row["Title"]
                    #     row["Content"] = row["Title"]
                    # await write_result(csv_out,row)
                    global WRITTEN_ENTRIES_ASYNC_SCRAPED
                    WRITTEN_ENTRIES_ASYNC_SCRAPED += 1
                    print(" \t\t ============== [Scraped] Done Writing into csv for <ID = {}><src= {} > =============== ".format(row["ID"],row["SourceSite"]))
                else:
                    global WRITTEN_ENTRIES_ASYNC_NO_CONTENT_IN_SCRAPING
                    WRITTEN_ENTRIES_ASYNC_NO_CONTENT_IN_SCRAPING += 1
                    print("\t\t xxxxxxxxxxxxxxxxxxx SKIPPING  for <ID = {}><src= {} > As No Title xxxxxxxxxxxxxxxxxxxxxxxx\n".format(row["ID"],row["SourceSite"]))
                return row
            else:
                retry_cnt -= 1
                print("\t x---------------- <ID = {}><src= {} > Unable to hit URL(ERR_CODE={}): {}.........  Sleeping for {} Retries remaining = {} -------------x".format(row["ID"],row["SourceSite"],status,row["Url"][:25], sleep_time, retry_cnt))
                await asyncio.sleep(sleep_time)
    #FIXME: howwwwwwwwwwwwwwwwwwwwwwwwwwwwww
    print("\t\txxxxx  For <ID = {}><src= {} >Totally unable to hit url.... using Title for Content & WeightedContent : {} ".format(row["ID"],row["SourceSite"],row["Url"]))
    # if len(row["Content"]) == 0:          
    #     row["WeightedContent"] = row["Title"]
    #     row["Content"] =  row["Title"]
    # await write_result(csv_out,row)
    global WRITTEN_ENTRIES_ASYNC_ON_URL_ERROR 
    WRITTEN_ENTRIES_ASYNC_ON_URL_ERROR += 1
    print(" \t\t\t ============== [Unreachable URL] Done Writing into csv for <ID = {}><src= {} > =============== ".format(row["ID"],row["SourceSite"]))
    return row



async def semaphoreSafeFetch(sem, row, session):
    """
        Simple puts check for semaphore count
    """
    async with sem:
        try:
            return await fetchWithRetry(row, session)
        except Exception as e:
            #FIXME: howwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
            global FAILED_ASYNC
            FAILED_ASYNC += 1
            # This error is mainly because of:
            ## 1. [nodename nor servname provided, or not known]
            ## 2. [Too many open files]
            print("\t======= XXXXXXXX ERROR XXXXXX ======>> <ID = {}><src= {} > NOW = {} Scraping failed. Using Title for Content.... \n \t\t ERROR {}".format(row["ID"],row["SourceSite"],time.strftime("%H:%M:%S", time.localtime()) ,e))
            # if len(row["Content"]) == 0:          
            #     row["WeightedContent"] = row["Title"]
            #     row["Content"] =  row["Title"]
            # await write_result(csv_out,row)
            global WRITTEN_ENTRIES_ASYNC_TRIED_ERR
            WRITTEN_ENTRIES_ASYNC_TRIED_ERR += 1
            print(" \t\t\t============== [Tried Catch] Done Writing into csv for <ID = {}><src= {} > =============== ".format(row["ID"],row["SourceSite"]))
            pass
    return row              #NOTE: this fucker!!!


async def write_result(csv_file, row):
    """
    cleans Content:
        * Content += clean_text(Content)
        * WeightedContent +=  clean_text(WeightedContent) + clean_text(Title) + text_actions.getUrlString(Content)
    """
    sem = asyncio.Semaphore(2)
    async with sem:
        # async with asyncio.Lock():   # lock for gracefully write to shared file object
        # writer.writerow(entry)
        sem2 = asyncio.Semaphore(2)
        async with sem2:
            f = open(csv_file, 'a+')
            writer = csv.writer(f)
            # content = await clean_text(row["Content"])
            # weighted_content = await clean_text(row["WeightedContent"])
            entry = [
                row["ID"],
                row["SourceSite"],
                row["ProcessingDate"],
                row["ProcessingEpoch"],
                row["CreationDate"],
                row["Title"],
                row["Url"],
                row["SourceTags"],
                row["ModelTags"],
                row["NumUpvotes"],
                row["NumComments"],
                row["PopI"],
                row["Content"],
                row["WeightedContent"],
            ]
            writer.writerow(entry)
            f.close()
            del writer


async def asyncFetchAll(url_csv):

    tasks = []
    sem = asyncio.Semaphore(100)

    #========================= db insertion starts here

    """ init connection """
    conn = sqlite3.connect('poc.db', timeout=10)
    c = conn.cursor()

    """ check if table exists: 1. if exists: flush, 2. if not, create """
    #get the count of tables with the name
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='timestamp_wc'")

    #if the count is 1, then table exists
    if c.fetchone()[0]==1 :
        print('**********************************Table exists.Flushing it *****************************')
        c.execute('delete from timestamp_wc')
    else :
        # create table => NOTE: tablename = timestamp+ ("_url",("_wc" or "_wp"))
        print('****************************** Creating a new table: timestamp_wc in db: poc.db *****************************')
        c.execute('''CREATE TABLE timestamp_wc
                (ID, SourceSite, ProcessingDate,ProcessingEpoch,CreationDate, Title, Url, SourceTags,ModelTags,NumUpvotes, NumComments, PopI,WeightedContent,Content)''')

    DIRECT_ENTRIES = 0
    SCRAPED_ENTRIES = 0
    stratTime = time.time()

    connector = TCPConnector(limit=100)
    async with ClientSession(headers={'Connection': 'keep-alive'},connector=connector) as session:
        with open(url_csv, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                # ENTRIES_TO_BE_WRITTEN += 1
                if(len(row["Content"]) != 0):
                    entry = [
                        row["ID"],
                        row["SourceSite"],
                        row["ProcessingDate"],
                        row["ProcessingEpoch"],
                        row["CreationDate"],
                        row["Title"],
                        row["Url"],
                        row["SourceTags"],
                        row["ModelTags"],
                        row["NumUpvotes"],
                        row["NumComments"],
                        row["PopI"],
                        row["WeightedContent"],
                        row["Content"]
                    ]
                    DIRECT_ENTRIES += 1
                    c.execute('INSERT INTO timestamp_wc VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', entry)
                    conn.commit()
                    print("\t\t============== <ID= {} ><{}> [Direct] INSERTED INTO TABLE ===============".format(row["ID"],row["SourceSite"]))
                    #TODO: try insert row
                elif(row["Url"] and row["Title"]):
                    task = asyncio.ensure_future(semaphoreSafeFetch(sem, row, session))
                    tasks.append(task)

        responses = await asyncio.gather(*tasks)

        #db insertion for scraped entries
        for row in responses:
            SCRAPED_ENTRIES += 1
            entry = [
                row["ID"],
                row["SourceSite"],
                row["ProcessingDate"],
                row["ProcessingEpoch"],
                row["CreationDate"],
                row["Title"],
                row["Url"],
                row["SourceTags"],
                row["ModelTags"],
                row["NumUpvotes"],
                row["NumComments"],
                row["PopI"],
                row["WeightedContent"],
                row["Content"]
            ]
            c.execute('INSERT INTO timestamp_wc VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', entry)
            conn.commit()
            print("\t\t============== <ID= {} ><{}> [Scraped] INSERTED INTO TABLE ===============".format(row["ID"],row["SourceSite"]))

    # conn.commit()
    endTime = time.time()
    conn.close()
    print(" \n***************************************  Done Writing into table. TIME TAKEN = {} *********************************** \n".format(endTime - stratTime))
    print("|\t\t DIRECT_ENTRIES \t  | \t {} \t |".format(DIRECT_ENTRIES))
    print("|\t\t SCRAPED_ENTRIES \t | \t {} \t |".format(SCRAPED_ENTRIES))
    print(" \n***************************************  Done Writing into table. TIME TAKEN = {} *********************************** \n".format(endTime - stratTime))

if __name__ == "__main__":
    url_csv = "/Users/aayush.chaturvedi/Desktop/sqlite3demo/url_data.csv"
    asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(asyncFetchAll(url_csv)))




