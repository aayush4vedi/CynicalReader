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

from utilities import csv_functions, text_actions, web_requests
from utilities import print_in_color as pc

SEMAPHORE_COUNT = 100
CONNTECTION_COUNT = 100

ENTRIES_TO_BE_WRITTEN = 0                               # total entries in original file
WRITTEN_ENTRIES_ASYNC_DIRECT = 0                        # for every entry written- just copied from prev file
WRITTEN_ENTRIES_ASYNC_SCRAPED = 0                       # for every entry written- fetched by scraping
ERR_ASYNC_NO_CONTENT_IN_SCRAPING = 0                    # when no url after scraping,dont waste the precious article
ERR_ASYNC_ON_URL_ERROR = 0                              # when unable to hit url,dont waste the precious article
ERR_ASYNC_TRIED_ERR = 0                                 # any other error(try/catch) in scraping,dont waste the precious article

ASYNC_ENTRIES_TO_BE_SCRAPED = 0                         # Just keeping count of how many requests have been spawned
BOYS_RETURNED_HOME_ALIVE = 0                         
BOYS_RETURNED_HOME_DEAD = 0                         

WRITTEN_ENTRIES_SYNC = 0
SKIPPED_SYNC = 0
FAILED_SYNC = 0



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

import string
import re 
from urlextract import URLExtract

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from readability import Document
from bs4 import BeautifulSoup


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

"""
    given raw text; finds all the useful words in urls; stiches them into a string & retursn that string.
    Mainly to be put in weightedcontent
"""
def getUrlString(intxt):
    common_url_words = ['http', 'https', 'www', 'com', 'html']
    extractor = URLExtract()
    urls = extractor.find_urls(intxt)
    urlstring = ' '.join(urls)
    clean_url_string = re.sub('[^A-Za-z0-9]+', ' ', urlstring)
    clean_url_list = [w for w in clean_url_string.split()]
    new_list = [word for word in clean_url_list if (word not in common_url_words and word.isalpha())]   # remove numbers from url
    return ' '.join(new_list)


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
    sleep_time = 5
    # TIMEOUT = ClientTimeout(total=20)
    TIMEOUT = 20
    
    while retry_cnt > 0 and status != 200:
        async with session.get(row[6],ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH), timeout = TIMEOUT) as response: 
            res = await response.text()
            # res = await response.content.read()
            # res = await text_actions.clean_text(str(response.content.read()))
            res = text_actions.clean_text(str(res))
            # res = res.encode('utf8', 'ignore').decode('utf8', 'ignore')                   #FIXME: not working
            status = response.status
            if( status == 200 and len(res) != 0):
                pc.printSucc("\t\t <ID = {}><src= {} > ============== #Scraped ....... \t NOW: {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime())))
                row_list = list(row)
                row_list[12] = text_actions.weightedcontentfromhtml(res) 
                row_list[13] = text_actions.contentfromhtml(res)
                # for i in range(len(row_list)):
                #     row_list[i] = row_list[i].decode("utf-8", "ignore")

                row = tuple(row_list)
                # pc.printWarn("\t <ID = {}><src= {} > sleeping for 0.0001 second ZZZZZZzzzzzzzzzzzz................. NOW: {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime())))
                # time.sleep(0.001)
                if(len(row[13]) == 0):
                    global ERR_ASYNC_NO_CONTENT_IN_SCRAPING
                    ERR_ASYNC_NO_CONTENT_IN_SCRAPING += 1
                    pc.printErr("\t\t xxxxxxxxxxxxxxxxxxx SKIPPING  for <ID = {}><src= {} > As No Content even after scraping xxxxxxxxxxxxxxxxxxxxxxxx\n".format(row[0],row[1]))
                return row
            else:
                retry_cnt -= 1
                pc.printWarn("\t x---------------- <ID = {}><src= {} > Unable to hit URL(ERR_CODE={}): {}.........  Sleeping for {} Retries remaining = {} -------------x".format(row[0],row[1],status,row[6][:25], sleep_time, retry_cnt))
                await asyncio.sleep(sleep_time)

    pc.printErr("\t\txxxxx  For <ID = {}><src= {} >Totally unable to hit url.... using Title for Content & WeightedContent : {} ".format(row[0],row[1],row[6]))
    global ERR_ASYNC_ON_URL_ERROR 
    ERR_ASYNC_ON_URL_ERROR += 1
    pc.printMsg(" \t\t\t ============== [Unreachable URL] Will write anyways. <ID = {}><src= {} > =============== ".format(row[0],row[1]))
    return row




async def semaphoreSafeFetch(sem, row, session):
    """
        Simple puts check for semaphore count
    """
    global BOYS_RETURNED_HOME_ALIVE
    global BOYS_RETURNED_HOME_DEAD
    # async with sem:
    # try:
    #     return await fetchWithRetry(row, session)
    #     BOYS_RETURNED_HOME_ALIVE += 1
    #     print(" \t\t\t\t\t\t\t\t\t\t\t\t BOYS_RETURNED_HOME_ALIVE = {}".format(BOYS_RETURNED_HOME_ALIVE))
    # except Exception as e:
    #     BOYS_RETURNED_HOME_DEAD += 1
    #     print(" \t\t\t\t\t\t\t\t\t\t\t\t BOYS_RETURNED_HOME_DEAD = {}".format(BOYS_RETURNED_HOME_DEAD))
    #     #TODO: delete this
    #     if str(e).find("codec can't decode byte") != -1:
    #         print(" \t\t\t row: {}".format(row))

    #     # This error is mainly because of:
    #     ## 1. [nodename nor servname provided, or not known]
    #     ## 2. [Too many open files] => UPDATE: got fixed with using sqlite
    #     pc.printErr("\t======= XXXXXXXX ERROR XXXXXX ======>> <ID = {}><src= {} > NOW = {} Scraping failed. Using Title for Content.... \n \t\t ERROR=> {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime()) ,e))
    #     logging.error(traceback.format_exc())
    #     if len(row[13]) == 0:   
    #         row_list = list(row)
    #         row_list[12] = row_list[5]
    #         row_list[13] =  row_list[5]
    #         row = tuple(row_list)
    #     global ERR_ASYNC_TRIED_ERR
    #     ERR_ASYNC_TRIED_ERR += 1
    #     pc.printMsg(" \t\t\t============== [Tried Catch] Done Writing into csv for <ID = {}><src= {} > =============== ".format(row[0],row[1]))
    #     pass
    # return row              #NOTE: this fucker!!!
    async with sem:
        try:
            return await fetchWithRetry(row, session)
            BOYS_RETURNED_HOME_ALIVE += 1
            print(" \t\t\t\t\t\t\t\t\t\t\t\t BOYS_RETURNED_HOME_ALIVE = {}".format(BOYS_RETURNED_HOME_ALIVE))
        except Exception as e:
            BOYS_RETURNED_HOME_DEAD += 1
            print(" \t\t\t\t\t\t\t\t\t\t\t\t BOYS_RETURNED_HOME_DEAD = {}".format(BOYS_RETURNED_HOME_DEAD))
            # #TODO: delete this
            # if str(e).find("codec can't decode byte") != -1:
            #     print(" \t\t\t row: {}".format(row))

            # This error is mainly because of:
            ## 1. [nodename nor servname provided, or not known]
            ## 2. [Too many open files] => UPDATE: got fixed with using sqlite
            pc.printErr("\t======= XXXXXXXX ERROR XXXXXX ======>> <ID = {}><src= {} > NOW = {} Scraping failed. Using Title for Content.... \n \t\t ERROR=> {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime()) ,e))
            logging.error(traceback.format_exc())
            if len(row[13]) == 0:   
                row_list = list(row)
                row_list[12] = row_list[5]
                row_list[13] =  row_list[5]
                row = tuple(row_list)
            global ERR_ASYNC_TRIED_ERR
            ERR_ASYNC_TRIED_ERR += 1
            pc.printMsg(" \t\t\t============== [Tried Catch] Done Writing into csv for <ID = {}><src= {} > =============== ".format(row[0],row[1]))
            pass
    return row              #NOTE: this fucker!!!


async def asyncFetchAll(ts):
    """
        INPUT: ts (format: 1598692058.887741)
    """
    global CONNTECTION_COUNT, SEMAPHORE_COUNT

    tasks = []
    sem = asyncio.Semaphore(SEMAPHORE_COUNT)

    #==========================init connection 
    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < CONTENT_SCRAPER: DB Connection Opened > ---------------------------------------------\n")
    stratTime = time.time()

    # """ Initialize the output file """
    # headers = ['ID', 'SourceSite', 'ProcessingDate','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content']
    # csv_functions.creteCsvFile(csv_out,headers)

    global ENTRIES_TO_BE_WRITTEN
    global WRITTEN_ENTRIES_ASYNC_SCRAPED
    global WRITTEN_ENTRIES_ASYNC_DIRECT
    global ASYNC_ENTRIES_TO_BE_SCRAPED

    connector = TCPConnector(limit=CONNTECTION_COUNT,family=socket.AF_INET,verify_ssl=False)
    # connector = TCPConnector(limit=CONNTECTION_COUNT)
    # connector = ProxyConnector.from_url('http://user:password@127.0.0.1:1080')
    async with ClientSession(headers={'Connection': 'keep-alive'},connector=connector) as session:
        q = "select * from " + wc_table
        rows_head = c.execute(q)
        rows = rows_head.fetchall()
        for row in rows:
            """
                ============= row is an array with indices: 
                ID(0),SourceSite(1),ProcessingDate(2),ProcessingEpoch(3),CreationDate(4),Title(5),Url(6),
                SourceTags(7),ModelTags(8),NumUpvotes(9),NumComments(10),PopI(11),WeightedContent(12),Content(13)
            """
            ENTRIES_TO_BE_WRITTEN += 1
            if(len(row[13]) != 0):
                pc.printWarn("\t <ID = {}><src= {} > [NO SCRAPING] Content already exists............... NOW: {}".format(row[0],row[1],time.strftime("%H:%M:%S", time.localtime())))
                clean_content = row[13]     #Already cleaned in url_scraper
                url_strings_content = getUrlString(row[13])
                clean_title = clean_text(row[5])
                clean_weighted_content = clean_text(row[12]) + " " + clean_title + " " + url_strings_content

                query = 'update ' + wc_table + ' set Content = ? , WeightedContent = ? where ID = ? and SourceSite = ?'
                data = (clean_content, clean_weighted_content,row[0],row[1])
                c.execute(query,data)
                WRITTEN_ENTRIES_ASYNC_DIRECT += 1
                pc.printSucc(" \t\t ============== <ID= {} ><{}> [Direct] INSERTED INTO TABLE =============== ".format(row[0],row[1]))
            elif(row[5] and row[6]): # else ignore the entry
                ASYNC_ENTRIES_TO_BE_SCRAPED += 1
                print("\t\t\t\t\t SENT...... SENT_COUNT = {}".format(ASYNC_ENTRIES_TO_BE_SCRAPED))
                # if(ASYNC_ENTRIES_TO_BE_SCRAPED%100 == 0):
                #     pc.printMsg("\t\t\t.......................zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz <NAP TIME> for 5 sec After 100 async-requests while content scraping #ZarooriHaiJi zzzzzzzzzzzzzzz.......................")
                #     time.sleep(5)
                task = asyncio.ensure_future(semaphoreSafeFetch(sem, row, session))
                tasks.append(task)

        responses = await asyncio.gather(*tasks)
        for row in responses:
            if row:
                clean_content = clean_text(row[13])
                url_strings_content = getUrlString(row[13])
                clean_title = clean_text(row[5])
                clean_weighted_content = clean_text(row[12]) + " " + clean_title + " " + url_strings_content
                query = 'update ' + wc_table + ' set Content = ? , WeightedContent = ? where ID = ? and SourceSite = ?'
                data = (clean_content, clean_weighted_content,row[0],row[1])
                c.execute(query,data)
                WRITTEN_ENTRIES_ASYNC_SCRAPED += 1
                pc.printSucc(" \t\t ============== <ID= {} ><{}> [Scraped] INSERTED INTO TABLE =============== ".format(row[0],row[1]))
        
    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < CONTENT_SCRAPER: DB Connection Closed > ---------------------------------------------\n")

        
""" ===============  Async-Executor Helpers: END ===============  """


""" ===============  (Not used)Async-Executor Checker: START ===============  """

def cleanNcheckAsyncOutput(csv_in, csv_out):
    """
        Analyse the created & input fles 
        Also, cleans Content & WeightedContent-> put in new file, delete the old one
        Variables:
            * NO_LINES_IN_INPUT_CSV
            * NO_LINES_IN_OUTPUT_CSV
            * NO_LINES_IN_OUTPUT_WITHOUT_TITLE
            * NO_LINES_IN_OUTPUT_WITHOUT_URL
            * NO_LINES_IN_OUTPUT_WITHOUT_CONTENT
    """

    f = open(csv_in,"r+")
    f.fseek(0)                     # reach to first line
    reader = csv.reader(f)
    NO_LINES_IN_INPUT_CSV = len(list(reader))


    """ Now check and create new "cleaned" file """


    headers = ['ID', 'SourceSite', 'ProcessingDate','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content']
    csv_final_out = os.path.join("F",csv_out)
    csv_functions.creteCsvFile(csv_final_out,headers)

    pc.prCyan(" ========================== NOW CREATING FINAL OUTPUT FILE: {} ===========================".format(csv_final_out))

    line_count = 0
    with open(csv_out, mode='r') as r , open(csv_final_out, 'a+', newline='') as f:
        reader = csv.DictReader(r)
        writer = csv.writer(f)
        NO_LINES_IN_OUTPUT_CSV = 0
        for row in reader:
            if( line_count == 0):       # skipping headers
                line_count += 1
            else:
                url_string_content = text_actions.getUrlString(row[13])
                content = text_actions.clean_text(row[13])
                weighted_content = text_actions.clean_text(row[12])
                entry = [
                    row[0],
                    row[1],
                    row["ProcessingDate"],
                    row["ProcessingEpoch"],
                    row["CreationDate"],
                    row[5],
                    row[6],
                    row["SourceTags"],
                    row["ModelTags"],
                    row["NumUpvotes"],
                    row["NumComments"],
                    row["PopI"],
                    weighted_content + url_string_content,
                    content,
                ]
                writer.writerow(entry)
                NO_LINES_IN_OUTPUT_CSV += 1
                if(len(row[5]) == 0):
                    NO_LINES_IN_OUTPUT_WITHOUT_TITLE += 1
                if(len(row[6]) == 0):
                    NO_LINES_IN_OUTPUT_WITHOUT_URL += 1
                if(len(row[13]) == 0):
                    NO_LINES_IN_OUTPUT_WITHOUT_CONTENT += 1


    pc.printWarn("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~ Analysis ~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    pc.printWarn("|\t NO_LINES_IN_INPUT_CSV                 \t | \t  {}  \t|".format(NO_LINES_IN_INPUT_CSV))
    pc.printWarn("|\t NO_LINES_IN_OUTPUT_CSV                \t | \t  {}  \t|".format(NO_LINES_IN_OUTPUT_CSV))
    pc.printWarn("|\t NO_LINES_IN_OUTPUT_WITHOUT_TITLE      \t | \t  {}  \t|".format(NO_LINES_IN_OUTPUT_WITHOUT_TITLE))
    pc.printWarn("|\t NO_LINES_IN_OUTPUT_WITHOUT_URL        \t | \t  {}  \t|".format(NO_LINES_IN_OUTPUT_WITHOUT_URL))
    pc.printWarn("|\t NO_LINES_IN_OUTPUT_WITHOUT_CONTENT    \t | \t  {}  \t|".format(NO_LINES_IN_OUTPUT_WITHOUT_CONTENT))


""" ===============  Async-Executor Checker: END ===============  """


""" ===============  (Being used )Async-Executor : START ===============  """


def RunAsync(ts):
    """
        Pick wc-db's table mapped with `ts` and scrapes (useful) "clean" Content & WeightedContent from url- ASYNCLY
        * NOTE:
            * If conent is already present in the table, "clean" it too & append the newly scraped content to it.
            * FIRST RUN: time = 17 hours, data = 12 MB, #entries = 6.5k
        Input: ts (format: 1598692058.887741)
    """
    global CONNTECTION_COUNT, SEMAPHORE_COUNT
    wc_table = 'wc_' + str(int(ts))
    pc.printMsg('@[{}] >>>>>> Started Content-scraper(ASYNC) .......[Sema = {}, conn_lim ={}]............ => TABLE: {}\n'.format(datetime.fromtimestamp(ts),SEMAPHORE_COUNT,CONNTECTION_COUNT,wc_table))

    stratTime = time.time()
    # csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    # csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'

    # Run the async job
    asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(asyncFetchAll(ts)))

    endTime = time.time()
    pc.printSucc("\n****************** (Async)Content Scraping is Complete , TABLE: {} ********************".format(wc_table))   
    
    pc.printMsg("\n--------------------------------------------------------------------------------------------------------------------------------")   
    pc.printMsg("|\t\t IN : Total Entries in Url-Scraped Output Table                   \t\t  | \t\t {} \t\t|".format(ENTRIES_TO_BE_WRITTEN)) 
    pc.printMsg("|\t\t OUT: WRITTEN_ENTRIES_ASYNC_DIRECT(content exists)                \t\t  | \t\t {} \t\t|".format(WRITTEN_ENTRIES_ASYNC_DIRECT)) 
    pc.printMsg("|\t\t OUT: WRITTEN_ENTRIES_ASYNC_SCRAPED(scraped entries)              \t\t  | \t\t {} \t\t|".format(WRITTEN_ENTRIES_ASYNC_SCRAPED)) 
    pc.printErr("\n\n------------------ ERRORS In Scraping (Written nonetheless; counted in  WRITTEN_ENTRIES_ASYNC_SCRAPED) --------------------------\n")    
    pc.printMsg("=================================================================================================================================")    
    pc.printErr("|\t\t ERR_ASYNC_NO_CONTENT_IN_SCRAPING(url hit;not content-written )   \t\t  | \t\t {} \t\t|".format(ERR_ASYNC_NO_CONTENT_IN_SCRAPING)) 
    pc.printErr("|\t\t ERR_ASYNC_ON_URL_ERROR(url not hit)                              \t\t  | \t\t {} \t\t|".format(ERR_ASYNC_ON_URL_ERROR)) 
    pc.printErr("|\t\t ERR_ASYNC_TRIED_ERR(other try/catch errs)                        \t\t  | \t\t {} \t\t|".format(ERR_ASYNC_TRIED_ERR)) 
    pc.printMsg("---------------------------------------------------------------------------------------------------------------------------------\n") 
    pc.printWarn('\t\t\t\t------------------------->>>>>> [ Semaphore Count = {}, Tcp connector limit ={} ]\n'.format(SEMAPHORE_COUNT,CONNTECTION_COUNT))
    pc.printWarn('\t\t\t\t------------------------->>>>>> [ Time Taken(sec) = {} ]\n'.format(int(endTime - stratTime)))

    # Run the analysis
    # cleanNcheckAsyncOutput(csv_src_file, csv_dest_file)   


""" --------------------------------===============  Async-Executor : END ===============--------------------------------  """


""" --------------------------------=============== (Not in use) sync-Executor : START ===============--------------------------------  """


def RunSync(ts):
    """
        Pick wc-db's table mapped with `ts` and scrapes (useful) "clean" Content & WeightedContent from url.
        * NOTE:
            * If conent is already present in the table, "clean" it too & append the newly scraped content to it.
            * FIRST RUN: time = 17 hours, data = 12 MB, #entries = 6.5k
        Input: ts (format: 1598692058.887741)
        * TODO: if unable to hit url, dont discard the valuable article, but Content = Title, WeightedContent = Title
    """
    pc.printMsg('@[{}] >>>>>> Started Content-scraper(SYNC) ................... => FILENAME: {}\n'.format(datetime.fromtimestamp(ts),'dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'))

    csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'_sync_wc.csv'
    index = 1
    headers = ['ID', 'SourceSite', 'ProcessingDate','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content']
    csv_functions.creteCsvFile(csv_dest_file,headers)

    f = csv.writer(open(csv_dest_file, "w"))          # Flush the old file
    f.writerow(['ID', 'SourceSite', 'ProcessingDate','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content'])
    with open(csv_src_file, mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Headers are {", ".join(row)}')
                line_count += 1
            #CHECK1(pre scraping): if (content != NULL) => no scraping, just put it in as is
            if(len(row[13]) != 0):
                pc.printWarn("\t <ID = {} > [NO SCRAPING] Content already exists....putting as it is............. NOW: {}".format(row[0],time.strftime("%H:%M:%S", time.localtime())))
                entry = [
                        row[0],
                        row[1],
                        row["ProcessingDate"],
                        row["ProcessingEpoch"],
                        row["CreationDate"],
                        row[5],
                        row[6],
                        row["SourceTags"],
                        row["ModelTags"],
                        row["NumUpvotes"],
                        row["NumComments"],
                        row["PopI"],
                        text_actions.clean_text(row[5] + row[12]) + text_actions.getUrlString(row[13]),  #add the url-words too
                        text_actions.clean_text(row[13]) + text_actions.getUrlString(row[13])
                        ]
                global WRITTEN_ENTRIES_SYNC
                WRITTEN_ENTRIES_SYNC += 1
                f = csv.writer(open(csv_dest_file, "a"))  
                f.writerow(entry)
            #CHECK2(pre scraping): if(url == NULL)=>discard
            #CHECK3(pre scraping): if (row[5]==NULL)=>discard
            elif ((len(row[6]) != 0)and(len(row[5]) != 0)):
                pc.printWarn("\t <ID = {} > [SCRAPING BEGIN] sleeping for 0.0001 second ZZZZZZzzzzzzzzzzzz................. NOW: {}".format(row[0],time.strftime("%H:%M:%S", time.localtime())))
                time.sleep(0.0001) 
                try:
                    # response = web_requests.hitGetWithRetry(url,TIMEOUT=10)
                    response = web_requests.hitGetWithRetry(row[6],'',False ,2,0.5,60)
                    # if response.status_code == 200:
                    if response != -1:
                        # content = text_actions.contentfromhtml(response)  #NOTE: for sync
                        content = text_actions.contentfromhtml(response.text)  #NOTE: for Async
                        urlstrings = text_actions.getUrlString(content)
                        content += urlstrings #add the url-words too
                        # weightedcontent = text_actions.weightedcontentfromhtml(response.text) + row[5] + urlstrings #add the url-words too      #NOTE: for sync
                        weightedcontent = text_actions.weightedcontentfromhtml(response.text) + row[5] + urlstrings #add the url-words too        #NOTE: for async
                        line_count += 1
                        #CHECK1(post scraping): if (content == null)&&(row[5] != null)<already checked abouve>=> row[13] = clean_text(row[5]) AND row[12] = clean_text(row[5])
                        if(len(content) == 0):
                            content = row[5]
                            weightedcontent = row[5]
                        else:
                            entry = [
                                row[0],
                                row[1],
                                row["ProcessingDate"],
                                row["ProcessingEpoch"],
                                row["CreationDate"],
                                row[5],
                                row[6],
                                row["SourceTags"],
                                row["ModelTags"],
                                row["NumUpvotes"],
                                row["NumComments"],
                                row["PopI"],
                                text_actions.clean_text(weightedcontent) ,
                                text_actions.clean_text(content)
                                ]
                            
                        f = csv.writer(open(csv_dest_file, "a"))          
                        f.writerow(entry)
                        pc.printMsg("\t\t <ID = {} > ============== Scraping Done....... \t NOW: {}".format(row[0],time.strftime("%H:%M:%S", time.localtime())))
                    else:
                        global SKIPPED_SYNC
                        SKIPPED_SYNC += 1
                        pc.printErr("\t\txxxxx SKIPPING... for ID: {} Unable to hit url: {} , ".format(row[0],row[6]))
                except Exception as e:
                    global FAILED_SYNC
                    FAILED_SYNC += 1
                    pc.printErr("\t======= XXXXXXXX ERROR XXXXXX ======>> ID= {} NOW = {} Skipping...Failed due to: \n \t\t ERROR {}".format(row[0],time.strftime("%H:%M:%S", time.localtime()) ,e))
                    pass
    pc.printMsg("\n****************** Content Scraping is Complete , FILENAME: {} ********************\n".format('dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'))    
    pc.printMsg("\n----------------------------------------------------------------------------------\n")   
    pc.printMsg("|\tWRITTEN_ENTRIES_SYNC \t  | \t {} \t|".format(WRITTEN_ENTRIES_SYNC)) 
    pc.printMsg("|\tSKIPPED_SYNC          \t | \t {} \t|".format(SKIPPED_SYNC)) 
    pc.printMsg("|\tFAILED_SYNC           \t | \t {} \t|".format(FAILED_SYNC)) 
    pc.printMsg("\n----------------------------------------------------------------------------------\n")    
    



""" --------------------------------===============  sync-Executor : END ===============--------------------------------  """








""" ERROR ISSUES in Content Scraper
    * xxxxxxxxxxxxxxxxxxx SKIPPING  for <ID = 115><src= r/computerscience > As No Title xxxxxxxxxxxxxxxxxxxxxxxx
    * ERROR 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte
    * ERROR Cannot connect to host {x} ssl:<ssl.SSLContext object at 0x135d786c0> [nodename nor servname provided, or not known]
    * ERROR Cannot connect to host {x} ssl:<ssl.SSLContext object at 0x135d786c0> [Too many open files]
"""