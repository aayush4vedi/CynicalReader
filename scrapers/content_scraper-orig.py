import csv
import string
import time
from datetime import datetime, timedelta
import asyncio
from aiohttp import ClientSession, TCPConnector
import ssl

from utilities import csv_functions, text_actions, web_requests
from utilities import print_in_color as pc

ENTRIES_TO_BE_WRITTEN = 0        # total entries in original file
WRITTEN_ENTRIES_ASYNC_DIRECT = 0        # for every entry written- just copied from prev file
WRITTEN_ENTRIES_ASYNC_SCRAPED = 0        # for every entry written- fetched by scraping
SKIPPED_ASYNC = 0                # when unable to hit url
FAILED_ASYNC = 0                 # other failures
WRITTEN_ENTRIES_SYNC = 0
SKIPPED_SYNC = 0
FAILED_SYNC = 0


""" =============== Async-Executor Helpers: START ===============  """

async def fetchWithRetry(row, session):
    status = 400
    retry_cnt = 3
    sleep_time = 10
    TIMEOUT = 60

    while retry_cnt > 0 and status != 200:
        async with session.get(row["Url"],ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH), timeout = TIMEOUT) as response: 
            res = await response.text()
            status = response.status
            if( status == 200 and len(res) != 0):
                pc.printSucc("\t\t <ID = {}><src= {} > ============== Scraping Done....... \t NOW: {}".format(row["ID"],row["SourceSite"],time.strftime("%H:%M:%S", time.localtime())))
                urlstrings = text_actions.getUrlString(row["Content"])
                row["WeightedContent"] = text_actions.clean_text(text_actions.weightedcontentfromhtml(res) + row["Title"] + urlstrings)
                row["Content"] = text_actions.clean_text(text_actions.contentfromhtml(res)  + urlstrings)
                if(len(row["Content"]) == 0):
                    row["WeightedContent"] = text_actions.clean_text(row["Title"])
                    row["Content"] =  text_actions.clean_text(row["Title"])
                # pc.printWarn("\t <ID = {}><src= {} > sleeping for 0.0001 second ZZZZZZzzzzzzzzzzzz................. NOW: {}".format(row["ID"],row["SourceSite"],time.strftime("%H:%M:%S", time.localtime())))
                # time.sleep(0.001) 
                return row
            else:
                retry_cnt -= 1
                pc.printWarn("\t x---------------- Unable to hit URL(ERR_CODE={}): {}  Sleeping for {} Retries remaining = {} -------------x".format(status,row["Url"], sleep_time, retry_cnt))
                await asyncio.sleep(sleep_time)
    pc.printErr("\t\txxxxx SKIPPING... for <ID = {}><src= {} > Unable to hit url: {} , ".format(row["ID"],row["SourceSite"],row["Url"]))
    global SKIPPED_ASYNC 
    SKIPPED_ASYNC += 1
    return row



async def semaphoreSafeFetch(sem, row, session):
    """
        Simple puts check for semaphore count
    """
    async with sem:
        try:
            return await fetchWithRetry(row, session)
        except Exception as e:
            global FAILED_ASYNC
            FAILED_ASYNC += 1
            pc.printErr("\t======= XXXXXXXX ERROR XXXXXX ======>> <ID = {}><src= {} > NOW = {} Skipping...Failed due to: \n \t\t ERROR {}".format(row["ID"],row["SourceSite"],time.strftime("%H:%M:%S", time.localtime()) ,e))
            pass
    return row              #FIXME: this fucker!!!

async def write_result(csv_file, entry):
    async with asyncio.Lock():   # lock for gracefully write to shared file object
        # writer.writerow(entry)
        with open(csv_file, 'a+', newline='') as write_obj:
            csv_writer = csv.writer(write_obj)
            csv_writer.writerow(entry)
        write_obj.close()

async def asyncFetchAll(csv_in,csv_out):
    """
        INPUT: csv_src_file & csv_dest_file(to be written)
        NOTE: 
            * Semaphore limit is: 500
            * While writing the response to csv_dest_file, it is done in chunks of `N` entries at a time
    """

    tasks = []
    sem = asyncio.Semaphore(1000)

    """ Initialize the output file """
    headers = ['ID', 'SourceSite', 'ProcessingTime','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content']
    csv_functions.creteCsvFile(csv_out,headers)

    connector = TCPConnector(limit=0)
    async with ClientSession(headers={'Connection': 'keep-alive'},connector=connector) as session:
        with open(csv_in, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            line_count = 0
            global ENTRIES_TO_BE_WRITTEN
            for row in csv_reader:
                ENTRIES_TO_BE_WRITTEN += 1
                if(len(row["Content"]) != 0):
                    pc.printWarn("\t <ID = {}><src= {} > [NO SCRAPING] Content already exists............... NOW: {}".format(row["ID"],row["SourceSite"],time.strftime("%H:%M:%S", time.localtime())))
                    row["WeightedContent"] = text_actions.clean_text(row["Title"] + row["WeightedContent"]) + text_actions.getUrlString(row["Content"])
                    row["Content"] = text_actions.clean_text(row["Content"]) + text_actions.getUrlString(row["Content"])
                    entry = [
                        row["ID"],
                        row["SourceSite"],
                        row["ProcessingTime"],
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
                    csv_functions.putToCsv(csv_out, entry)
                    global WRITTEN_ENTRIES_ASYNC_DIRECT
                    WRITTEN_ENTRIES_ASYNC_DIRECT += 1
                    pc.printMsg(" \t\t ============== Done Writing into csv for <ID = {}><src= {} >=============== ".format(row["ID"],row["SourceSite"]))
                elif(row["Url"] and row["Title"]):
                    task = asyncio.ensure_future(semaphoreSafeFetch(sem, row, session))
                    tasks.append(task)

        responses = await asyncio.gather(*tasks)
        
        pc.printMsg("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ len(responses):: to be scraped = {} @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n".format(len(responses)))
        
        for row in responses:
            if row["Content"] or row["Title"]:
                if len(row["Content"]) == 0:          # that means url was hit successfully and content was generated
                    row["Content"] = row["Title"]
                entry = [
                    row["ID"],
                    row["SourceSite"],
                    row["ProcessingTime"],
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
                await write_result(csv_out,entry)
                # csv_functions.putToCsv(csv_out, entry)
                global WRITTEN_ENTRIES_ASYNC_SCRAPED
                WRITTEN_ENTRIES_ASYNC_SCRAPED += 1
                pc.printMsg(" \t\t ============== Done Writing into csv for <ID = {}><src= {} > =============== ".format(row["ID"],row["SourceSite"]))
            else:
                pc.printErr("\t\t xxxxxxxxxxxxxxxxxxx Skipping  for <ID = {}><src= {} > As No Content & Title xxxxxxxxxxxxxxxxxxxxxxxx\n".format(row["ID"],row["SourceSite"]))




""" ===============  Async-Executor Helpers: END ===============  """

""" ===============  Async-Executor : START ===============  """


def RunAsync(ts):
    """
        Pick wc-db's table mapped with `ts` and scrapes (useful) "clean" Content & WeightedContent from url- ASYNCLY
        * NOTE:
            * If conent is already present in the table, "clean" it too & append the newly scraped content to it.
            * FIRST RUN: time = 17 hours, data = 12 MB, #entries = 6.5k
        Input: ts (format: 1598692058.887741)
    """

    # pc.printMsg('@[{}] >>>>>> Started Content-scraper(ASYNC) .......[Sema = 10, conn_lim =10]............ => FILENAME: {}\n'.format(datetime.fromtimestamp(ts),'dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'))
    pc.printMsg('@[{}] >>>>>> Started Content-scraper(ASYNC) .......[Sema = 50, conn_lim =50]............ => FILENAME: {}\n'.format(datetime.fromtimestamp(ts),'dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'))

    stratTime = time.time()
    csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'_wwccc100-8.csv'

    # Run the async job
    asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(asyncFetchAll(csv_src_file,csv_dest_file)))

    endTime = time.time()
    pc.printSucc("\n****************** Content Scraping is Complete , FILENAME: {} ********************\n \t\t ===========> TIME TAKEN = {}".format('dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv', (endTime-stratTime)))    
    
    pc.printMsg("\n------------------------------------------------------------------------")   
    pc.printMsg("|\tENTRIES_TO_BE_WRITTEN        \t  | \t {} \t|".format(ENTRIES_TO_BE_WRITTEN)) 
    pc.printMsg("|\tWRITTEN_ENTRIES_ASYNC_DIRECT \t  | \t {} \t|".format(WRITTEN_ENTRIES_ASYNC_DIRECT)) 
    pc.printMsg("|\tWRITTEN_ENTRIES_ASYNC_SCRAPED\t  | \t {} \t|".format(WRITTEN_ENTRIES_ASYNC_SCRAPED)) 
    pc.printMsg("|\tSKIPPED_ASYNC                \t  | \t {} \t|".format(SKIPPED_ASYNC)) 
    pc.printMsg("|\tFAILED_ASYNC                 \t  | \t {} \t|".format(FAILED_ASYNC)) 
    pc.printMsg("--------------------------------------------------------------------------\n")    


""" --------------------------------===============  Async-Executor : END ===============--------------------------------  """


""" --------------------------------===============  sync-Executor : START ===============--------------------------------  """


def RunSync(ts):
    """
        Pick wc-db's table mapped with `ts` and scrapes (useful) "clean" Content & WeightedContent from url.
        * NOTE:
            * If conent is already present in the table, "clean" it too & append the newly scraped content to it.
            * FIRST RUN: time = 17 hours, data = 12 MB, #entries = 6.5k
        Input: ts (format: 1598692058.887741)
    """
    pc.printMsg('@[{}] >>>>>> Started Content-scraper(SYNC) ................... => FILENAME: {}\n'.format(datetime.fromtimestamp(ts),'dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'))

    csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'_wc_sync.csv'
    index = 1
    headers = ['ID', 'SourceSite', 'ProcessingTime','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content']
    csv_functions.creteCsvFile(csv_dest_file,headers)

    f = csv.writer(open(csv_dest_file, "w"))          # Flush the old file
    f.writerow(['ID', 'SourceSite', 'ProcessingTime','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content'])
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
                        row["ProcessingTime"],
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
                                row["ProcessingTime"],
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