from collections import OrderedDict
from datetime import datetime, timedelta
import json
import time
import praw  # reddit scraper
import sqlite3

from utilities import csv_functions, text_actions, web_requests, date_conversion
import vault
from utilities import print_in_color as pc

# NOTE: API documentation: https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html

""" < subreddit(key),[tag_arr](value)>
    Many -to- One mapping : as why scrape the same /r for new tag
"""
LIST = OrderedDict([
    ('compsci',['cse']),
    ('computerscience',['cse']),
    ('systems',['cse','peropt.prog']),
    ('algorithms',['algo.cse']),
    ('crypto',['crypto.cse']),
    ('cryptography',['crypto.cse']),
    ('logic',['logic.cse']),
    ('compilers',['compiler']),
    ('osdev',['os']),
    ('kernel',['linux.os']),
    ('ReverseEngineering',['reveng.prog']),
    ('bigdata',['bigdata']),
    ('datasets',['dataset']),
    ('MachineLearning',['ml']),
    ('artificial',['ai']),
    ('LanguageTechnology',['nlp']),
    ('computervision',['cvis']),
    ('datamining',['dataming']),
    ('visualization',['datavis.ds']),
    ('dataisbeautiful',['datavis.ds']),
    ('statistics',['stats']),
    ('programming',['prog']),
    ('coding',['prog']),
    ('softwaredevelopment',['prog','tools.prog','devpract.prog']),
    ('SoftwareEngineering',['prog']),
    ('asm',['assem']),
    ('C_Programming',['c']),
    ('c_language',['c']),
    ('cpp',['cpp']),
    ('Cplusplus',['cpp']),
    ('Python',['python']),
    ('scala',['scala']),
    ('erlang',['erlang']),
    ('haskell',['haskell']),
    ('java',['java']),
    ('javascript',['javascript']),
    ('lisp',['lisp']),
    ('perl',['perl']),
    ('PHP',['php']),
    ('ruby',['ruby']),
    ('dotnet',['dotnet']),
    ('Kotlin',['kotlin']),
    ('rails',['ror']),
    ('django',['django']),
    ('reactjs',['reactjs']),
    ('aws',['aws']),
    ('Database',['dbs']),
    ('webdev',['webd.prog']),
    ('compsec',['compsec']),
    ('websec',['websec']),
    ('computergraphics',['cmpgr']),
    ('web_design',['webdes']),
    ('tinycode',['devpract.prog']),
    ('gamedev',['gamedev']),
    ('opensource',['opensrc']),
    ('AskComputerScience',['query']),
    ('cscareerquestions',['advise.carr']),
    ('programmingchallenges',['codingchlg']),
    ('technology',['technews']),
    ('atheism',['phil']),
    ('math',['maths']),
    ('mathematics',['maths']),
    ('statistics',['stats']),
    ('Bitcoin',['bitcoin'])
])

def run(ts):
    """
        Get top 1000 submissions of the listed subreddits (max_limit is 1000; should be enough)
        Hence no use of `ts` here
    """
    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    pc.printSucc('@[{}] >>>>>> Started r-scraper ................... => TABLE: {}\n'.format(datetime.fromtimestamp(ts),wc_table))    
    pc.printMsg("\t -------------------------------------- < r_SCRAPER: DB Connection Opened > ---------------------------------------------\n")
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < r_SCRAPER: DB Connection Opened > ---------------------------------------------\n")
    stratTime = time.time()

    # csv_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    index = 1
    TOTAL_ENTRIES_YET = 0
    # Setup Client
    reddit = praw.Reddit(
                    client_id= vault.R_CLIENT_ID,                                 # PERSONAL_USE_SCRIPT_14_CHARS
                    client_secret= vault.R_CLIENT_SECRET,                         # SECRET_KEY_27_CHARS
                    user_agent= vault.R_USER_AGENT,                               # YOUR_APP_NAME
                    username =  vault.R_USERNAME,                                 # YOUR_REDDIT_USER_NAME
                    password = vault.R_PASSWORD)                                  # YOUR_REDDIT_LOGIN_PASSWORD

    for subreddit,tag_arr in LIST.items():
        pc.printWarn("\t ............  Subreddit: {}  .............".format(subreddit))
        sr = reddit.subreddit(subreddit)
        # for submission in sr.top('day',limit=10):                   # For testing....
        # for submission in sr.top('year',limit=1000):                #remove this & uncomemnt below line
        for submission in sr.top('week',limit=1000):              #NOTE: max limit is 1000
            #Check1: if the post is unlocked by mods
            content = ''
            
            """ Fixing permalink type urls """
            url = submission.url
            if(url[:2]== '/r'):
                url = "https://www.reddit.com" + url 
            if(submission.locked == False):
                #Check2: if post is just an image, discard it
                if(submission.url[-4:] != ".jpg" and submission.url[-4:] != ".png"  and submission.url[-4:] != ".gif"):  #as reddit currentluy hosts .png & .gif only
                    # if permalink is a substring of url OR submission is a selfpost (text-only) => no need to scrape  
                    # NOTE: I know there might be links in post with some discription+link to other article he's reffering; but not worth wasting precious processing time
                    if((submission.permalink in submission.url) or (submission.is_self == True)):
                        content = submission.selftext
                    entry = [
                        index,
                        "r/"+subreddit,
                        datetime.fromtimestamp(ts).date(),
                        int(ts),
                        date_conversion.RedditDate(str(datetime.fromtimestamp(submission.created))),
                        submission.title,              
                        url,
                        json.dumps(tag_arr),
                        '',
                        submission.score,
                        submission.num_comments,
                        '',
                        '',
                        text_actions.clean_text(content)
                    ]
                    # csv_functions.putToCsv(csv_file,entry)
                    c.execute('INSERT INTO ' + wc_table + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', entry)
                    index += 1
                    TOTAL_ENTRIES_YET += 1
        pc.printMsg("\t\t\t ====>> TOTAL_ENTRIES_YET = {}".format(TOTAL_ENTRIES_YET))
    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < r_SCRAPER: DB Connection Closed > ---------------------------------------------\n")
    pc.printSucc("\n\n***************************** Reddit Url Scraping is Complete. TABLE: {} *******************".format(wc_table))
    pc.printSucc("| \t\t TOTAL URLS FETCHED                    \t\t | \t\t {} \t\t |".format(TOTAL_ENTRIES_YET))
    pc.printSucc("| \t\t TIME TAKEN FOR URL SCRAPING           \t\t | \t\t {}  \t\t |".format(int(endTime - stratTime)))
    pc.printSucc("*************************************************************************************************\n\n")
