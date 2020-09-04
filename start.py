import time
from datetime import datetime
import csv

from scrapers import url_scraper_runner, content_scraper

if __name__ == '__main__':
    
    ts = datetime.now().timestamp()
    current_time = datetime.fromtimestamp(ts)
    
    print(" current time: {}".format(current_time))

    """ Run URL Scrapers : url_scarper.py  => update WC-DB & WP-DB """
    
    url_scraper_runner.run(ts)
    
    """ Run Conent Scraper : content_scraper.py => update WC-DB """

    content_scraper.run(ts)
    # content_scraper.run(1599005541)
    
    """ Run Tagger => update WC-DB """
    
    """ Run DomainHontessRanker => update DDS-DB """
    
    """ Run Newsletter Generator """
    
    """ Run Admin View Maker """
    
    
    
    
    
    
    
    
    
    
    