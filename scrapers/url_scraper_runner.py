from scrapers.urlScrapers import hn_scraper, r_scraper, ph_scraper
from utilities import csv_functions

from utilities import print_in_color as pc

def run(ts):

    """ Runs following scrapers serially and updates them in WC-DB:
        1. hn_scraper.py
        2. r_scraper.py
        4. ph_scraper.py => Api exists, Scraping not allowed(doint it anyway)
        3. ih_scraper.py => No Api, Scraping not allowed(postponed for later)

        Input: float(timestamp) - set when the main.py run is triggered
            * float because o/w `datetime.fromtimestamp(ts)` wont run on int
        Outpu: None, just put data in WC-DB
    """

    """ Initialize the weekly content table in wc-db and wp-db"""
    
    wc_db_table = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    headers = ['ID', 'SourceSite', 'ProcessingTime','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content']
    csv_functions.creteCsvFile(wc_db_table,headers)

    wp_db_table = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wp-db/wp_table_'+str(int(ts))+'.csv'
    headers = ['ID', 'SourceSite', 'ProcessingTime','ProcessingEpoch','CreationDate', 'Title', 'Url','ThumbnailUrl' ,'SourceTags','NumUpvotes', 'NumComments', 'PopI','Content']
    csv_functions.creteCsvFile(wp_db_table,headers)


    """ Run the scrapers sequentially """

    try:
        hn_scraper.run(ts)
        pc.printSucc("\n================ HH url scraper run: Complete ================\n")
    except Exception as e:
        pc.printErr(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in scraping HN for url xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\t>>> Error = {}".format(str(e)))
        pass

    try:
        r_scraper.run(ts)
        pc.printSucc(" \n================ Reddit url scraper run: Complete ================\n")
    except Exception as e:
        pc.printErr(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in scraping Reddit for url xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\tError = {}".format(str(e)))
        pass

    try:
        ph_scraper.run(ts)
        pc.printSucc(" \n====== PH url scraper run: Complete ======\n")
    except Exception as e:
        pc.printErr(" XXXXXXXXXXXX Error in scraping PH for url XXXXXXXXXXXXXXXXX \n \t\tError = {}".format(str(e)))
        pass

    # try:
    #     ih_scraper.run(ts)
    #     print(" \n====== IH url scraper run: Complete ======\n")
    # except Exception as e:
    #     print(" XXXXXXXXXXXX Error in scraping IH for url XXXXXXXXXXXXXXXXX \n \t\tError = {}".format(str(e)))
    #     pass
    pc.printSucc(" ******************** All url scrapers ran successfully *****************\n")


