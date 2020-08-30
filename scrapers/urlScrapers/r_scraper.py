from collections import OrderedDict
from datetime import datetime, timedelta
import praw  # reddit scraper

from utilities import csv_functions,web_requests
import vault

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

    print('@[{}] >>>>>> Started r-scraper ................... => FILENAME: {}\n'.format(datetime.fromtimestamp(ts),'dbs/wc-db/table_'+str(int(ts))+'.csv'))

    csv_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/table_'+str(int(ts))+'.csv'
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
        print("\t ............  Subreddit: {}  .............".format(subreddit))
        sr = reddit.subreddit(subreddit)
        # for submission in sr.top('day',limit=10):                   # For testing....
        for submission in sr.top('week',limit=1000):              #NOTE: max limit is 1000
            entry = [
                index,
                "r/"+subreddit,
                datetime.fromtimestamp(ts),
                int(ts),
                datetime.fromtimestamp(submission.created),
                submission.title,              
                submission.url,
                tag_arr,
                '',
                submission.score,
                submission.num_comments,
                '',
                '',
                submission.selftext
                ]
            # print('\t\t => entry: {}'.format(entry))
            csv_functions.putToCsv(csv_file,entry)
            index += 1
            TOTAL_ENTRIES_YET += 1
        print("\t\t\t ====>> TOTAL_ENTRIES_YET = {}".format(TOTAL_ENTRIES_YET))

    print("\n****************** Reddit Url Scraping is Complete : TOTAL_ENTRIES_YET = {} , FILENAME: {} ********************\n".format(TOTAL_ENTRIES_YET,'dbs/wc-db/table_'+str(int(ts))+'.csv'))

