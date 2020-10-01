import time
from datetime import datetime
import csv

from scrapers import url_scraper_runner, content_scraper
from components import popi_calculator, tagger_simulator, th_creator, th_query
from utilities import print_in_color as pc
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
    c.execute("create table " + wc_table + " as select * from wc_1601413857")   #url table
    # c.execute("create table " + wc_table + " as select * from wc_1601292562")   #full content table
    pc.printWarn("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Created test table in dc.db => {} @@@@@@@@@@@@@@@@@@@@@@@@@@@@".format(wc_table))

if __name__ == '__main__':
    
    # ts = datetime.now().timestamp()
    # current_time = datetime.fromtimestamp(ts)
    # pc.printMsg(" current time: {}".format(current_time))
    ts = 2029
    

    """ Run URL Scrapers : url_scarper.py  => table@ts in (WC-DB, WP-DB) """

    # url_scraper_runner.run(ts)
    
    # """ Run Conent Scraper : content_scraper.py => table@ts in (WC-DB, WP-DB) """
    create_test_table(ts)                # Update time here: as per the name of tmp(copy) table 
    content_scraper.run(ts)          
    
    # """ Run PopICalculator => update table@ts in (WC-DB, WP-DB) """

    # popi_calculator.run(ts)

    # """ Run Tagger => update WC-DB """
    
    # tagger_simulator.run(ts)

    """ Run DomainHontessRanker => update DDS-DB """
    # th_creator.run(ts)

    # """ Query TH-table for tag_names"""
    # th_query.return_imm_children(ts, "cse")
    # th_query.return_all_descendents(ts, "cse")
    
    """ Run Newsletter Generator """
    
    """ Run Admin View Maker """
    