from collections import OrderedDict
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from xml.etree import ElementTree
import sys
from csv import writer
import json
import string
import time
from datetime import datetime, timedelta

from utilities import csv_functions, text_actions, web_requests
import vault
from utilities import print_in_color as pc

def run(ts):
    """
        Scrapes PH api for last 7 days & puts data in WP-DB.
            * Api supports daywaise only. So scrape for one day at a time
            * Link to documentation: https://api.producthunt.com/v1/docs/posts/posts_index_request_a_specific_day_with_the_%60day%60_parameter_(tech_category)
        * NOTE:
            * No threshold set on upvotes or comments rn.Maybe later?
            * API-Ratelimit: You can make up to 900 requests every 15 minutes, else gives `status 429` in response.If that happens, wait for 16 mins, then hit again.   
                * Retry 2 times; if failed nonetheless, skip!
            * Content = Tagline
            * URL: is the PH url only. Going to the product page & then finding the actual link is overkill
                * (this could also help later on getting their permission while monetizing)
            * Used self-retry logic. but check this package:: Read about requests.retries here: [doc](https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure), [stkofw](https://stackoverflow.com/questions/23267409/how-to-implement-retry-mechanism-into-python-requests-library?rq=1)
        Input: ts (format: 1598692058.887741)
    """

    pc.printSucc('@[{}] >>>>>> Started PH-scraper ................... => FILENAME: {}\n'.format(datetime.fromtimestamp(ts),'dbs/wp-db/wp_table_'+str(int(ts))+'.csv'))

    """
        here is how you add day to `ts`:

        from datetime import datetime, timedelta
        newts = datetime.fromtimestamp(ts) + timedelta(days=1) # 2020-08-30 16:02:34.352094
        newts.timestamp() # 1598783633.284871
        datetime.fromtimestamp(ts) #2020-08-29 17:15:32
        # get date from it: 
        datetime.fromtimestamp(ts).date() #2020-08-29
    """

    """ days_arr has last 7 days(including today's) (YYYY-MM-DD)date strings ; just the way PH's API needs
    """
    curr_date = str(int(ts))
    days_arr = [str(datetime.fromtimestamp(int(ts)).date())] # '2020-08-29'

    for i in range(6):
        new_ts = datetime.fromtimestamp(int(curr_date)) + timedelta(days=-1)
        new_ts = new_ts.timestamp()
        curr_date = new_ts
        days_arr.append(str(datetime.fromtimestamp(int(new_ts)).date()))

    PH_REQ_HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + vault.PH_ACCESS_TOKEN ,
        "Host": "api.producthunt.com"
    }

    csv_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wp-db/wp_table_'+str(int(ts))+'.csv'
    index = 1

    for date in days_arr:
        pc.printMsg(" ................. scraping for date =  {} .................\n".format(date))
        url = 'https://api.producthunt.com/v1/posts?day=' + date
        try:
            data = web_requests.hitGetWithRetry(url,PH_REQ_HEADERS,False ,2,5,10)
            if(data == -1):
                pc.printErr("\t\txxxxxx Unable to hit {} after 2 retries.Skipping this date( {} ) xxxxxx\n".format(url,date))
            else:
                items_arr = json.loads(data.content)["posts"]
                for item in items_arr:
                    # print(json.dumps(item, indent = 4))
                    """ get all the tags attached along with the item """
                    source_tags = []
                    for tag in item["topics"]:
                        source_tags.append(tag["name"])
                    entry = [
                        index,
                        "PH",
                        datetime.fromtimestamp(ts),
                        int(ts),
                        item["created_at"],
                        item["name"],             
                        item["discussion_url"],
                        item["thumbnail"]["image_url"],
                        source_tags,
                        item["votes_count"],
                        item["comments_count"],
                        '',
                        item["tagline"]
                        ]
                    csv_functions.putToCsv(csv_file,entry)
                    index=index+1

        except Exception as e:
            pc.printErr(" \t xxxxxxxxxxxxx ERROR xxxxxxxxxxxxxxxxxxxx >> [ID]= {} Skipping...Failed due to: {} \n".format(index, e))
            pass

        pc.printMsg("\t\t\t ====>> TOTAL_ENTRIES_YET = {}".format(index+1))

    pc.printSucc("\n****************** PH Url Scraping is Complete : TOTAL_ENTRIES_YET = {} , FILENAME: {} ********************\n".format(index+1,'dbs/wp-db/wp_table_'+str(int(ts))+'.csv'))