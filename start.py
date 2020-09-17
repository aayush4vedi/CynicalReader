import time
from datetime import datetime
import csv

from scrapers import url_scraper_runner, content_scraper
from components import popi_calculator, tagger_simulator
from utilities import print_in_color as pc

if __name__ == '__main__':
    
    ts = datetime.now().timestamp()
    current_time = datetime.fromtimestamp(ts)
    
    pc.printMsg(" current time: {}".format(current_time))

    """ Run URL Scrapers : url_scarper.py  => table@ts in (WC-DB, WP-DB) """

    url_scraper_runner.run(ts)
    
    """ Run Conent Scraper : content_scraper.py => table@ts in (WC-DB, WP-DB) """

    content_scraper.run(ts)        
    
    """ Run PopICalculator => update table@ts in (WC-DB, WP-DB) """

    popi_calculator.run(ts)

    """ Run ManchTagger(simulator for now) => update WC-DB """
    
    tagger_simulator.run(ts)

    """ Run DomainHontessRanker => update DDS-DB """
    
    """ Run Newsletter Generator """
    
    """ Run Admin View Maker """
    
    
