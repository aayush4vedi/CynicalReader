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
from prettytable import PrettyTable
import socket
import ssl
import sqlite3
import re 
import signal
from urlextract import URLExtract
import nest_asyncio

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from readability import Document
from bs4 import BeautifulSoup

from utilities import csv_functions, text_actions, web_requests
from utilities import print_in_color as pc
from utilities import global_wars as gw

""" ============================================================================================== text_action functions:START ================================"""
extractor = URLExtract()
wordnet = WordNetLemmatizer()


def timeout_handler(signum, frame):
    raise Exception("Function Timed Out !!!!!!")

def getUrlString(intxt):
    common_url_words = ['http', 'https', 'www', 'com', 'html', 'htm','pdf','mp3','mp4','jpg','jpeg','gif','png', ':','/','//']
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



""" ============================================================================================== text_action functions:END ================================"""

""" =============== Async-Executor Helpers: START ===============  """

async def fetchWithRetry(conn,row, session,series_count,ts):
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
    sleep_time = 0.1

    t1 = time.time()
    while retry_cnt > 0 and status != 200:
        async with session.get(row[6],ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH), timeout = gw.CS_ASYNC_REQ_TIMEOUT) as response: 
            # res = await response.content.read()       # returns blob which gives error while ContentFormatter; hence discarded
            res = await response.text()
            status = response.status
            if( status == 200 and len(res) != 0):
                gw.CS_ASYNC_ITEM_SCRAPED += 1
                gw.CS_BOYS_STILL_PLAYING -= 1
                pc.printSucc("\t\t <ID = {}><src= {} > ============== [ASYNCED SCRAPED#{}] Done ....... \t\t TimeTaken = {} \t NOW: {}".format(row[0],row[1],series_count,round((round((time.time()-t1),5)),5),time.strftime("%H:%M:%S", time.localtime())))
                row_list = list(row)
                row_list[13] = res
                row = tuple(row_list)

                # wc_db = 'dbs/wc.db'
                wc_table = 'wc_' + str(int(ts))
                # conn = sqlite3.connect(wc_db)
                # gw.SQL_CONN_OPEN += 1
                try:
                    c = conn.cursor()
                    q = 'update ' + wc_table + ' set Content = ? where ID = ? and SourceSite = ?'
                    d = (row[13],row[0],row[1])
                    c.execute(q,d)
                    pc.printWarn(" \t\t ============== <ID= {} ><{}> [ASYNC ContentScraped] \t INSERTED INTO TABLE :: gw.SQL_CONN_OPEN = {} =============== ".format(row[0],row[1],gw.SQL_CONN_OPEN))
                    conn.commit()
                except Exception as e:
                    pc.printMsg(" \t\t === XXXX ====== <ID= {} ><{}> [ASYNC ContentScraped] \t ERRR in INSERTED INTO TABLE :: gw.SQL_CONN_OPEN = {} =============== ".format(row[0],row[1],gw.SQL_CONN_OPEN))
                    logging.error(traceback.format_exc())
                    pass
                # conn.close()
                # gw.SQL_CONN_OPEN -= 1

                return row
            else:
                retry_cnt -= 1
                pc.printWarn("\t x---------------- <ID = {}><src= {} > Unable to hit URL(ERR_CODE={}): {}.........  Sleeping for {} Retries remaining = {} -------------x".format(row[0],row[1],status,row[6][:25], sleep_time, retry_cnt))
                await asyncio.sleep(sleep_time)
    if series_count == gw.ASYNC_SERIES_CONNECTION:
        gw.CS_ASYNC_URL_UNREACHABLE += 1
        pc.printErr("\t\txxxxx  For <ID = {}><src= {} >Totally unable to hit url.... Will try sync later: {} \t\t TimeTaken = {} \t NOW: {}".format(row[0],row[1],row[6],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
    # return row 
    return []




# async def semaphoreSafeFetch(sem, row, session,series_count):
#     """
#         Simply puts semaphore limit on async-fetch
#     """

#     async with sem:
#         try:
#             return await fetchWithRetry(row, session,series_count)
#         except Exception as e:
#             if series_count == gw.ASYNC_SERIES_CONNECTION:      # dont count the errors in each series run.Some might get ressolved in next one.
#                 gw.CS_ASYNC_SEMA_EXCEPTION_ERR += 1
#                 pc.printWarn("\t======= XXXXXXXXXXXXXX ======>> <ID = {}><src= {} > NOW = {} Async Scraping failed.Will try SYNC later... \n \t\t ERROR=> {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime()) ,e))
#                 # logging.error(traceback.format_exc())
#             pass
#     return [] 


async def semaphoreSafeFetch(conn,sem, row, session,series_count,ts):
    """
        Simply puts semaphore limit on async-fetch
    """

    # async with sem:
    #     try:
    #         row = await fetchWithRetry(row, session,series_count)
    #         if row and len(row[13]) >0:
    #             # await semaphoreSqlUpdate(row,ts)
    #             wc_db = 'dbs/wc.db'
    #             wc_table = 'wc_' + str(int(ts))
    #             content = row[13]  
    #             conn = sqlite3.connect(wc_db)
    #             gw.SQL_CONN_OPEN += 1
    #             c = conn.cursor()
    #             q = 'update ' + wc_table + ' set Content = ? where ID = ? and SourceSite = ?'
    #             d = (content,row[0],row[1])
    #             c.execute(q,d)
    #             pc.printWarn(" \t\t ============== <ID= {} ><{}> [ASYNC ContentScraped] \t INSERTED INTO TABLE :: gw.SQL_CONN_OPEN = {} =============== ".format(row[0],row[1],gw.SQL_CONN_OPEN))
    #             conn.commit()
    #             conn.close()
    #             gw.SQL_CONN_OPEN -= 1
    #     except Exception as e:
    #         if series_count == gw.ASYNC_SERIES_CONNECTION:      # dont count the errors in each series run.Some might get ressolved in next one.
    #             gw.CS_ASYNC_SEMA_EXCEPTION_ERR += 1
    #             pc.printWarn("\t======= XXXXXXXXXXXXXX ======>> <ID = {}><src= {} > NOW = {} Async Scraping failed.Will try SYNC later... \n \t\t ERROR=> {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime()) ,e))
    #             # logging.error(traceback.format_exc())
    #         pass
    # return []        
    async with sem:
        try:
            row = await fetchWithRetry(conn,row, session,series_count,ts)
            if row and len(row[13]) >0:
                # await semaphoreSqlUpdate(row,ts)
                content = row[13]  
        except Exception as e:
            if series_count == gw.ASYNC_SERIES_CONNECTION:      # dont count the errors in each series run.Some might get ressolved in next one.
                gw.CS_ASYNC_SEMA_EXCEPTION_ERR += 1
                pc.printWarn("\t======= XXXXXXXXXXXXXX ======>> <ID = {}><src= {} > NOW = {} Async Scraping failed.Will try SYNC later... \n \t\t ERROR=> {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime()) ,e))
                # logging.error(traceback.format_exc())
            pass
    return []        

#NOTE: Abandoned SQL ingesion async because of mutex issue with sql
# async def semaphoreSqlUpdate(row,ts):
#     try:
#         wc_db = 'dbs/wc.db'
#         wc_table = 'wc_' + str(int(ts))
#         content = row[13]  
#         conn = sqlite3.connect(wc_db)
#         gw.SQL_CONN_OPEN += 1
#         c = conn.cursor()
#         q = 'update ' + wc_table + ' set Content = ? where ID = ? and SourceSite = ?'
#         d = (content,row[0],row[1])
#         c.execute(q,d)
#         pc.printSucc(" \t\t ============== <ID= {} ><{}> [ASYNC ContentScraped] \t INSERTED INTO TABLE :: gw.SQL_CONN_OPEN = {} =============== ".format(row[0],row[1],gw.SQL_CONN_OPEN))
#         conn.commit()
#         conn.close()
#         gw.SQL_CONN_OPEN -= 1
#         # return 1
#     except Exception as e:
#         pc.printWarn("\t======= XXXXXXXXXXXXXX SEMAPHORE_SQL_UPDATE_ERR:: gw.SQL_CONN_OPEN = {} ======>> <ID = {}><src= {} > NOW = {} \n \t\t ERROR=> {}".format(gw.SQL_CONN_OPEN,row[0],row[1],time.strftime("%H:%M:%S", time.localtime()) ,e))
#         logging.error(traceback.format_exc())    
#         pass
#     # return 0 
    

""" ===============  Async-Executor Helpers: END ===============  """

async def asyncFetchAll(conn,ts,series_count):       #series_count : {1,gw.ASYNC_SERIES_CONNECTION}
    """
        just add the content into Content column, no cleaning OR weightedContent OR UrlString etc. here.
    """

    # wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    # conn = sqlite3.connect(wc_db)
    # gw.SQL_CONN_OPEN += 1
    c = conn.cursor()
    q = "select * from " + wc_table + " where length(Content) = 0"  # only get the rows without content
    rows_head = c.execute(q)
    rows = rows_head.fetchall()
    conn.commit()
    # conn.close()
    # gw.SQL_CONN_OPEN -= 1
    pc.printMsg("\t -------------------------------------- < CONTENT_SCRAPER_ASYNC: DB/wc Connection Opened > ---------------------------------------------\n")
    startTime = time.time()

    socket.gethostbyname("")
    connector = TCPConnector(limit=gw.CONNECTION_COUNT,family=socket.AF_INET,verify_ssl=False)
    pc.printMsg("\n\n===================================================================== Doing {}-th Async Scraping in the same table =====================================================================\n\n".format(series_count))
    async with ClientSession(headers={'Connection': 'keep-alive'},connector=connector) as session:

        tasks = []
        sem = asyncio.Semaphore(gw.SEMAPHORE_COUNT)
        for row in rows:
            """
                ============= row is an array with indices: 
                ID(0),SourceSite(1),ProcessingDate(2),ProcessingEpoch(3),CreationDate(4),Title(5),Url(6),
                SourceTags(7),ModelTags(8),NumUpvotes(9),NumComments(10),PopI(11),WeightedContent(12),Content(13)
            """
            t1 = time.time()
            if(row[5] and row[6]): # else ignore the entry
                gw.CS_BOYS_STILL_PLAYING += 1
                if gw.CS_BOYS_STILL_PLAYING % gw.CS_BOYS_PLAYING_LIMIT == 0:
                    pc.printMsg("\t [ASYNC_SCRAPING] sleeping for 1 sec...zzzzzzzzz....... \t BOYS_STILL_PLAYING = {}".format(gw.CS_BOYS_STILL_PLAYING))
                    time.sleep(1)
                # task = asyncio.ensure_future(semaphoreSafeFetch(sem, row, session,series_count))
                task = asyncio.ensure_future(semaphoreSafeFetch(conn,sem, row, session,series_count,ts))
                tasks.append(task)

        await asyncio.gather(*tasks)
        # responses = await asyncio.gather(*tasks)
        # for row in responses:
        #     if row and len(row[13]) >0:
        #         try:
        #             content = row[13]  
        #             conn = sqlite3.connect(wc_db)
        #             c = conn.cursor()
        #             q = 'update ' + wc_table + ' set Content = ? where ID = ? and SourceSite = ?'
        #             d = (content,row[0],row[1])
        #             c.execute(q,d)
        #             pc.printSucc(" \t\t ============== <ID= {} ><{}> [ASYNC ContentScraped] \t INSERTED INTO TABLE =============== ".format(row[0],row[1]))
        #             conn.commit()
        #             conn.close()
        #         except Exception as e:
        #             logging.error(traceback.format_exc())
        #         pass
        # succs = []
        # for row in responses:
        #     if row and len(row[13]) >0:
        #         succ = asyncio.ensure_future(semaphoreSqlUpdate(sem,row,ts))
        #         succs.append(succ)
        # succsx = await asyncio.gather(*succs)

    endTime = time.time()
    
    pc.printSucc("\n***************************** {} -th Async Content Scraping is Complete. TABLE: {} ******************".format(series_count,wc_table))
    print("\n\n")
    table = PrettyTable(['Success (Post Async Content Scraping)', 'Notation(if any)','Value'])
    table.add_row(['OUT : TOTAL ITEMS SCRAPED WITH ASYNC YET','[B] (A+B+C=X)' ,gw.CS_ASYNC_ITEM_SCRAPED])
    pc.printSucc(table)
    print("\n")
    pc.printWarn('\t\t\t------------------------->>>>>> [ TimeTaken for Async Scraping (min) = {} ]\n'.format(round((endTime - startTime),5)/60))
    print("\n\n")


async def RunAsync(ts):
    """
        Does ASYNC_SERIES_CONNECTION times number of series executions in parallel
    """
    startTime = time.time()
    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    conn = sqlite3.connect(wc_db)

    """ get rows with content alredy present & put in gw.CS_ITEMS_WRITTEN_DIRECT .Will work just for 1st iteration"""
    c = conn.cursor()
    q = "select count(*) from " + wc_table + " where length(Content) != 0"
    no_scraping_needed_item_count = c.execute(q)
    no_scraping_needed_item_count = c.fetchone()[0]
    gw.CS_ITEMS_WRITTEN_DIRECT = no_scraping_needed_item_count

    conn.commit()
    # conn.close()
    # gw.SQL_CONN_OPEN -= 1

    for i in range(1,gw.ASYNC_SERIES_CONNECTION+1):
        gw.CS_BOYS_STILL_PLAYING = 0
        pc.printMsg("\n\n..........-------------\/\/\/------\/\/\/------\/\/\/---------------............  Running Async for {} -th time - \t Numer of Async-runs remaining: {} \t\t NOW: {}\n\n".format(i,(gw.ASYNC_SERIES_CONNECTION-i),time.strftime("%H:%M:%S", time.localtime())))
        # asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(asyncFetchAll(ts,i)))
        await asyncFetchAll(conn,ts,i)
        pc.printMsg("\t\t..........-------------\/\/\/------............  {} -th Async Running is done.Sleeping for 10 sec now......ZZZZZZZzzzzzzzzz\t\t NOW: {}\n\n".format(i,time.strftime("%H:%M:%S", time.localtime())))
        time.sleep(10)
    
    conn.close()
    endTime = time.time()
    pc.printSucc("\n\n***************************** All {} Async Content Scraping is Complete. TABLE: {} ******************".format(gw.ASYNC_SERIES_CONNECTION,wc_table))
    print("\n\n")
    table = PrettyTable(['Success (Post ALL series Async Content Scraping)', 'Notation(if any)','Value'])
    table.add_row(['IN : gw.WC_TOTAL_URL_ENTRIES ', '[X] (A+B+C=X)' ,gw.WC_TOTAL_URL_ENTRIES])
    table.add_row(['OUT : ITEMS WRITTEN DIRECT(no scraping needed) ', '[A] (A+B1+B2+C=X)',gw.CS_ITEMS_WRITTEN_DIRECT])
    table.add_row(['OUT : ITEMS SCRAPED WITH ASYNC','[B] (A+B+C=X)' ,gw.CS_ASYNC_ITEM_SCRAPED])
    table.add_row(['TIME TAKEN - ASYNC CONTENT SCRAPING (min)', '-',round((endTime - startTime)/60,2)])
    pc.printSucc(table)

    pc.printErr("------------------------------------------ ERRORS-ASYNC (Written nonetheless, chill) ------------------------------------------------\n")    
    table = PrettyTable(['Failures (Counted as-in last run of Async Content Scraping)','Value'])
    table.add_row(['COUNT. UNREACHABLE URLS in ASYNC ' ,gw.CS_ASYNC_URL_UNREACHABLE])
    table.add_row(['COUNT. TRY/CATCHED SEMA EXCEP. in ASYNC ' ,gw.CS_ASYNC_SEMA_EXCEPTION_ERR])
    pc.printErr(table)
    table.add_row(['TIME TAKEN FOR URL SCRAPING-r (min) ', round((endTime - startTime)/60,2)])
    print("\n")
    pc.printWarn('\t\t\t------------------------->>>>>> [ TimeTaken for All {} Sync Scraping (min) = {} ]\n'.format(gw.ASYNC_SERIES_CONNECTION,round((endTime - startTime),5)/60))
    print("\n\n")


def RunSync(ts):
    """
        NOTE: pdf pages taking a lot of time.Is it right to scrape them still?
    """
    startTime = time.time()
    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    conn = sqlite3.connect(wc_db)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < CONTENT_SCRAPER_SYNC: DB/wc Connection Opened > ---------------------------------------------\n")

    blob_pages = ['.jpg', '.png', '.gif','.mp3', '.mp4']

    q = "select * from " + wc_table + " where length(Content) = 0"
    rows_head = c.execute(q)
    rows = rows_head.fetchall()
    pc.printMsg("\n\n \t ******************************* ITEMS FOR SYNC TO SCRAPE = {} ******************************\n\n".format(len(rows)))
    conn.commit()
    for row in rows:
        t1 = time.time()
        if(len(row[13]) == 0):
            try:
                if row[6][-4:] not in blob_pages:
                    response = web_requests.hitGetWithRetry(row[6],'',False ,2,0.5,30)
                    if response != -1:
                        gw.CS_SYNC_ITEM_SCRAPED += 1
                        res = response.text 
                        row_list = list(row)
                        row_list[13] = res
                        row = tuple(row_list)
                            
                        pc.printWarn("\t <ID = {}><src= {} > [SYNCED SCRAPED] Done................ \t\t TimeTaken = {} \t NOW: {} ".format(row[0],row[1],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
                        q = 'update ' + wc_table + ' set Content = ? where ID = ? and SourceSite = ?'
                        d = (row[13],row[0],row[1])
                        c.execute(q,d)
                        conn.commit()
                        # pc.printSucc(" \t\t ============== <ID= {} ><{}> [SYNCED SCRAPED] INSERTED INTO TABLE =============== ".format(row[0],row[1]))
                    else:
                        gw.CS_SYNC_URL_UNREACHABLE += 1
                        pc.printErr("\t\tXXXXXXXXX [SYNCED SCRAPED]\t SKIPPING... <ID: {}> Totally unable to hit url even in SYNC: {}  \t\t TimeTaken = {} \t NOW: {} ".format(row[0],row[6],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
                else:
                    pc.printMsg("\t\txxxxx [SYNCED SCRAPED]\t... for ID: {} Found BLOB page SYNC. Will use title. URL: {}  \t\t TimeTaken = {} \t NOW: {} ".format(row[0],row[6],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
            except Exception as e:
                gw.CS_SYNC_TRIED_CATCH_EXCEPTION_ERR += 1
                pc.printErr("\t XXXXXXXXXXXXXX [SYNC SCRAPING] XXXX ==>> <ID = {}><src= {} > NOW = {} , \t\t TimeTaken = {} ....Sync Scraping failed too.Will use Title for content... \n \t\t ERROR=> {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime()),round((time.time()-t1),5) ,e))
                # logging.error(traceback.format_exc())
                pass
    endTime = time.time()
    conn.close()
    pc.printMsg("\t -------------------------------------- < CONTENT_SCRAPER_SYNC: DB/wc Connection Closed > ---------------------------------------------\n")
    
    pc.printSucc("\n\n***************************** Sync Content Scraping is Complete. TABLE: {} ******************".format(wc_table))
    print("\n\n")
    table = PrettyTable(['Success (Post Sync Content Scraping)', 'Notation(if any)','Value'])
    table.add_row(['IN : gw.WC_TOTAL_URL_ENTRIES ', '[X] (A+B+C=X)' ,gw.WC_TOTAL_URL_ENTRIES])
    table.add_row(['OUT : ITEMS SCRAPED WITH SYNC','[C] (A+B+C=X)' ,gw.CS_SYNC_ITEM_SCRAPED])
    table.add_row(['TIME TAKEN - SYNC CONTENT SCRAPING (min)', '-',round((endTime - startTime)/60,5)])
    pc.printSucc(table)

    pc.printErr("------------------------------------------ ERRORS-SYNC (Written nonetheless, chill) ------------------------------------------------\n")    
    table = PrettyTable(['Failures (Post Sync Content Scraping)','Value'])
    table.add_row(['COUNT. UNREACHABLE URLS - SYNC ' ,gw.CS_SYNC_URL_UNREACHABLE])
    table.add_row(['COUNT. TRY/CATCHED EXCEP. - SYNC ' ,gw.CS_SYNC_TRIED_CATCH_EXCEPTION_ERR])
    pc.printErr(table)
    print("\n")
    pc.printWarn('\t\t\t------------------------->>>>>> [ TimeTaken for Sync Scraping (min) = {} ]\n'.format(round((endTime - startTime),5)/60))
    print("\n\n")

""" --------------------------------===============  sync-Executor : END ===============--------------------------------  """

#NOTE: cant make async as sql has a DEADLOCK on c.execute(q,d)
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
    conn = sqlite3.connect(wc_db)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < Content Formatter: DB/wc Connection Opened > ---------------------------------------------\n")
    startTime = time.time()
    pc.printWarn("\tRunning ContentFormatter for wc ....... \t NOW: {}".format(time.strftime("%H:%M:%S", time.localtime())))
    pc.printWarn("\t\t. .  .  .  .  .  .  .  .  .  .  .......... Content Formatting Started @Content_Scraper ...........  .  .  .  .  .  .  .  .  .  .  .")

    signal.signal(signal.SIGALRM, timeout_handler)      # timeouts on few function calls, see below
    q = "select * from " + wc_table
    rows_head = c.execute(q)
    rows = rows_head.fetchall()
    conn.commit()
    for row in rows:
        t1 = time.time()
        row_list = list(row)
        if(len(row[13]) != 0):
            gw.CS_ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK += 1
            clean_title = clean_text(row_list[5])
            if len(row_list[13]) == 0 :
                pc.printWarn("\t\t\t\t --------- No content found on cleaning, using Title as Content :(")
                row_list[13] = clean_title
                row_list[12] = clean_title
            else:
                raw_content = row_list[13]
                signal.alarm(200)        # Timeout of 200 sec on function call
                content = clean_title    # if timeout happens, this will be the value of content
                try:
                    content = text_actions.contentfromhtml(raw_content)
                except Exception as exc: 
                    pc.printErr("\t <ID = {}><src= {} > Timeout of 200 sec happened on CONTENT@ContentFromHtml ! ....using Title as content ".format(row[0],row[1]))
                    # pc.printWarn(exc)
                    pass

                signal.alarm(200)        # Timeout of 200 sec on function call
                clean_content = clean_title    # if timeout happens, this will be the value of content
                try:
                    clean_content = clean_text(content)
                except Exception as exc: 
                    pc.printErr("\t <ID = {}><src= {} > Timeout of 200 sec happened on CONTENT@CleanText ! ....using Title as content ".format(row[0],row[1]))
                    # pc.printWarn(exc)
                    pass

                signal.alarm(200)        # Timeout of 200 sec on function call
                weighted_content = clean_title    # if timeout happens, this will be the value of content
                try:
                    weighted_content = text_actions.weightedcontentfromhtml(raw_content) 
                except Exception as exc: 
                    pc.printErr("\t <ID = {}><src= {} > Timeout of 200 sec happened on WEIGHTED_CONTENT@WeightedContentFromHtml ! ....using Title as weightedcontent ".format(row[0],row[1]))
                    # pc.printWarn(exc)
                    pass

                signal.alarm(200)        # Timeout of 200 sec on function call
                clean_weighted_content = clean_title    # if timeout happens, this will be the value of content
                try:
                    clean_weighted_content = clean_text(weighted_content)
                except Exception as exc: 
                    pc.printErr("\t <ID = {}><src= {} > Timeout of 200 sec happened on WEIGHTED_CONTENT@CleanText ! ....using Title as weightedcontent ".format(row[0],row[1]))
                    # pc.printWarn(exc)
                    pass

                signal.alarm(200)        # Timeout of 200 sec on function call
                url_string_text = ''    # if timeout happens, this will be the value of content
                try:
                    url_string_text = getUrlString(raw_content)
                except Exception as exc: 
                    pc.printErr("\t <ID = {}><src= {} > Timeout of 200 sec happened on URL_STRING@getUrlString ! ....using empty str as url_string_text ".format(row[0],row[1]))
                    # pc.printWarn(exc)
                    pass

                row_list[13] = clean_content
                row_list[12] = clean_weighted_content + " " + url_string_text + " " + clean_title

            row = tuple(row_list)
                
            pc.printWarn("\t <ID = {}><src= {} > [Content Formatting] Done................ \t\t TimeTaken = {} \t NOW: {}".format(row[0],row[1],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
            content = row[13]  
            q = 'update ' + wc_table + ' set Content = ?, WeightedContent = ?  where ID = ? and SourceSite = ?'
            d = (row[13], row[12],row[0],row[1])
            c.execute(q,d)
            conn.commit()
            # pc.printSucc(" \t\t ============== <ID= {} ><{}> [Content Formatting]-with content INSERTED INTO TABLE =============== ".format(row[0],row[1]))
        else: #No content
            gw.CS_ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT += 1
            pc.printMsg("\t <ID = {}><src= {} > [Content Formatting] No content.Using title finally................ \t\t TimeTaken = {} \t NOW: {}".format(row[0],row[1],round((time.time()-t1),5),time.strftime("%H:%M:%S", time.localtime())))
            clean_title = clean_text(row_list[5])
            content = clean_title 
            q = 'update ' + wc_table + ' set Content = ?, WeightedContent = ?  where ID = ? and SourceSite = ?'
            d = (content, content,row[0],row[1])
            c.execute(q,d)
            conn.commit()
            # pc.printSucc(" \t\t ============== <ID= {} ><{}> [Content Formatting]-without content INSERTED INTO TABLE =============== ".format(row[0],row[1]))
    endTime = time.time()
    
    conn.close()
    pc.printMsg("\t -------------------------------------- < Content Formatter: DB/wc Connection Closed > ---------------------------------------------\n")

    pc.printSucc("\n\n***************************** Content Formatting is Complete. TABLE: {} ******************".format(wc_table))
    print("\n\n")
    table = PrettyTable(['Success (Post Content Formatting)', 'Notation(if any)','Value'])
    table.add_row(['IN : gw.WC_TOTAL_URL_ENTRIES ', '[X] (A+B+C=X)' ,gw.WC_TOTAL_URL_ENTRIES])
    table.add_row(['OUT : ITEMS PUT IN WITH SCRAPED CONTENT','[P] (P+Q=X)' ,gw.CS_ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK])
    table.add_row(['OUT : x--ITEMS PUT IN WITH TITLE AS CONTENT--x','[Q] (P+Q=X)' ,gw.CS_ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT])
    table.add_row(['TIME TAKEN - CONTENT FORMATTING (min)', '-',round((endTime - startTime)/60,5)])
    pc.printSucc(table)

    print("\n")
    pc.printWarn('\t\t\t------------------------->>>>>> [ TimeTaken for Content Formatting (min) = {} ]\n'.format(round((endTime - startTime),5)/60))
    print("\n\n")


def run(ts):
    nest_asyncio.apply()        #  to be able to run async loop from aj async loop

    wc_table = 'wc_' + str(int(ts))
    pc.printMsg('@[{}] >>>>>> Started Content-scraper(ASYNC) .......[Sema = {}, conn_lim ={}]............ => TABLE: {}\n'.format(datetime.fromtimestamp(ts),gw.SEMAPHORE_COUNT,gw.CONNECTION_COUNT,wc_table))

    startTime = time.time()

    """ scrape content in async """
    asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(RunAsync(ts)))
    time.sleep(10)
    """ scrape remaining items with sync """
    RunSync(ts) 

    """ formatting everything in the end-done in sync """
    time.sleep(10)
    ContentFormatting(ts) 

    endTime = time.time()
    pc.printSucc("\n\n\n\n\n****************** Content Scraping is Complete , TABLE: {} ********************".format(wc_table))   
    print("\n\n")
    table = PrettyTable(['Entities (Post Content Scraping-all)', 'Notation(if any)','Value'])
    
    table.add_row(['IN : gw.WC_TOTAL_URL_ENTRIES ', '[X] (A+B+C=X)' ,gw.WC_TOTAL_URL_ENTRIES])
    table.add_row(['CS_OUT : ITEMS SCRAPED WITH ASYNC','[A] (A+B+C=X)' ,gw.CS_ASYNC_ITEM_SCRAPED])
    table.add_row(['CS_OUT : ITEMS WRITTEN DIRECT(no scraping needed) ', '[B] (A+B+C=X)',gw.CS_ITEMS_WRITTEN_DIRECT])
    table.add_row(['CS_OUT : ITEMS SCRAPED WITH SYNC','[C] (A+B+C=X)' ,gw.CS_SYNC_ITEM_SCRAPED])
    table.add_row(['CF_OUT : ITEMS PUT IN WITH SCRAPED CONTENT','[P] (P+Q=X)' ,gw.CS_ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK])
    table.add_row(['CF_OUT : x--ITEMS PUT IN WITH TITLE AS CONTENT--x','[Q] (P+Q=X)' ,gw.CS_ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT])
    
    pc.printSucc(table)

    pc.printErr("\n\n------------------------------------------ ERRORS (Written nonetheless, chill) ------------------------------------------------\n")    
    table = PrettyTable(['Failures (Post Content Scraping-all)','Value'])
    table.add_row(['COUNT. UNREACHABLE URLS - ASYNC ' ,gw.CS_ASYNC_URL_UNREACHABLE])
    table.add_row(['COUNT. TRY/CATCHED SEMA EXCEP. - ASYNC ' ,gw.CS_ASYNC_SEMA_EXCEPTION_ERR])
    table.add_row(['COUNT. UNREACHABLE URLS - SYNC ' ,gw.CS_SYNC_URL_UNREACHABLE])
    table.add_row(['COUNT. TRY/CATCHED EXCEP. - SYNC ' ,gw.CS_SYNC_TRIED_CATCH_EXCEPTION_ERR])
    pc.printErr(table)
    print("\n")
    pc.printWarn('\t\t\t\t------------------------->>>>>> [ Time Taken(min) = {} ]\n\n\n\n\n\n'.format(round((endTime - startTime),5)/60))
    print("\n\n\n\n")
