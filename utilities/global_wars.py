""" Specific to all the wc_table's url scrapers(hn_scraper,r_scraper)"""
WC_TOTAL_URL_ENTRIES = 0


""" |---------- Specific to hn_scraper.py """

HN_STORY_UPVOTE_TH  = 10
HN_SHOWHN_UPVOTE_TH = 5
HN_ASKHN_UPVOTE_TH  = 5

HN_TOTAL_ITEMS_GOT_YET = 0

""" |----------- Specific to r_scraper.py """
R_TOTAL_ITEMS_GOT_YET = 0
R_ITEM_LIMIT_PER_SUBREDDIT = 100   #FIXME: or 200?? Considering UeX: is it too less, decide after full build


""" Specific to all the wp_table's url scrapers(ph)"""
WP_TOTAL_ENTRIES_YET = 0


""" |------------- Specific to r_scraper.py """
PH_TOTAL_ITEMS_GOT_YET = 0


""" Specific to content_scraper.py"""

SQL_CONN_OPEN = 0                                       # Number of sql conn open at the moment, you're in troube if this number !=1 (both >1 or ==0 means something is fucked up)
SEMAPHORE_COUNT = 10                                    # NOTE: cant do better than this, everythin falls apart if made >10
CONNECTION_COUNT = 10                                   # NOTE: cant do better than this, everythin falls apart if made >10
# ASYNC_SERIES_CONNECTION = 2                            # Number of paraller async fetch done in series, #items_output  decrease exponantialy with each next iteration
ASYNC_SERIES_CONNECTION = 30                            # Number of paraller async fetch done in series, #items_output  decrease exponantialy with each next iteration
CS_ASYNC_REQ_TIMEOUT = 100

CS_ASYNC_ITEM_SCRAPED = 0                                # Successfully hit url & get content with async method
CS_ASYNC_URL_UNREACHABLE = 0                             # Url unreachable after retries with async
CS_ASYNC_SEMA_EXCEPTION_ERR = 0                          # Tried-Catch error when running async jobs with semaphore
CS_ITEMS_WRITTEN_DIRECT = 0                              # No need to scrape item with asycn, content already present
CS_BOYS_STILL_PLAYING = 0                                # Items sent for async which are not returned yet
CS_BOYS_PLAYING_LIMIT = 100                              # used in if gw.CS_BOYS_STILL_PLAYING % gw.CS_BOYS_PLAYING_LIMIT == 0: time.sleep(2)    

CS_SYNC_ITEM_SCRAPED = 0                                    # Successfully hit url & get content with sync method
CS_SYNC_URL_UNREACHABLE = 0                                 # Url unreachable after retries with sync
CS_SYNC_TRIED_CATCH_EXCEPTION_ERR = 0                       # Tried-Catch error when running sync get

CS_ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK = 0              # Item finally put in with content
CS_ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT = 0      # Item finally put in with Title as content

ASYNC_ITEM_SCRAPED = 0                                   # Successfully hit url & get content with async method
ASYNC_URL_UNREACHABLE = 0                                # Url unreachable after retries with async
ASYNC_SEMA_EXCEPTION_ERR = 0                             # Tried-Catch error when running async jobs with semaphore
ASYNC_ITEM_WRITTEN_DIRECT = 0                            # No need to scrape item with asycn, content already present
SYNC_ITEM_SCRAPED = 0                                    # Successfully hit url & get content with sync method
SYNC_URL_UNREACHABLE = 0                                 # Url unreachable after retries with sync
SYNC_TRIED_CATCH_EXCEPTION_ERR = 0                       # Tried-Catch error when running sync get
ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_OK = 0              # Item finally put in with content
ITEM_PUT_IN_AFTER_CONTENT_FORMATTING_NO_CONTENT = 0      # Item finally put in with Title as content
BOYS_STILL_PLAYING = 0                                   # Items sent for async which are not returned yet
