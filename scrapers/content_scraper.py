# encoding: utf-8
import csv
import os
import string
import time
import json
from datetime import datetime, timedelta
import asyncio
import aiohttp
from aiohttp import ClientSession, TCPConnector, ClientTimeout
import traceback
import logging
# import aiohttp_proxy
# from aiohttp_proxy import ProxyConnector, ProxyType
import socket
import ssl
import sqlite3
import re 
from urlextract import URLExtract

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from readability import Document
from bs4 import BeautifulSoup

from utilities import csv_functions, text_actions, web_requests
from utilities import print_in_color as pc

SEMAPHORE_COUNT = 10
CONNTECTION_COUNT = 10

TOTAL_ITEMS_TO_BE_FETCHED = 0                            # Total items in wc table(as returned by url_scraper)
ASYNC_ITEM_SCRAPED = 0                                   # Successfully hit url & get content with async method
ASYNC_URL_UNREACHABLE = 0                                # Url unreachable after retries with async
ASYNC_SEMA_EXCEPTION_ERR = 0                             # Tried-Catch error when running async jobs with semaphore
ASYNC_ITEM_WRITTEN_DIRECT = 0                            # No need to scrape item with asycn, content already present
SYNC_ITEM_SCRAPED = 0                                    # Successfully hit url & get content with sync method
SYNC_URL_UNREACHABLE = 0                                 # Url unreachable after retries with sync
SYNC_TRIED_CATCH_EXCEPTION_ERR = 0                              # Tried-Catch error when running sync get
ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK = 0              # Item finally put in with content
ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT = 0      # Item finally put in with Title as content


""" ============================================================================================== text_action functions:START ================================"""
extractor = URLExtract()
wordnet = WordNetLemmatizer()

def getUrlString(intxt):
    common_url_words = ['http', 'https', 'www', 'com', 'html']
    # extractor = URLExtract()
    urls = extractor.find_urls(intxt)
    urlstring = ' '.join(urls)
    clean_url_string = re.sub('[^A-Za-z0-9]+', ' ', urlstring)
    clean_url_list = [w for w in clean_url_string.split()]
    new_list = [word for word in clean_url_list if (word not in common_url_words and word.isalpha())]   # remove numbers from url
    return ' '.join(new_list)

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



""" ============================================================================================== text_action functions:START ================================"""

""" =============== Async-Executor Helpers: START ===============  """

async def fetchWithRetry(row, session):
    """
        Hits ulr(with retires):
        * if status == 200:
            return resposne ((raw)Content & (raw)WeightedContent in row)
        * if still unable to hit after retries: Content = Title , WeightedContent = Title
        INPUT: `row` is an array with indices: 
            ID(0),SourceSite(1),ProcessingDate(2),ProcessingEpoch(3),CreationDate(4),Title(5),Url(6),
            SourceTags(7),ModelTags(8),NumUpvotes(9),NumComments(10),PopI(11),WeightedContent(12),Content(13)
    """

    status = 400
    retry_cnt = 2
    sleep_time = 2
    TIMEOUT = 60

    global ASYNC_ITEM_SCRAPED, ASYNC_URL_UNREACHABLE
    
    t1 = time.time()
    while retry_cnt > 0 and status != 200:
        async with session.get(row[6],ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH), timeout = TIMEOUT) as response: 
            # res = await response.content.read()       #NOTE: returns blob which gives error while ContentFormatter; hence discarded
            res = await response.text()
            status = response.status
            if( status == 200 and len(res) != 0):
                ASYNC_ITEM_SCRAPED += 1
                pc.printSucc("\t\t <ID = {}><src= {} > ============== #ASYNC_Scraped ....... \t\t TimeTaken = {} \t NOW: {}".format(row[0],row[1],round((round((time.time()-t1),5)),5),time.strftime("%H:%M:%S", time.localtime())))
                row_list = list(row)
                row_list[13] = res
                row = tuple(row_list)
                return row
            else:
                retry_cnt -= 1
                pc.printWarn("\t x---------------- <ID = {}><src= {} > Unable to hit URL(ERR_CODE={}): {}.........  Sleeping for {} Retries remaining = {} -------------x".format(row[0],row[1],status,row[6][:25], sleep_time, retry_cnt))
                await asyncio.sleep(sleep_time)
    ASYNC_URL_UNREACHABLE += 1
    pc.printErr("\t\txxxxx  For <ID = {}><src= {} >Totally unable to hit url.... Will try sync later: {} \t\t TimeTaken = {} \t NOW: {}".format(row[0],row[1],row[6],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
    return row




async def semaphoreSafeFetch(sem, row, session):
    """
        Simple puts check for semaphore count
    """

    global ASYNC_SEMA_EXCEPTION_ERR

    async with sem:
        try:
            return await fetchWithRetry(row, session)
        except Exception as e:
            ASYNC_SEMA_EXCEPTION_ERR += 1
            pc.printWarn("\t======= XXXXXXXXXXXXXX ======>> <ID = {}><src= {} > NOW = {} Async Scraping failed.Will try sync later... \n \t\t ERROR=> {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime()) ,e))
            logging.error(traceback.format_exc())
            pass
    return row          


async def asyncFetchAll(ts):
    """
        just add the content into Content column, no cleaning OR weightedContent OR UrlString etc. here.
    """
    global CONNTECTION_COUNT, SEMAPHORE_COUNT

    tasks = []
    sem = asyncio.Semaphore(SEMAPHORE_COUNT)

    global ASYNC_ITEM_WRITTEN_DIRECT
    global TOTAL_ITEMS_TO_BE_FETCHED

    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < CONTENT_SCRAPER_ASYNC: DB Connection Opened > ---------------------------------------------\n")
    startTime = time.time()

    socket.gethostbyname("")
    connector = TCPConnector(limit=CONNTECTION_COUNT,family=socket.AF_INET,verify_ssl=False)
    # connector = TCPConnector(limit=CONNTECTION_COUNT)
    async with ClientSession(headers={'Connection': 'keep-alive'},connector=connector) as session:
        q = "select * from " + wc_table
        rows_head = c.execute(q)
        rows = rows_head.fetchall()
        for row in rows:
            TOTAL_ITEMS_TO_BE_FETCHED += 1
            """
                ============= row is an array with indices: 
                ID(0),SourceSite(1),ProcessingDate(2),ProcessingEpoch(3),CreationDate(4),Title(5),Url(6),
                SourceTags(7),ModelTags(8),NumUpvotes(9),NumComments(10),PopI(11),WeightedContent(12),Content(13)
            """
            t1 = time.time()

            if(len(row[13]) != 0):
                ASYNC_ITEM_WRITTEN_DIRECT += 1
                pc.printWarn("\t <ID = {}><src= {} > [NO SCRAPING] Content already exists............... \t\t TimeTaken = {} \t NOW: {}".format(row[0],row[1],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
                content = row[13]  
                q = 'update ' + wc_table + ' set Content = ? where ID = ? and SourceSite = ?'
                d = (content,row[0],row[1])
                c.execute(q,d)
                pc.printSucc(" \t\t ============== <ID= {} ><{}> [Direct] INSERTED INTO TABLE =============== ".format(row[0],row[1]))
            elif(row[5] and row[6]): # else ignore the entry
                task = asyncio.ensure_future(semaphoreSafeFetch(sem, row, session))
                tasks.append(task)

        responses = await asyncio.gather(*tasks)
        for row in responses:
            if row:
                content = row[13]  
                q = 'update ' + wc_table + ' set Content = ? where ID = ? and SourceSite = ?'
                d = (content,row[0],row[1])
                c.execute(q,d)
                pc.printSucc(" \t\t ============== <ID= {} ><{}> [Scraped] INSERTED INTO TABLE =============== ".format(row[0],row[1]))
        
    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < CONTENT_SCRAPER_ASYNC: DB Connection Closed > ---------------------------------------------\n")
    pc.printMsg("\n\n--------------------------------------------------------------------------------------------------------------------------------")   
    pc.printMsg("|\t\t IN : TOTAL_ITEMS_TO_BE_FETCHED                         [X]          \t  | \t\t {} \t\t|".format(TOTAL_ITEMS_TO_BE_FETCHED)) 
    pc.printMsg("|\t\t OUT : ASYNC_ITEM_SCRAPED                               [A] (A+B+C=X)\t  | \t\t {} \t\t|".format(ASYNC_ITEM_SCRAPED)) 
    pc.printMsg("|\t\t OUT : ASYNC_ITEM_WRITTEN_DIRECT                        [B] (A+B+C=X)\t  | \t\t {} \t\t|".format(ASYNC_ITEM_WRITTEN_DIRECT)) 
    pc.printErr("\n\n------------------------------------------ ERRORS (Written nonetheless, chill) ------------------------------------------------\n")    
    pc.printMsg("|\t\t ASYNC_URL_UNREACHABLE                                               \t  | \t\t {} \t\t|".format(ASYNC_URL_UNREACHABLE)) 
    pc.printMsg("|\t\t ASYNC_SEMA_EXCEPTION_ERR                                            \t  | \t\t {} \t\t|".format(ASYNC_SEMA_EXCEPTION_ERR)) 
    pc.printWarn('\t\t\t------------------------->>>>>> [ TimeTaken (min) = {} ]\n'.format(round((endTime - startTime),5)/60))



def RunSync(ts):

    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < CONTENT_SCRAPER_SYNC: DB Connection Opened > ---------------------------------------------\n")
    startTime = time.time()

    global SYNC_ITEM_SCRAPED,SYNC_URL_UNREACHABLE,SYNC_TRIED_CATCH_EXCEPTION_ERR

    q = "select * from " + wc_table
    rows_head = c.execute(q)
    rows = rows_head.fetchall()
    for row in rows:
        t1 = time.time()
        if(len(row[13]) == 0):
            try:
                response = web_requests.hitGetWithRetry(row[6],'',False ,2,0.5,30)
                if response != -1:
                    SYNC_ITEM_SCRAPED += 1
                    res = response.text 
                    row_list = list(row)
                    row_list[13] = res
                    row = tuple(row_list)
                        
                    pc.printWarn("\t <ID = {}><src= {} > [SYNCED SCRAPING] Done................ \t\t TimeTaken = {} \t NOW: {} ".format(row[0],row[1],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
                    q = 'update ' + wc_table + ' set Content = ? where ID = ? and SourceSite = ?'
                    d = (row[13],row[0],row[1])
                    c.execute(q,d)
                    pc.printSucc(" \t\t ============== <ID= {} ><{}> [SYNCED SCRAPING] INSERTED INTO TABLE =============== ".format(row[0],row[1]))
                else:
                    SYNC_URL_UNREACHABLE += 1
                    pc.printErr("\t\txxxxx SKIPPING... for ID: {} Totally unable to hit url even in SYNC: {}  \t\t TimeTaken = {} \t NOW: {} ".format(row[0],row[6],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
            except Exception as e:
                SYNC_TRIED_CATCH_EXCEPTION_ERR += 1
                pc.printErr("\t======= XXXXXXXXXXXXXX ======>> <ID = {}><src= {} > NOW = {} , \t\t TimeTaken = {} ....Sync Scraping failed too.Will use Title for content... \n \t\t ERROR=> {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime()),round((time.time()-t1),5) ,e))
                logging.error(traceback.format_exc())
                pass
    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < CONTENT_SCRAPER_SYNC: DB Connection Closed > ---------------------------------------------\n")
    pc.printMsg("\n\n--------------------------------------------------------------------------------------------------------------------------------")   
    pc.printMsg("|\t\t IN : TOTAL_ITEMS_TO_BE_FETCHED                         [X]          \t  | \t\t {} \t\t|".format(TOTAL_ITEMS_TO_BE_FETCHED)) 
    pc.printMsg("|\t\t OUT : SYNC_ITEM_SCRAPED                                [C] (A+B+C=X)\t  | \t\t {} \t\t|".format(SYNC_ITEM_SCRAPED)) 
    pc.printErr("\n\n------------------------------------------ ERRORS (Written nonetheless, chill) ------------------------------------------------\n")    
    pc.printMsg("|\t\t SYNC_URL_UNREACHABLE                                                \t  | \t\t {} \t\t|".format(SYNC_URL_UNREACHABLE)) 
    pc.printMsg("|\t\t SYNC_TRIED_CATCH_EXCEPTION_ERR                                      \t  | \t\t {} \t\t|".format(SYNC_TRIED_CATCH_EXCEPTION_ERR)) 
    pc.printWarn('\t\t\t------------------------->>>>>> [ TimeTaken (min) = {} ]\n'.format(round((endTime - startTime),5)/60))



""" --------------------------------===============  sync-Executor : END ===============--------------------------------  """



#############################TODO:                     make async------> taking freaking 20 mins now
def ContentFormatting(ts):
    """ 
    Do:
        0. Update Content & WeightedContent column for each row
        1. get url_strings_content = getUrlString(row[13]) -> add it in weighted_content
        2. do clean_text(row[13])
        2. do clean_text(row[12])
        3. clean text clean_text(row[5]) -> add it in weighted_content :: clean_text(row[12]) + " " + clean_title + " " + url_strings_content
        4. if content col is still null; put title into it & in weightedContent too
    """

    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < Content Formatter: DB Connection Opened > ---------------------------------------------\n")
    startTime = time.time()
    pc.printWarn("\tRunning ContentFormatter for wc ....... \t NOW: {}".format(time.strftime("%H:%M:%S", time.localtime())))
    pc.printWarn("\t\t. .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .")

    global ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK, ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT,TOTAL_ITEMS_TO_BE_FETCHED

    q = "select * from " + wc_table
    rows_head = c.execute(q)
    rows = rows_head.fetchall()
    for row in rows:
        t1 = time.time()
        if(len(row[13]) != 0):
            ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK += 1
            row_list = list(row)
            raw_content = row_list[13]
            content = text_actions.contentfromhtml(raw_content)
            clean_content = clean_text(content)
            weighted_content = text_actions.weightedcontentfromhtml(raw_content) 
            clean_weighted_content = clean_text(weighted_content)
            url_string_text = getUrlString(raw_content)
            clean_title = clean_text(row_list[5])
            
            row_list[13] = clean_content
            if len(row_list[13]) == 0:
                pc.printWarn("\t\t\t\t --------- No content found on cleaning, using Title as Content :(")
                row_list[13] = clean_title

            row_list[12] = clean_weighted_content + " " + url_string_text + " " + clean_title

            row = tuple(row_list)
                
            pc.printWarn("\t <ID = {}><src= {} > [Content Formatting] Done................ \t\t TimeTaken = {} \t NOW: {}".format(row[0],row[1],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
            content = row[13]  
            q = 'update ' + wc_table + ' set Content = ?, WeightedContent = ?  where ID = ? and SourceSite = ?'
            d = (row[13], row[12],row[0],row[1])
            c.execute(q,d)
            pc.printSucc(" \t\t ============== <ID= {} ><{}> [Content Formatting]-with content INSERTED INTO TABLE =============== ".format(row[0],row[1]))
        else: #No content
            ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT += 1
            pc.printMsg("\t <ID = {}><src= {} > [Content Formatting] No content.Using title finally................ \t\t TimeTaken = {} \t NOW: {}".format(row[0],row[1],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
            clean_title = clean_text(row_list[5])
            content = clean_title 
            q = 'update ' + wc_table + ' set Content = ?, WeightedContent = ?  where ID = ? and SourceSite = ?'
            d = (content, content,row[0],row[1])
            c.execute(q,d)
            pc.printSucc(" \t\t ============== <ID= {} ><{}> [Content Formatting]-without content INSERTED INTO TABLE =============== ".format(row[0],row[1]))
    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < Content Formatter: DB Connection Closed > ---------------------------------------------\n")
    pc.printMsg("\n--------------------------------------------------------------------------------------------------------------------------------")   
    pc.printMsg("|\t\t IN : TOTAL_ITEMS_TO_BE_FETCHED                         [X]          \t  | \t\t {} \t\t|".format(TOTAL_ITEMS_TO_BE_FETCHED)) 
    pc.printMsg("|\t\t OUT : ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK          [P] (P+Q=X)  \t  | \t\t {} \t\t|".format(ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK)) 
    pc.printMsg("|\t\t OUT : ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT  [Q] (P+Q=X)  \t  | \t\t {} \t\t|".format(ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT)) 
    pc.printWarn('\t\t\t------------------------->>>>>> [ TimeTaken (min) = {} ]\n'.format(round((endTime - startTime),5)/60))


""" ===============  Async-Executor Helpers: END ===============  """


def run(ts):
    global CONNTECTION_COUNT
    global SEMAPHORE_COUNT

    global TOTAL_ITEMS_TO_BE_FETCHED
    global ASYNC_ITEM_SCRAPED
    global ASYNC_ITEM_WRITTEN_DIRECT
    global SYNC_ITEM_SCRAPED
    global ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK
    global ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT
    global ASYNC_URL_UNREACHABLE
    global ASYNC_SEMA_EXCEPTION_ERR
    global SYNC_URL_UNREACHABLE
    global SYNC_TRIED_CATCH_EXCEPTION_ERR

    wc_table = 'wc_' + str(int(ts))
    pc.printMsg('@[{}] >>>>>> Started Content-scraper(ASYNC) .......[Sema = {}, conn_lim ={}]............ => TABLE: {}\n'.format(datetime.fromtimestamp(ts),SEMAPHORE_COUNT,CONNTECTION_COUNT,wc_table))

    startTime = time.time()

    # """ scrape content in async """
    asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(asyncFetchAll(ts)))
    time.sleep(10)

    """ scrape remaining items with sync """
    RunSync(ts) 

    """ formatting everything in the end-done in sync """
    ContentFormatting(ts) #TODO: see if it can be made async-----------------taking 30 mins

    endTime = time.time()
    pc.printSucc("\n****************** Content Scraping is Complete , TABLE: {} ********************".format(wc_table))   
    pc.printMsg("\n--------------------------------------------------------------------------------------------------------------------------------")   
    pc.printMsg("|\t\t IN : TOTAL_ITEMS_TO_BE_FETCHED                         [X] (A+B+C+D=X)\t  | \t\t {} \t\t|".format(TOTAL_ITEMS_TO_BE_FETCHED)) 
    pc.printMsg("|\t\t OUT : ASYNC_ITEM_SCRAPED                               [A]            \t  | \t\t {} \t\t|".format(ASYNC_ITEM_SCRAPED)) 
    pc.printMsg("|\t\t OUT : ASYNC_ITEM_WRITTEN_DIRECT                        [B]            \t  | \t\t {} \t\t|".format(ASYNC_ITEM_WRITTEN_DIRECT)) 
    pc.printMsg("|\t\t OUT : SYNC_ITEM_SCRAPED                                [C]            \t  | \t\t {} \t\t|".format(SYNC_ITEM_SCRAPED)) 
    pc.printMsg("|\t\t OUT : ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK          [Y] (A+B+C=Y)  \t  | \t\t {} \t\t|".format(ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK)) 
    pc.printMsg("|\t\t OUT : ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT  [D]            \t  | \t\t {} \t\t|".format(ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT)) 
    pc.printErr("\n\n------------------------------------------ ERRORS (Written nonetheless, chill) ------------------------------------------------\n")    
    pc.printErr("|\t\t ASYNC_URL_UNREACHABLE                                               \t  | \t\t {} \t\t|".format(ASYNC_URL_UNREACHABLE)) 
    pc.printErr("|\t\t ASYNC_SEMA_EXCEPTION_ERR                                            \t  | \t\t {} \t\t|".format(ASYNC_SEMA_EXCEPTION_ERR)) 
    pc.printErr("|\t\t SYNC_URL_UNREACHABLE                                                \t  | \t\t {} \t\t|".format(SYNC_URL_UNREACHABLE)) 
    pc.printErr("|\t\t SYNC_TRIED_CATCH_EXCEPTION_ERR                                      \t  | \t\t {} \t\t|".format(SYNC_TRIED_CATCH_EXCEPTION_ERR)) 
    pc.printWarn('\t\t\t\t------------------------->>>>>> [ Semaphore Count = {}, Tcp connector limit ={} ]\n'.format(SEMAPHORE_COUNT,CONNTECTION_COUNT))
    pc.printWarn('\t\t\t\t------------------------->>>>>> [ Time Taken(min) = {} ]\n'.format(round((endTime - startTime),5)/60))
