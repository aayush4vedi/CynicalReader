# import asyncio
# from timeit import default_timer

# from aiohttp import ClientSession
# import requests

# def demo_sequential(urls):
#     """Fetch list of web pages sequentially."""
#     start_time = default_timer()
#     for url in urls:
#         start_time_url = default_timer()
#         _ = requests.get(url)
#         elapsed = default_timer() - start_time_url
#         print('{0:30}{1:5.2f} {2}'.format(url, elapsed, asterisks(elapsed)))
#     tot_elapsed = default_timer() - start_time
#     print(' TOTAL SECONDS: '.rjust(30, '-') + '{0:5.2f} {1}'. \
#         format(tot_elapsed, asterisks(tot_elapsed)) + '\n')

# def demo_async(urls):
#     """Fetch list of web pages asynchronously."""
#     start_time = default_timer()

#     loop = asyncio.get_event_loop() # event loop
#     future = asyncio.ensure_future(fetch_all(urls)) # tasks to do
#     loop.run_until_complete(future) # loop until done

#     tot_elapsed = default_timer() - start_time
#     print(' WITH ASYNCIO: '.rjust(30, '-') + '{0:5.2f} {1}'. \
#         format(tot_elapsed, asterisks(tot_elapsed)))

# async def fetch_all(urls):
#     """Launch requests for all web pages."""
#     tasks = []
#     fetch.start_time = dict() # dictionary of start times for each url
#     async with ClientSession() as session:
#         for url in urls:
#             task = asyncio.ensure_future(fetch(url, session))
#             tasks.append(task) # create list of tasks
#         _ = await asyncio.gather(*tasks) # gather task responses

# async def fetch(url, session):
#     """Fetch a url, using specified ClientSession."""
#     fetch.start_time[url] = default_timer()
#     async with session.get(url) as response:
#         resp = await response.read()
#         elapsed = default_timer() - fetch.start_time[url]
#         print('{0:30}{1:5.2f} {2}'.format(url, elapsed, asterisks(elapsed)))
#         return resp

# def asterisks(num):
#     """Returns a string of asterisks reflecting the magnitude of a number."""
#     return int(num*10)*'*'

# if __name__ == '__main__':
#     URL_LIST = [
#                 # 'https://facebook.com',
#                 # 'https://github.com',
#                 'https://google.com',
#                 'https://google.com',
#                 'https://google.com',
#                 'https://google.com',
#                 'https://google.com',
#                 'https://google.com',
#                 'https://google.com',
#                 # 'https://microsoft.com',
#                 # 'https://yahoo.com'
#                 ]
#     # demo_sequential(URL_LIST)
#     demo_async(URL_LIST)
# """ ================================ POC: Compare Sync vs Async ==================================================== """

""" RESOURCES:
    * About asyncio: https://cheat.readthedocs.io/en/latest/python/asyncio.html
    * Below code is taken from Article: https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html

"""
# import requests
# from utilities import text_actions
# import asyncio
# from aiohttp import ClientSession, TCPConnector
# import time

# import ssl





# def syncDemo(urls):
#     res_arr = []
#     for url in urls:
#         response =  requests.get(url,verify=False,headers='')
#         print(" \t  URL: {} , STATUS: {}".format(url, response.status_code))
#         content = text_actions.contentfromhtml(response)
#         res_arr.append(content)
#     return res_arr


# async def asyncFetch(url):
#     async with ClientSession() as session:              # First `async`, fetches response asynchronously. ClientSession allows you to store cookies between requests and keeps objects that are common for all requests (event loop, connection and other things.Session needs to be closed after using it, and closing session is another asynchronous operation, this is why you need async with every time you deal with sessions.
#         async with session.get(url) as response:        # Second `async`, it reads response body in asynchronous manner
#             return await response.read()
#             # return text_actions.contentfromhtml(response)
#             # return response

# async def fetch(url, session):
#     async with session.get(url,ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)) as response: #FIXME: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain : FOUND@last comment: https://github.com/aio-libs/aiohttp/issues/3904
#         res = await response.read()
#         #NOTE: check for status codes here & put retry mechanisms( see: https://docs.aiohttp.org/en/stable/client_reference.html)
#         print("======================== URL : {}  \t STATUS: {}".format(url, response.status))
#         # print("======================== URL : {}".format(url))
#         return res

# async def semaphoreSafeFetch(sem, url, session):
#     # Getter function with semaphore.
#     async with sem:
#         await fetch(url, session)
#         # print("\n ******************************************************************* \n")

# async def asyncFetchAll(urls):
#     tasks = []

#     # create instance of Semaphore
#     sem = asyncio.Semaphore(50)

#     # Fetch all responses within one Client session,
#     # keep connection alive for all requests.
#     async with ClientSession(headers={'Connection': 'keep-alive'}) as session:
#         for url in urls:
#             # task = asyncio.ensure_future(fetch(url, session))
#             task = asyncio.ensure_future(semaphoreSafeFetch(sem, url, session))
#             tasks.append(task)

#         responses = await asyncio.gather(*tasks)
#         # you now have all response bodies in this variable
#         # print(responses)
#         return responses

# def asyncDemoExecutor(urls):
#     # FOR SINGLE URL
#     # loop = asyncio.get_event_loop()  
#     # loop.run_until_complete(asyncFetch(url))         # To start your program you need to run it in event loop
#     # loop = asyncio.get_event_loop()

#     # FOR MULTIPLE URLS
#     loop = asyncio.get_event_loop()  
#     #need to wrap `asyncFetchAll()` in asyncio Future object and pass whole lists of Future objects as tasks to be executed in the loop
#     future = asyncio.ensure_future(asyncFetchAll(urls))
#     loop.run_until_complete(future)

# if __name__ == "__main__":
#     url = "https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html"
#     urls = [
#         "https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html",
#         "https://github.com/connorferster/handcalcs",
#         "https://transitcosts.com/about/",
#         "https://www.howmanydayssinceajwtalgnonevuln.com",
#         "https://googleprojectzero.blogspot.com/2020/09/jitsploitation-one.html",
#         "https://mindemulation.org",
#         "http://www.markshelley.co.uk/Astronomy/SonyA7S/sonystareater.html",
#         "https://blogs.nvidia.com/blog/2020/09/01/nvidia-ceo-geforce-rtx-30-series-gpus/",
#         "https://algebradriven.design/",
#         "https://news.ycombinator.com/item?id=24342498",
#         "https://www.reddit.com/r/computerscience/comments/ijzbct/how_to_determine_which_rotation_to_use/",
#         "https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html",
#         "https://github.com/connorferster/handcalcs",
#         "https://transitcosts.com/about/",
#         "https://www.howmanydayssinceajwtalgnonevuln.com",
#         "https://googleprojectzero.blogspot.com/2020/09/jitsploitation-one.html",
#         "https://mindemulation.org",
#         "http://www.markshelley.co.uk/Astronomy/SonyA7S/sonystareater.html",
#         "https://blogs.nvidia.com/blog/2020/09/01/nvidia-ceo-geforce-rtx-30-series-gpus/",
#         "https://algebradriven.design/",
#         "https://news.ycombinator.com/item?id=24342498",
#         "https://www.reddit.com/r/computerscience/comments/ijzbct/how_to_determine_which_rotation_to_use/",
#         "https://www.howmanydayssinceajwtalgnonevuln.com",
#         "https://googleprojectzero.blogspot.com/2020/09/jitsploitation-one.html",
#         "https://mindemulation.org",
#         "http://www.markshelley.co.uk/Astronomy/SonyA7S/sonystareater.html",
#         "https://blogs.nvidia.com/blog/2020/09/01/nvidia-ceo-geforce-rtx-30-series-gpus/",
#         "https://algebradriven.design/",
#         "https://news.ycombinator.com/item?id=24342498",
#         "https://www.reddit.com/r/computerscience/comments/ijzbct/how_to_determine_which_rotation_to_use/",
#     ]


#     # print("\t======================== START Sync using `requests` ===========================\n")
#     # stratTime = time.time()
#     # syncRes = syncDemo(urls)
#     # endTime = time.time()
#     # print("======================== END Sync using `requests` ===========================\n \t\t >>> Time Taken = {} \n".format(endTime-stratTime))



#     print("\t======================== START Async using `asyncio` ===========================\n")
#     stratTime = time.time()
#     # asyncRes = asyncDemoExecutor(urls)
#     asyncDemoExecutor(urls)
#     # print("========================= Response ============================\n  \n ******** STARTTIME: {} ***********".format(stratTime))
#     endTime = time.time()
#     print("======================== END Sync using `asyncio` ===========================\n  \t\t >>> Time Taken = {} \n".format(endTime-stratTime))










""" ================================ POC: (async) Get content & weightedContent ==================================================== """

# # Article: https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
# import requests
# from utilities import text_actions
# import asyncio
# from aiohttp import ClientSession, TCPConnector
# import time

# import ssl

# from readability import Document
# from bs4 import BeautifulSoup


# def contentfromhtml(response):
#     """
#         get meaningful content from article page.Uses `readability` pkg
#         INPUT: http response object.E.g: `response = requests.get(url,verify=False,timeout=30)`
#         OUTPUT: single string of text
#     """

#     ## original starts=======
#     article = Document(response)
#     html = article.summary()
#     soup = BeautifulSoup(html)
#     ## ==========oring ends

#     # kill all script and style elements
#     for script in soup(["script", "style"]):
#         script.extract()    # rip it out

#     text = soup.get_text()
#     lines = (line.strip() for line in text.splitlines())
#     chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
#     text = ' '.join(chunk for chunk in chunks if chunk)
#     return text

# def weightedcontentfromhtml(response):
#     """
#         get emphasised words from meaningful content from article page
#         INPUT: http response object.E.g: `response = requests.get(url,verify=False,timeout=30)`
#         OUTPUT: single string of text
#     """
#     article = Document(response)
#     html = article.summary()
#     soup = BeautifulSoup(html)
#     whitelist = [
#         'h1',
#         'h2',
#         'h3',
#         'h4',
#         'strong',
#         'title',
#         'u',
#         'a',
#         # other elements,
#         ]
#     weightedcontent = ' '.join(t for t in soup.find_all(text=True) if t.parent.name in whitelist) 
#     return weightedcontent

# # def page_content(page):
# #     return BeautifulSoup(page, 'html.parser')


# async def fetch(url, session):
#     async with session.get(url,ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH), timeout = 15) as response: 
#         res = await response.text()
#         print("======================== URL : {}  \t STATUS: {}".format(url, response.status))
#         return res
#         # return await response.text()


# async def fetchWithRetry(url, session):
#     status = 400
#     #TODO: pass as arg
#     retry_cnt = 3 #TODO: pass as arg
#     sleep_time = 5 #NOTE: could be more because async
#     # while retry_cnt > 0 and status != 200:
#     #     try:
#     #         print("Trying...............\n")
#     #         async with session.get(url,ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH), timeout = 15) as response: 
#     #             res = await response.text()
#     #             status = response.status
#     #             if( status == 200 ):
#     #                 print("======================== URL : {}  \t STATUS: {}".format(url, response.status))
#     #                 return await response.text()
#     #     except status != 200:
#     #         # except aiohttp.ClientError:
#     #         print(" Excepting...............\n")
#     #         retry_cnt -= 1
#     #         print("\t x----------- Unable to hit URL: {} Sleeping for {} Retries remaining = {} --------------------x".format(url, sleep_time, retry_cnt))
#     #         await asyncio.sleep(sleep_time)
#     #         pass
#     while retry_cnt > 0 and status != 200:
#         async with session.get(url,ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH), timeout = 15) as response: 
#             res = await response.text()
#             status = response.status
#             if( status == 200 ):
#                 print("======================== URL : {}  \t STATUS: {}".format(url, status))
#                 return await response.text()
#             else:
#                 retry_cnt -= 1
#                 print("\t x----------- Unable to hit URL(ERR_CODE={}): {}  Sleeping for {} Retries remaining = {} --------------------x".format(status,url, sleep_time, retry_cnt))
#                 await asyncio.sleep(sleep_time)
#     return None

# async def semaphoreSafeFetch(sem, url, session):
#     async with sem:
#         return await fetchWithRetry(url, session)

# async def asyncFetchAll(urls):
#     tasks = []
#     sem = asyncio.Semaphore(50)

#     async with ClientSession(headers={'Connection': 'keep-alive'}) as session:
#         #NOTE: read here
#         for url in urls:
#             task = asyncio.ensure_future(semaphoreSafeFetch(sem, url, session))
#             tasks.append(task)

#         responses = await asyncio.gather(*tasks)
#         for res in responses:
#             #NOTE: write here
#             if(res == None):
#                 print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
#             else:
#                 print(" \t \t @@@@@@@@@@@@@@@@@@ START : CONTENT @@@@@@@@@@@@@@@@@@@ \n {} \n".format(contentfromhtml(res)))
#                 print(" \t \t @@@@@@@@@@@@@@@@@@ END @@@@@@@@@@@@@@@@@@@")
#                 print(" \t \t @@@@@@@@@@@@@@@@@@ START : WeightedCONTENT @@@@@@@@@@@@@@@@@@@ \n {} \n".format(weightedcontentfromhtml(res)))
#                 print(" \t \t @@@@@@@@@@@@@@@@@@ END @@@@@@@@@@@@@@@@@@@ \n")
#         return responses

# def asyncDemoExecutor(urls):
#     loop = asyncio.get_event_loop()  
#     future = asyncio.ensure_future(asyncFetchAll(urls))
#     result = loop.run_until_complete(future)



# def syncDemo(urls):
#     responses = []
#     for url in urls:
#         response =  requests.get(url,verify=False,headers='')
#         print(" \t  URL: {} , STATUS: {}".format(url, response.status_code))
#         responses.append(response)
#     for res in responses:
#         print(" \t \t @@@@@@@@@@@@@@@@@@ START : CONTENT @@@@@@@@@@@@@@@@@@@ \n {} \n".format(contentfromhtml(res.text)))
#         print(" \t \t @@@@@@@@@@@@@@@@@@ END @@@@@@@@@@@@@@@@@@@")
#         print(" \t \t @@@@@@@@@@@@@@@@@@ START : WeightedCONTENT @@@@@@@@@@@@@@@@@@@ \n {} \n".format(weightedcontentfromhtml(res.text)))
#         print(" \t \t @@@@@@@@@@@@@@@@@@ END @@@@@@@@@@@@@@@@@@@ \n")








# if __name__ == "__main__":
#     url = "https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html"
#     urls = [
#         "https://mindemulation.org/",
#         "https://www.reddit.com/r/compsci/comments/ij6x7g/pure_gold_the_internet_explained/",
#         "https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html",
#         "https://github.com/connorferster/handcalcs",
#         "https://transitcosts.com/about/",
#         "https://www.howmanydayssinceajwtalgnonevuln.com",
#         "https://googleprojectzero.blogspot.com/2020/09/jitsploitation-one.html",
#         "http://www.markshelley.co.uk/Astronomy/SonyA7S/sonystareater.html",
#         "https://blogs.nvidia.com/blog/2020/09/01/nvidia-ceo-geforce-rtx-30-series-gpus/",
#         "https://algebradriven.design/",
#         "https://news.ycombinator.com/item?id=24342498",
#         "https://www.reddit.com/r/computerscience/comments/ijzbct/how_to_determine_which_rotation_to_use/",
#         "https://transitcosts.com/about/",
#         "https://thistooshallgrow.com/blog/privacy-security-roundup"
#     ]



#     # print("\t======================== START Sync using `requests` ===========================\n")
#     # stratTime = time.time()
#     # syncDemo(urls)
#     # endTime = time.time()
#     # print("======================== END Sync using `requests` ===========================\n \t\t >>> Time Taken = {} \n".format(endTime-stratTime))



#     print("\t======================== START Async using `asyncio` ===========================\n")
#     stratTime = time.time()
#     # asyncRes = asyncDemoExecutor(urls)
#     asyncDemoExecutor(urls)
#     # print("========================= Response ============================ {} \n".format(asyncRes))
#     endTime = time.time()
#     print("======================== END Sync using `asyncio` ===========================\n  \t\t >>> Time Taken = {} \n".format(endTime-stratTime))







""" ================================ POC: (async) Read from csv & write to csv ==================================================== """

# Article: https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
import requests
from utilities import text_actions
import asyncio
from aiohttp import ClientSession, TCPConnector
import time
import csv
import string

import ssl

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
    html = article.summary()
    soup = BeautifulSoup(html)
    ## ==========oring ends

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

# def page_content(page):
#     return BeautifulSoup(page, 'html.parser')


async def fetchWithRetry(row, session):
    status = 400
    #TODO: pass as arg
    retry_cnt = 1 #TODO: pass as arg
    sleep_time = 0.1 #NOTE: could be more because async
    url = row["Url"]
    while retry_cnt > 0 and status != 200 and url:
        async with session.get(url,ssl=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH), timeout = 15) as response: 
            res = await response.text()
            status = response.status
            if( status == 200 ):
                print("======================== URL : {}  \t STATUS: {}".format(url, status))
                row["Content"] = contentfromhtml(res)
                row["WeightedContent"] = weightedcontentfromhtml(res)
                return row
            else:
                retry_cnt -= 1
                print("\t x----------- Unable to hit URL(ERR_CODE={}): {}  Sleeping for {} Retries remaining = {} --------------------x".format(status,url, sleep_time, retry_cnt))
                await asyncio.sleep(sleep_time)
    return row



async def semaphoreSafeFetch(sem, row, session):
    async with sem:
        return await fetchWithRetry(row, session)

async def write_result( result ):
    with open( 'results.csv', 'a' ) as csv_file:
        writer = csv.writer( csv_file )
        writer.writerow( result )

async def write_result(res, row, writer):
    async with asyncio.Lock():   # lock for gracefully write to shared file object
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
                weightedcontentfromhtml(res),   #TODO: add other things here too
                contentfromhtml(res)            #TODO: add other things here too
                ]
        writer.writerow(entry)


async def validate_page(sem, session, row, writer):
    url = row["Url"]                                        #TODO: check for url exists
    res = await semaphoreSafeFetch(sem, url, session)
    if res:
        print(" \t Writing into csv for ID={} .....................".format(row["ID"]))
        await write_result(res, row, writer)
        print(" \t\t ============== Done Writing into csv for ID={} =============== ".format(row["ID"]))
    else:
        print("\t [i={}] xxxxxxxxxxxxxxxxxxx Skipping xxxxxxxxxxxxxxxxxxxxxxxx\n".format(row["ID"]))


async def asyncFetchAll(csv_in,csv_out):
    tasks = []
    sem = asyncio.Semaphore(50)

    #Create new file
    f = csv.writer(open(csv_out, "w"))          # Flush the old file
    f.writerow(['ID', 'SourceSite', 'ProcessingTime','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content'])


    async with ClientSession(headers={'Connection': 'keep-alive'}) as session:
        with open(csv_in, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    writer = csv.writer(open(csv_out, "a"))
                    aws = [validate_page(sem, session, row, writer)]
                    await asyncio.gather(*aws)
            print('\n********************************** Done writing using Async *****************************\n')


async def asyncFetchAllNew(csv_in,csv_out):
    tasks = []
    sem = asyncio.Semaphore(50)

    async with ClientSession(headers={'Connection': 'keep-alive'}) as session:
        with open(csv_in, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            line_count = 0
            for row in csv_reader:
                # if line_count == 0:
                #     line_count += 1
                # else:
                    task = asyncio.ensure_future(semaphoreSafeFetch(sem, row, session))
                    tasks.append(task)

        responses = await asyncio.gather(*tasks)

        f = csv.writer(open(csv_out, "w"))          # Flush the old file
        f.writerow(['ID', 'SourceSite', 'ProcessingTime','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content'])

        f = csv.writer(open(csv_out, "a"))
        for res in responses:
            if res["Content"]:
                entry = [
                    res["ID"],
                    res["SourceSite"],
                    res["ProcessingTime"],
                    res["ProcessingEpoch"],
                    res["CreationDate"],
                    res["Title"],
                    res["Url"],
                    res["SourceTags"],
                    res["ModelTags"],
                    res["NumUpvotes"],
                    res["NumComments"],
                    res["PopI"],
                    res["Content"],
                    res["WeightedContent"],
                    ]
                f.writerow(entry)
                print(" \t\t ============== Done Writing into csv for ID={} =============== ".format(res["ID"]))
            else:
                print("\t\t xxxxxxxxxxxxxxxxxxx Skipping  for ID={} xxxxxxxxxxxxxxxxxxxxxxxx\n".format(row["ID"]))
                # print(" \t \t @@@@@@@@@@@@@@@@@@ START : CONTENT @@@@@@@@@@@@@@@@@@@ \n {} \n".format(contentfromhtml(res)))
                # print(" \t \t @@@@@@@@@@@@@@@@@@ END @@@@@@@@@@@@@@@@@@@")
                # print(" \t \t @@@@@@@@@@@@@@@@@@ START : WeightedCONTENT @@@@@@@@@@@@@@@@@@@ \n {} \n".format(weightedcontentfromhtml(res)))
                # print(" \t \t @@@@@@@@@@@@@@@@@@ END @@@@@@@@@@@@@@@@@@@ \n")
        return responses



def asyncDemoExecutor(csv_in,csv_out):
    loop = asyncio.get_event_loop()  
    # future = asyncio.ensure_future(asyncFetchAll(csv_in,csv_out))
    future = asyncio.ensure_future(asyncFetchAllNew(csv_in,csv_out))
    result = loop.run_until_complete(future)


def syncDemo(csv_in,csv_out):
    f = csv.writer(open(csv_out, "w"))          # Flush the old file
    f.writerow(['ID', 'SourceSite', 'ProcessingTime','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content'])

    with open(csv_in, mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        line_count = 0
        for row in csv_reader:
            # if line_count == 0:
            #     # print(f'Headers are {", ".join(row)}')
            #     line_count += 1
            # else:
                res =  requests.get(row["Url"],verify=False,headers='')
                if res.status_code == 200:
                    print(" \t Writing into csv for ID={} .....................".format(row["ID"]))
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
                        contentfromhtml(res.text),
                        weightedcontentfromhtml(res.text)
                        ]
                    f = csv.writer(open(csv_out, "a"))          
                    f.writerow(entry)
                    print(" \t\t ============== Done Writing into csv for ID={} =============== ".format(row["ID"]))
                else:
                    print("\t [i={}] xxxxxxxxxxxxxxxxxxx Skipping xxxxxxxxxxxxxxxxxxxxxxxx\n".format(row["ID"]))
    print('\n********************************** Done writing using Sync *****************************\n')           
                
def syncDemoReadOnly(csv_in,csv_out):
    responses = []
    with open(csv_in, mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                url = row["Url"]
                response =  requests.get(url,verify=False,headers='')
                print(" \t  URL: {} , STATUS: {}".format(url, response.status_code))
                responses.append(response)
    # for res in responses:
    #     print(" \t \t @@@@@@@@@@@@@@@@@@ START : CONTENT @@@@@@@@@@@@@@@@@@@ \n {} \n".format(contentfromhtml(res.text)))
    #     print(" \t \t @@@@@@@@@@@@@@@@@@ END @@@@@@@@@@@@@@@@@@@")
    #     print(" \t \t @@@@@@@@@@@@@@@@@@ START : WeightedCONTENT @@@@@@@@@@@@@@@@@@@ \n {} \n".format(weightedcontentfromhtml(res.text)))
    #     print(" \t \t @@@@@@@@@@@@@@@@@@ END @@@@@@@@@@@@@@@@@@@ \n")

if __name__ == "__main__":
    
    csv_in = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/POC/dummy_wc_table.csv'
    csv_out_sync = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/POC/dummy_wc_table_sync.csv'
    csv_out_async = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/POC/dummy_wc_table_async_wc.csv'

    # headers = ['ID', 'SourceSite', 'ProcessingTime','ProcessingEpoch','CreationDate', 'Title', 'Url','ThumbnailUrl' ,'SourceTags','NumUpvotes', 'NumComments', 'PopI','Content']
    # csv_functions.creteCsvFile(csv_out,headers)

    print("\t======================== START Sync using `requests` ===========================\n")
    stratTime = time.time()
    syncDemo(csv_in,csv_out_sync)
    # syncDemoReadOnly(csv_in,csv_out_sync)
    endTime = time.time()
    print("======================== END Sync using `requests` ===========================\n \t\t >>> Time Taken = {} \n".format(endTime-stratTime))



    print("\t======================== START Async using `asyncio` ===========================\n")
    stratTime = time.time()
    # asyncDemoExecutor(urls)
    asyncDemoExecutor(csv_in,csv_out_async)
    # print("========================= Response ============================ {} \n".format(asyncRes))
    endTime = time.time()
    print("======================== END Sync using `asyncio` ===========================\n  \t\t >>> Time Taken = {} \n".format(endTime-stratTime))










