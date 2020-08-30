import time
from datetime import datetime
import csv

from scrapers import url_scraper_runner
from utilities import csv_functions



if __name__ == '__main__':
    
    ts = datetime.now().timestamp()
    current_time = datetime.fromtimestamp(ts)
    
    print(" current time: {}".format(current_time))

    """ Initialize the weekly content table in wc-db"""
    csv_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/table_'+str(int(ts))+'.csv'
    headers = ['ID', 'SourceSite', 'ProcessingTime','ProcessingEpoch','CreationDate', 'Title', 'Url', 'SourceTags','ModelTags','NumUpvotes', 'NumComments', 'PopI','WeightedContent','Content']
    csv_functions.creteCsvFile(csv_file,headers)
    
    """ Run URL Scrapers : url_scarper.py  => update WC-DB """
    
    url_scraper_runner.run(ts)
    
    """ Run Conent Scraper : content_scraper.py => update WC-DB """
    
    """ Run Tagger => update WC-DB """
    
    """ Run DomainHontessRanker => update DDS-DB """
    
    """ Run Newsletter Generator """
    
    """ Run Admin View Maker """
    
    
    
    
    
    
    
    
    
    
    
    