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

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from utilities import csv_functions, text_actions, web_requests
from utilities import print_in_color as pc

ENTRIES_TO_BE_WRITTEN = 0                               # total entries in original file
WRITTEN_ENTRIES_ASYNC_DIRECT = 0                        # for every entry written- just copied from prev file
WRITTEN_ENTRIES_ASYNC_SCRAPED = 0                       # for every entry written- fetched by scraping
WRITTEN_ENTRIES_ASYNC_NO_CONTENT_IN_SCRAPING = 0        # when no url after scraping,dont waste the precious article
WRITTEN_ENTRIES_ASYNC_ON_URL_ERROR = 0                  # when unable to hit url,dont waste the precious article
WRITTEN_ENTRIES_ASYNC_TRIED_ERR = 0                     # any other error(try/catch) in scraping,dont waste the precious article
FAILED_ASYNC = 0                                        # other failures

# total entries written after `content_scraper` is run =   WRITTEN_ENTRIES_ASYNC_DIRECT + WRITTEN_ENTRIES_ASYNC_SCRAPED + WRITTEN_ENTRIES_ASYNC_ON_URL_ERROR + WRITTEN_ENTRIES_ASYNC_NO_CONTENT_IN_SCRAPING + WRITTEN_ENTRIES_ASYNC_TRIED_ERR

WRITTEN_ENTRIES_SYNC = 0
SKIPPED_SYNC = 0
FAILED_SYNC = 0


OPEN_CSV = 0

""" =============== Async-Executor Helpers: START ===============  """

async def fetchWithRetry(row, session, csv_out):
    """
        Hits ulr(with retires):
        * if status == 200:
            put content into csv
        * if still unable to hit after retries: Content = Title , WeightedContent = Title
    """


    status = 400
    retry_cnt = 2
    sleep_time = 10
    TIMEOUT = 10

    while retry_cnt > 0 and status != 200:
        async with session.get(row["Url"],ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH), timeout = TIMEOUT) as response: 
            res = await response.text()
            status = response.status
            if( status == 200 and len(res) != 0):
                pc.printSucc("\t\t <ID = {}><src= {} > ============== Scraping Done....... \t NOW: {}".format(row["ID"],row["SourceSite"],time.strftime("%H:%M:%S", time.localtime())))
                urlstrings = text_actions.getUrlString(row["Content"])
                row["WeightedContent"] = text_actions.weightedcontentfromhtml(res) + row["Title"] + urlstrings
                row["Content"] = text_actions.contentfromhtml(res)  + urlstrings
                # pc.printWarn("\t <ID = {}><src= {} > sleeping for 0.0001 second ZZZZZZzzzzzzzzzzzz................. NOW: {}".format(row["ID"],row["SourceSite"],time.strftime("%H:%M:%S", time.localtime())))
                # time.sleep(0.001)
                if (len(row["Title"]) !=0):
                    if len(row["Content"]) == 0:          
                        row["WeightedContent"] = row["Title"]
                        row["Content"] = row["Title"]
                    await write_result(csv_out,row)
                    global WRITTEN_ENTRIES_ASYNC_SCRAPED
                    WRITTEN_ENTRIES_ASYNC_SCRAPED += 1
                    pc.printMsg(" \t\t ============== [Scraped] Done Writing into csv for <ID = {}><src= {} > =============== ".format(row["ID"],row["SourceSite"]))
                else:
                    global WRITTEN_ENTRIES_ASYNC_NO_CONTENT_IN_SCRAPING
                    WRITTEN_ENTRIES_ASYNC_NO_CONTENT_IN_SCRAPING += 1
                    pc.printErr("\t\t xxxxxxxxxxxxxxxxxxx SKIPPING  for <ID = {}><src= {} > As No Title xxxxxxxxxxxxxxxxxxxxxxxx\n".format(row["ID"],row["SourceSite"]))
                return row
            else:
                retry_cnt -= 1
                pc.printWarn("\t x---------------- <ID = {}><src= {} > Unable to hit URL(ERR_CODE={}): {}.........  Sleeping for {} Retries remaining = {} -------------x".format(row["ID"],row["SourceSite"],status,row["Url"][:25], sleep_time, retry_cnt))
                await asyncio.sleep(sleep_time)
    pc.printErr("\t\txxxxx  For <ID = {}><src= {} >Totally unable to hit url.... using Title for Content & WeightedContent : {} ".format(row["ID"],row["SourceSite"],row["Url"]))
    if len(row["Content"]) == 0:          
        row["WeightedContent"] = row["Title"]
        row["Content"] =  row["Title"]
    await write_result(csv_out,row)
    global WRITTEN_ENTRIES_ASYNC_ON_URL_ERROR 
    WRITTEN_ENTRIES_ASYNC_ON_URL_ERROR += 1
    pc.printMsg(" \t\t\t ============== [Unreachable URL] Done Writing into csv for <ID = {}><src= {} > =============== ".format(row["ID"],row["SourceSite"]))
    return row



async def semaphoreSafeFetch(sem, row, session,csv_out):
    """
        Simple puts check for semaphore count
    """
    async with sem:
        try:
            return await fetchWithRetry(row, session,csv_out)
        except Exception as e:
            global FAILED_ASYNC
            FAILED_ASYNC += 1
            # This error is mainly because of:
            ## 1. [nodename nor servname provided, or not known]
            ## 2. [Too many open files]
            pc.printErr("\t======= XXXXXXXX ERROR XXXXXX ======>> <ID = {}><src= {} > NOW = {} Scraping failed. Using Title for Content.... \n \t\t ERROR {}".format(row["ID"],row["SourceSite"],time.strftime("%H:%M:%S", time.localtime()) ,e))
            if len(row["Content"]) == 0:          
                row["WeightedContent"] = row["Title"]
                row["Content"] =  row["Title"]
            await write_result(csv_out,row)
            global WRITTEN_ENTRIES_ASYNC_TRIED_ERR
            WRITTEN_ENTRIES_ASYNC_TRIED_ERR += 1
            pc.printMsg(" \t\t\t============== [Tried Catch] Done Writing into csv for <ID = {}><src= {} > =============== ".format(row["ID"],row["SourceSite"]))
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
        # del writer

    # global OPEN_CSV
    # with open(csv_file, 'a+', newline='') as f:
    #     OPEN_CSV += 1
    #     csv_writer = csv.writer(f)
    #     # TODO: RUN AGAIN:url_string_content = await getUrlString(row["Content"])
    #     content = await clean_text(row["Content"])
    #     weighted_content = await clean_text(row["WeightedContent"])
    #     entry = [
    #         row["ID"],
    #         row["SourceSite"],
    #         row["ProcessingDate"],
    #         row["ProcessingEpoch"],
    #         row["CreationDate"],
    #         row["Title"],
    #         row["Url"],
    #         row["SourceTags"],
    #         row["ModelTags"],
    #         row["NumUpvotes"],
    #         row["NumComments"],
    #         row["PopI"],
    #         content,
    #         weighted_content,
    #         # weighted_content + content + url_string_content,
    #     ]
    #     csv_writer.writerow(entry)
    #     OPEN_CSV -= 1
    # pc.printErr("*************************************************** OPEN_CSV = {} **************************************".format(OPEN_CSV))
    # # f.close()
    # # If the the frequency of your writes to the file is high you may want to avoid the open/close overhead
    # #  adding a flush after each write to make sure the data is written to disk
    # # f.flush()
    # # os.fsync(f.fileno())

async def asyncFetchAll(csv_in,csv_out):
    """
        INPUT: csv_src_file & csv_dest_file(to be written)
        NOTE: 
            * Semaphore limit is: 500
            * While writing the response to csv_dest_file, it is done in chunks of `N` entries at a time
    """

    tasks = []
    sem = asyncio.Semaphore(5)

    """ Initialize the output file """
    headers = ['ID', 'SourceSite', 'ProcessingDate','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content']
    csv_functions.creteCsvFile(csv_out,headers)

    connector = TCPConnector(limit=10)
    async with ClientSession(headers={'Connection': 'keep-alive'},connector=connector) as session:
        with open(csv_in, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            global ENTRIES_TO_BE_WRITTEN
            for row in csv_reader:
                ENTRIES_TO_BE_WRITTEN += 1
                if(len(row["Content"]) != 0):
                    pc.printWarn("\t <ID = {}><src= {} > [NO SCRAPING] Content already exists............... NOW: {}".format(row["ID"],row["SourceSite"],time.strftime("%H:%M:%S", time.localtime())))
                    row["WeightedContent"] = row["Title"] + row["WeightedContent"] 
                    row["Content"] = row["Content"]
                    await write_result(csv_out, row)
                    global WRITTEN_ENTRIES_ASYNC_DIRECT
                    WRITTEN_ENTRIES_ASYNC_DIRECT += 1
                    pc.printMsg(" \t\t ==============  Done Writing into csv for <ID = {}><src= {} >=============== ".format(row["ID"],row["SourceSite"]))
                elif(row["Url"] and row["Title"]):
                    task = asyncio.ensure_future(semaphoreSafeFetch(sem, row, session,csv_out))
                    tasks.append(task)

        responses = await asyncio.gather(*tasks)
        pc.printMsg("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Total items to actually scrape(found w/o Content) = {} @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n".format(len(responses)))
        
""" ===============  Async-Executor Helpers: END ===============  """


""" ===============  Async-Executor Checker: START ===============  """

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
                url_string_content = text_actions.getUrlString(row["Content"])
                content = text_actions.clean_text(row["Content"])
                weighted_content = text_actions.clean_text(row["WeightedContent"])
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
                    weighted_content + url_string_content,
                    content,
                ]
                writer.writerow(entry)
                NO_LINES_IN_OUTPUT_CSV += 1
                if(len(row["Title"]) == 0):
                    NO_LINES_IN_OUTPUT_WITHOUT_TITLE += 1
                if(len(row["Url"]) == 0):
                    NO_LINES_IN_OUTPUT_WITHOUT_URL += 1
                if(len(row["Content"]) == 0):
                    NO_LINES_IN_OUTPUT_WITHOUT_CONTENT += 1

    #TODO:  os.remove(csv_in) %% rename

    pc.printWarn("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~ Analysis ~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    pc.printWarn("|\t NO_LINES_IN_INPUT_CSV                 \t | \t  {}  \t|".format(NO_LINES_IN_INPUT_CSV))
    pc.printWarn("|\t NO_LINES_IN_OUTPUT_CSV                \t | \t  {}  \t|".format(NO_LINES_IN_OUTPUT_CSV))
    pc.printWarn("|\t NO_LINES_IN_OUTPUT_WITHOUT_TITLE      \t | \t  {}  \t|".format(NO_LINES_IN_OUTPUT_WITHOUT_TITLE))
    pc.printWarn("|\t NO_LINES_IN_OUTPUT_WITHOUT_URL        \t | \t  {}  \t|".format(NO_LINES_IN_OUTPUT_WITHOUT_URL))
    pc.printWarn("|\t NO_LINES_IN_OUTPUT_WITHOUT_CONTENT    \t | \t  {}  \t|".format(NO_LINES_IN_OUTPUT_WITHOUT_CONTENT))


""" ===============  Async-Executor Checker: END ===============  """


""" ===============  Async-Executor : START ===============  """


def RunAsync(ts):
    """
        Pick wc-db's table mapped with `ts` and scrapes (useful) "clean" Content & WeightedContent from url- ASYNCLY
        * NOTE:
            * If conent is already present in the table, "clean" it too & append the newly scraped content to it.
            * FIRST RUN: time = 17 hours, data = 12 MB, #entries = 6.5k
        Input: ts (format: 1598692058.887741)
    """

    pc.printMsg('@[{}] >>>>>> Started Content-scraper(ASYNC) .......[Sema = 5, conn_lim =100]............ => FILENAME: {}\n'.format(datetime.fromtimestamp(ts),'dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'))

    stratTime = time.time()
    csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'

    # Run the async job
    asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(asyncFetchAll(csv_src_file,csv_dest_file)))

    endTime = time.time()
    pc.printSucc("\n****************** Content Scraping is Complete , FILENAME: {} ********************\n \t\t ===========> TIME TAKEN = {}".format('dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv', (endTime-stratTime)))    
    pc.printMsg('@[{}] >>>>>> Started Content-scraper(ASYNC) .......[Sema = 5, conn_lim =100]............\n'.format(datetime.fromtimestamp(ts)))
    
    pc.printMsg("\n------------------------------------------------------------------")   

    pc.printMsg("|\tENTRIES_TO_BE_WRITTEN                           \t  | \t {} \t|".format(ENTRIES_TO_BE_WRITTEN)) 
    pc.printMsg("|\tWRITTEN_ENTRIES_ASYNC_DIRECT                    \t  | \t {} \t|".format(WRITTEN_ENTRIES_ASYNC_DIRECT)) 
    pc.printMsg("|\tWRITTEN_ENTRIES_ASYNC_SCRAPED                   \t  | \t {} \t|".format(WRITTEN_ENTRIES_ASYNC_SCRAPED)) 
    pc.printMsg("|\tWRITTEN_ENTRIES_ASYNC_ON_URL_ERROR              \t  | \t {} \t|".format(WRITTEN_ENTRIES_ASYNC_ON_URL_ERROR)) 
    pc.printMsg("|\tWRITTEN_ENTRIES_ASYNC_NO_CONTENT_IN_SCRAPING    \t  | \t {} \t|".format(WRITTEN_ENTRIES_ASYNC_NO_CONTENT_IN_SCRAPING)) 
    pc.printMsg("|\tWRITTEN_ENTRIES_ASYNC_TRIED_ERR                 \t  | \t {} \t|".format(WRITTEN_ENTRIES_ASYNC_TRIED_ERR)) 
    pc.printMsg("|\tFAILED_ASYNC                                    \t  | \t {} \t|".format(FAILED_ASYNC)) 
    pc.printMsg("=====================================================================\n")    
    pc.printMsg("|\t Total Entries Written                          \t  | \t {} \t|".format(WRITTEN_ENTRIES_ASYNC_DIRECT + WRITTEN_ENTRIES_ASYNC_SCRAPED + WRITTEN_ENTRIES_ASYNC_ON_URL_ERROR + WRITTEN_ENTRIES_ASYNC_NO_CONTENT_IN_SCRAPING + WRITTEN_ENTRIES_ASYNC_TRIED_ERR)) 
    pc.printMsg("--------------------------------------------------------------------\n") 

    # Run the analysis
    cleanNcheckAsyncOutput(csv_src_file, csv_dest_file)   


""" --------------------------------===============  Async-Executor : END ===============--------------------------------  """


""" --------------------------------===============  sync-Executor : START ===============--------------------------------  """


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
            if(len(row["Content"]) != 0):
                pc.printWarn("\t <ID = {} > [NO SCRAPING] Content already exists....putting as it is............. NOW: {}".format(row["ID"],time.strftime("%H:%M:%S", time.localtime())))
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
                        text_actions.clean_text(row["Title"] + row["WeightedContent"]) + text_actions.getUrlString(row["Content"]),  #add the url-words too
                        text_actions.clean_text(row["Content"]) + text_actions.getUrlString(row["Content"])
                        ]
                global WRITTEN_ENTRIES_SYNC
                WRITTEN_ENTRIES_SYNC += 1
                f = csv.writer(open(csv_dest_file, "a"))  
                f.writerow(entry)
            #CHECK2(pre scraping): if(url == NULL)=>discard
            #CHECK3(pre scraping): if (row["title"]==NULL)=>discard
            elif ((len(row["Url"]) != 0)and(len(row["Title"]) != 0)):
                pc.printWarn("\t <ID = {} > [SCRAPING BEGIN] sleeping for 0.0001 second ZZZZZZzzzzzzzzzzzz................. NOW: {}".format(row["ID"],time.strftime("%H:%M:%S", time.localtime())))
                time.sleep(0.0001) 
                try:
                    # response = web_requests.hitGetWithRetry(url,TIMEOUT=10)
                    response = web_requests.hitGetWithRetry(row["Url"],'',False ,2,0.5,60)
                    # if response.status_code == 200:
                    if response != -1:
                        # content = text_actions.contentfromhtml(response)  #NOTE: for sync
                        content = text_actions.contentfromhtml(response.text)  #NOTE: for Async
                        urlstrings = text_actions.getUrlString(content)
                        content += urlstrings #add the url-words too
                        # weightedcontent = text_actions.weightedcontentfromhtml(response.text) + row["Title"] + urlstrings #add the url-words too      #NOTE: for sync
                        weightedcontent = text_actions.weightedcontentfromhtml(response.text) + row["Title"] + urlstrings #add the url-words too        #NOTE: for async
                        line_count += 1
                        #CHECK1(post scraping): if (content == null)&&(row["Title"] != null)<already checked abouve>=> row["Content"] = clean_text(row["title"]) AND row["weightedContent"] = clean_text(row["title"])
                        if(len(content) == 0):
                            content = row["Title"]
                            weightedcontent = row["Title"]
                        else:
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
                                text_actions.clean_text(weightedcontent) ,
                                text_actions.clean_text(content)
                                ]
                            
                        f = csv.writer(open(csv_dest_file, "a"))          
                        f.writerow(entry)
                        pc.printMsg("\t\t <ID = {} > ============== Scraping Done....... \t NOW: {}".format(row["ID"],time.strftime("%H:%M:%S", time.localtime())))
                    else:
                        global SKIPPED_SYNC
                        SKIPPED_SYNC += 1
                        pc.printErr("\t\txxxxx SKIPPING... for ID: {} Unable to hit url: {} , ".format(row["ID"],row["Url"]))
                except Exception as e:
                    global FAILED_SYNC
                    FAILED_SYNC += 1
                    pc.printErr("\t======= XXXXXXXX ERROR XXXXXX ======>> ID= {} NOW = {} Skipping...Failed due to: \n \t\t ERROR {}".format(row["ID"],time.strftime("%H:%M:%S", time.localtime()) ,e))
                    pass
    pc.printMsg("\n****************** Content Scraping is Complete , FILENAME: {} ********************\n".format('dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'))    
    pc.printMsg("\n----------------------------------------------------------------------------------\n")   
    pc.printMsg("|\tWRITTEN_ENTRIES_SYNC \t  | \t {} \t|".format(WRITTEN_ENTRIES_SYNC)) 
    pc.printMsg("|\tSKIPPED_SYNC          \t | \t {} \t|".format(SKIPPED_SYNC)) 
    pc.printMsg("|\tFAILED_SYNC           \t | \t {} \t|".format(FAILED_SYNC)) 
    pc.printMsg("\n----------------------------------------------------------------------------------\n")    
    



""" --------------------------------===============  sync-Executor : END ===============--------------------------------  """
