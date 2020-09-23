import sqlite3
import traceback
import logging
from scrapers.urlScrapers import hn_scraper, r_scraper, ph_scraper
from utilities import csv_functions

from utilities import print_in_color as pc

def run(ts):

    """ I. Creates wc_table(in wc.db) & wp_table(in wp.dp) for the week
        II. Runs following scrapers serially and updates them in WC-DB:
            1. hn_scraper.py
            2. r_scraper.py
            4. ph_scraper.py => Api exists, Scraping not allowed(doint it anyway)
            3. ih_scraper.py => No Api, Scraping not allowed(postponed for later)

        Input: float(timestamp) - set when the main.py run is triggered
            * float because o/w `datetime.fromtimestamp(ts)` wont run on int
        Outpu: None, just put data in WC-DB
    """

    """ Initialize the weekly content tables in wc.db and wp.db"""
    
    # wc_db = 'POC/poc.db'
    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts)) 
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'".format(wc_table))
    if c.fetchone()[0]==1 :                        # table exists, flush away!
        c.execute("delete from {}".format(wc_table))
    else :                                         # creting new table
        c.execute("CREATE TABLE {} (ID, SourceSite, ProcessingDate,ProcessingEpoch,CreationDate, Title, Url, SourceTags,ModelTags,NumUpvotes, NumComments, PopI,WeightedContent,Content)".format(wc_table))

    wp_db = 'dbs/wp.db'
    wp_table = 'wp_' + str(int(ts))
    conn = sqlite3.connect(wp_db, timeout=10)
    c = conn.cursor()
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'".format(wp_table))
    if c.fetchone()[0]==1 :                        # table exists, flush away!
        c.execute("delete from {}".format(wc_table))
    else :                                         # creting new table
        c.execute('''CREATE TABLE {}
                (ID, SourceSite, ProcessingDate,ProcessingEpoch,CreationDate, Title, Url, ThumbnailUrl,SourceTags,NumUpvotes, NumComments, PopI,Content)'''.format(wp_table))


    # wc_db_table = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    # headers = ['ID', 'SourceSite', 'ProcessingDate','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content']
    # csv_functions.creteCsvFile(wc_db_table,headers)

    # wp_db_table = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wp-db/wp_table_'+str(int(ts))+'.csv'
    # headers = ['ID', 'SourceSite', 'ProcessingDate','ProcessingEpoch','CreationDate', 'Title', 'Url','ThumbnailUrl' ,'SourceTags','NumUpvotes', 'NumComments', 'PopI','Content']
    # csv_functions.creteCsvFile(wp_db_table,headers)


    """ Run the scrapers sequentially """

    try:
        hn_scraper.run(ts)
        pc.printSucc("\n================ HH url scraper run: Complete ================\n")
    except Exception as e:
        pc.printErr(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in Running Url Scraper-HN xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\t>>> Error = {}".format(str(e)))
        logging.error(traceback.format_exc())
        pass

    try:
        r_scraper.run(ts)
        pc.printSucc(" \n================ Reddit url scraper run: Complete ================\n")
    except Exception as e:
        pc.printErr(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in Running Url Scraper-Reddit xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\tError = {}".format(str(e)))
        logging.error(traceback.format_exc())
        pass

    try:
        ph_scraper.run(ts)
        pc.printSucc(" \n================ PH url scraper run: Complete ================\n")
    except Exception as e:
        pc.printErr(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in Running Url Scraper-PH xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\tError = {}".format(str(e)))
        logging.error(traceback.format_exc())
        pass

    # try:
    #     ih_scraper.run(ts)
    #     print(" \n====== IH url scraper run: Complete ======\n")
    # except Exception as e:
    #     print(" XXXXXXXXXXXX Error in scraping IH for url XXXXXXXXXXXXXXXXX \n \t\tError = {}".format(str(e)))
    #     pass
    pc.printSucc(" ******************** All url scrapers ran successfully *****************\n")


