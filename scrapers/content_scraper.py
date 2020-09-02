import csv
import string
import time
from datetime import datetime, timedelta

from utilities import csv_functions, text_actions, web_requests

def run(ts):
    """
        Pick wc-db's table mapped with `ts` and scrapes (useful) "clean" Content & WeightedContent from url.
        * NOTE:
            * If conent is already present in the table, "clean" it too & append the newly scraped content to it.
            * FIRST RUN: time = 17 hours, data = 12 MB, #entries = 6.5k
        Input: ts (format: 1598692058.887741)
    """

    print('@[{}] >>>>>> Started HN-scraper ................... => FILENAME: {}\n'.format(datetime.fromtimestamp(ts),'dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'))

    csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'
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
                print("\t <ID = {} > [NO SCRAPING] Content already exists....putting as it is............. NOW: {}".format(row["ID"],time.strftime("%H:%M:%S", time.localtime())))
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
                        text_actions.clean_text(row["Content"]) + text_actions.getUrlString(row["Content"]),
                        text_actions.clean_text(row["Title"] + row["WeightedContent"]) + text_actions.getUrlString(row["Content"])  #add the url-words too
                        ]
                f = csv.writer(open(csv_dest_file, "a"))  
                f.writerow(entry)
            #CHECK2(pre scraping): if(url == NULL)=>discard
            #CHECK3(pre scraping): if (row["title"]==NULL)=>discard
            else if ((len(row["Url"]) != 0)and(len(row["Title"]) != 0)):
                print("\t <ID = {} > [SCRAPING BEGIN] sleeping for 0.0001 second ZZZZZZzzzzzzzzzzzz................. NOW: {}".format(row["ID"],time.strftime("%H:%M:%S", time.localtime())))
                time.sleep(0.0001) 
                try:
                    # response = web_requests.hitGetWithRetry(url,TIMEOUT=10)
                    response = web_requests.hitGetWithRetry(url,'',False ,2,5,10)
                    if response.status_code == 200:
                        content = text_actions.contentfromhtml(response) + text_actions.getUrlString(content) #add the url-words too
                        weightedcontent = text_actions.contentfromhtml(row["Title"]) + text_actions.weightedcontentfromhtml(response) + text_actions.getUrlString(content) #add the url-words too
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
                                text_actions.clean_text(content)]
                            
                        f = csv.writer(open(csv_dest_file, "a"))          
                        f.writerow(entry)
                        print("\t\t <ID = {} > ============== Scraping Done....... \t NOW: {}".format(row["ID"],time.strftime("%H:%M:%S", time.localtime())))
                    else:
                        print("\t\txxxxx SKIPPING... for ID: {} Found Error code: {} , ".format(row["ID"],response.status_code))
                except Exception as e:
                    print("\t======= XXXXXXXX ERROR XXXXXX ======>> ID= {} NOW = {} Skipping...Failed due to: \n \t\t ERROR {}".format(row["ID"],time.strftime("%H:%M:%S", time.localtime()) ,e))
                    pass
    print("\n****************** Content Scraping is Complete , FILENAME: {} ********************\n".format('dbs/wc-db/wc_table_'+str(int(ts))+'_wc.csv'))    





































        