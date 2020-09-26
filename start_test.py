import time
from datetime import datetime
import csv

from scrapers import url_scraper_runner, content_scraper
from components import popi_calculator, tagger_simulator
from utilities import print_in_color as pc
import tree_maker
import sqlite3

"""
   Run any component independently as you want
   URL_TABLE: wc_1600014495  (update later if changed)
"""



def create_test_table(n):       # similar to wc_1599816944 (the url-only table)
    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(n) 
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    c.execute("create table " + wc_table + " as select * from wc_1600014495")
    pc.printWarn("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Created test table in dc.db => {} @@@@@@@@@@@@@@@@@@@@@@@@@@@@".format(wc_table))

if __name__ == '__main__':
    
    # ts = datetime.now().timestamp()
    # current_time = datetime.fromtimestamp(ts)
    
    # pc.printMsg(" current time: {}".format(current_time))

    """ Run URL Scrapers : url_scarper.py  => table@ts in (WC-DB, WP-DB) """

    # url_scraper_runner.run(ts)
    
    """ Run Conent Scraper : content_scraper.py => table@ts in (WC-DB, WP-DB) """
    # create_test_table(111111)                # Update time here: as per the name of tmp(copy) table 
    # content_scraper.run(1600925655)          
    
    """ Run PopICalculator => update table@ts in (WC-DB, WP-DB) """

    # popi_calculator.run(1600925655)

    """ Run Tagger => update WC-DB """
    
    # tagger_simulator.run(1600925655)

    """ Run DomainHontessRanker => update DDS-DB """
    tree_maker.run(1600925655)
    
    """ Run Newsletter Generator """
    
    """ Run Admin View Maker """
    
    

