import time
from datetime import datetime
import csv

from scrapers import url_scraper_runner, content_scraper
from components import popi_calculator
from utilities import print_in_color as pc

"""
    # NOTE: to dupicate a table(for testing)
        CREATE TABLE wc_123456 AS SELECT * FROM wc_1599816944;
"""


import sqlite3

def create_test_table(n):       # similar to wc_1599816944 (the url-only table)
    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(n) 
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    c.execute("create table " + wc_table + " as select * from wc_1600014495")
    pc.printWarn("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Created test table in dc.db => {} @@@@@@@@@@@@@@@@@@@@@@@@@@@@".format(wc_table))

if __name__ == '__main__':
    
    ts = datetime.now().timestamp()
    current_time = datetime.fromtimestamp(ts)
    
    pc.printMsg(" current time: {}".format(current_time))

    """ Run URL Scrapers : url_scarper.py  => table@ts in (WC-DB, WP-DB) """

    url_scraper_runner.run(ts)
    
    """ Run Conent Scraper : content_scraper.py => table@ts in (WC-DB, WP-DB) """

    # content_scraper.RunAsync(ts)
    
    # for testing purposes...................
    # content_scraper.RunAsync(1599855814)
    # create_test_table(7)
    # content_scraper.RunAsync(7)        
    # content_scraper.RunSync(1599009243)           #Not used       
    
    """ Run PopICalculator => update table@ts in (WC-DB, WP-DB) """

    popi_calculator.run(ts)
    # popi_calculator.run(1600014495)

    """ Run Tagger => update WC-DB """
    
    """ Run DomainHontessRanker => update DDS-DB """
    
    """ Run Newsletter Generator """
    
    """ Run Admin View Maker """
    
    
    
    
    
    
