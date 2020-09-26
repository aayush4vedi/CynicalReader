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
    ('compsci',['gen_cse']),
    ('computerscience',['gen_cse']),
    ('distributed',['distribut_sys']),
    ('datastructures',['data_struct']),
    ('algorithms',['algo_dsa']),
    ('cpp_questions',['algo_dsa']),
    ('GAMETHEORY',['gametheory']),
    ('Discretemathematics',['disco']),
    ('crypto',['crypto_cse']),
    ('cryptography',['crypto_cse']),
    ('logic',['logic']),
    ('computerarchitecture',['comparch']),
    ('compilers',['compiler']),
    ('Network',['network']),
    ('ReverseEngineering',['revengg']),
    ('osdev',['osdev']),
    ('Android',['android']),
    ('MacOS',['mac']),
    ('osx',['mac']),
    ('windows',['windows']),
    ('linux',['linux']),
    ('kernel',['linux']),
    ('linuxdev',['linux']),
    ('linuxquestions',['linux']),
    ('Ubuntu',['linux']),
    ('hacking',['hacking']),
    ('HowToHack',['hacking']),
    ('Hacking_Tutorials',['hacking']),
    ('hackers',['hacking']),
    ('robotics',['robotics']),
    ('arduino',['robotics']),
    ('virtualreality',['arvr']),
    ('augmentedreality',['arvr']),
    ('IOT',['iot']),
    ('computervision',['compvision']),
    ('opencv',['compvision']),
    ('imageprocessing',['imgprocess']),
    ('dip',['imgprocess']),
    ('datamining',['datamine']),
    ('textdatamining',['datamine']),
    ('MachineLearning',['gen_ml']),
    ('learnmachinelearning',['gen_ml']),
    ('ResearchML',['gen_ml']),
    ('neuralnetworks',['gen_ml']),
    ('neuralnetworks',['ann','dl']),        # yep, array indeed
    ('NeuralNetwork',['ann']),
    ('deeplearning',['dl']),
    ('DeepLearningPapers',['dl']),
    ('deeplearners',['dl']),
    ('datascience',['gen_ds']),
    ('learndatascience',['gen_ds']),
    ('Database',['database']),
    ('datasets',['dataset']),
    ('statistics',['statistics']),
    ('AskStatistics',['statistics']),
    ('Rlanguage',['rlang']),
    ('rstats',['rlang']),
    ('matlab',['matlab']),
    ('scala',['scala']),
    ('scikit_learn',['scikit']),
    ('JupyterNotebooks',['jupyternote']),
    ('kaggle',['kaggle']),
    ('datacleaning',['datacleaning']),
    ('NLP',['nlp']),
    ('LanguageTechnology',['nlp']),
    ('bigdata',['gen_bigdata']),
    ('apachespark',['spark']),
    ('hadoop',['hadoop']),
    ('visualization',['gen_datavis']),
    ('dataisbeautiful',['gen_datavis']),
    ('tableau',['tableau']),
    ('excel',['excel']),
    ('ExcelTips',['excel']),
    ('artificial',['ai']),
    ('ArtificialInteligence',['ai']),
    ('softwaredevelopment',['gen_prog','devpract']),
    ('programming',['gen_prog']),
    ('coding',['gen_prog']),
    ('SoftwareEngineering',['gen_prog']),
    ('ProgrammingLanguages',['prog']),
    ('learnprogramming',['prog']),
    ('functionalprogramming',['prog']),
    ('asm',['asm']),
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
    ('rust',['rust']),
    ('dotnet',['dotnet']),
    ('Kotlin',['kotlin']),
    ('html',['HTML']),
    ('html',['html5']),
    ('css',['css']),
    ('rails',['ror']),
    ('django',['django']),
    ('reactjs',['reactjs']),
    ('git',['git']),
    ('github',['git']),
    ('gitlab',['git']),
    ('virtualization',['virtualn']),
    ('browsers',['browser']),
    ('aws',['aws']),
    ('AWS_cloud',['aws']),
    ('AZURE',['azure']),
    ('azuredevops',['azure']),
    ('kubernetes',['k8s']),
    ('k8s',['k8s']),
    ('docker',['docker']),
    ('GCP',['gcp']),
    ('vim',['vim']),
    ('neovim',['vim']),
    ('vim_magic',['vim']),
    ('emacs',['emacs']),
    ('appdev',['gen_appdev']),
    ('AppDevelopment',['gen_appdev']),
    ('iosdev',['iosdev']),
    ('iOSProgramming',['iosdev']),
    ('androiddev',['androiddev']),
    ('devops',['gen_devops']),
    ('netsec',['infosec']),
    ('compsec',['compsec']),
    ('websec',['websec']),
    ('computergraphics',['compgphix']),
    ('web_design',['webdes']),
    ('UI_Design',['ui']),
    ('UI_programming',['ui']),
    ('UXDesign',['ux']),
    ('UXResearch',['ux']),
    ('UX_Design',['ux']),
    ('webdev',['webd']),
    ('softwaretesting',['sdt']),
    ('systems',['system']),
    ('tinycode',['devpract']),
    ('api',['api']),
    ('gamedev',['gamedev']),
    ('programmingchallenges',['codingchlg']),
    ('opensource',['opensrc']),
    ('AskComputerScience',['prog_query','tech_query']),
    ('forhire',['jobs']),
    ('cscareerquestions',['carr_query']),
    ('interviewpreparations',['interviewprep']),
    ('csinterviewproblems',['interviewprep']),
    ('interviews',['interviewexp']),
    ('technology',['technews']),
    ('TrueReddit',['technews']),
    ('wikipedia',['technews']),
    ('geek',['technews']),
    ('skeptic',['community']),
    ('blog',['tech_blog']),
    ('COPYRIGHT',['tech_law']),
    ('noip',['tech_law']),
    ('cognitivescience',['cogsci']),
    ('torrents',['torrent']),
    ('books',['book']),
    ('scifi',['book']),
    ('bookclub',['book']),
    ('writing',['write']),
    ('atheism',['phil']),
    ('philosophy',['phil']),
    ('history',['history']),
    ('AskHistorians',['history']),
    ('business',['gen_business']),
    ('Flipping',['gen_business']),
    ('freelance',['freelance']),
    ('Upwork',['freelance']),
    ('SaaS',['saas']),
    ('SideProject',['sideproj']),
    ('marketing',['market']),
    ('SEO',['seo']),
    ('bigseo',['seo']),
    ('SEO_Digital_Marketing',['seo']),
    ('science',['gen_science']),
    ('askscience',['sci_query']),
    ('AskPhysics',['sci_query']),
    ('chemistry',['chemistry']),
    ('biology',['biology']),
    ('medicine',['medicine']),
    ('neuroscience',['neuroscience']),
    ('geology',['geology']),
    ('environment',['env']),
    ('Health',['health']),
    ('Physics',['gen_physics']),
    ('space',['astro']),
    ('aerospace',['astro']),
    ('quantum',['quantum']),
    ('QuantumPhysics',['quantum']),
    ('energy',['nuclear']),
    ('FluidMechanics',['fluid_mech']),
    ('engineering',['gen_engg']),
    ('electronics',['engg_ece']),
    ('ECE',['engg_ece']),
    ('ElectricalEngineering',['engg_electric']),
    ('AskEngineers',['engg_query']),
    ('LearnEngineering',['engg_query']),
    ('AskElectronics',['engg_query']),
    ('MechanicalEngineering',['engg_mech']),
    ('EngineeringStudents',['engg_student']),
    ('rocketry',['rocket']),
    ('aviation',['rocket']),
    ('nasa',['rocket']),
    ('spacex',['rocket']),
    ('aerodynamics',['rocket']),
    ('StructuralEngineering',['engg_struct']),
    ('3Dprinting',['threedprint']),
    ('math',['gen_maths']),
    ('mathematics',['gen_maths']),
    ('calculus',['calculus']),
    ('DifferentialEquations',['calculus']),
    ('Algebra',['algebra']),
    ('GraphTheory',['graphtheory']),
    ('Economics',['economics']),
    ('economy',['economics']),
    ('finance',['finance']),
    ('personalfinance',['finance']),
    ('Accounting',['accounting']),
    ('invest',['invest']),
    ('invest',['invest']),
    ('BlockchainStartups',['gen_blockchain']),
    ('CryptoCurrency',['crypto_fin']),
    ('Bitcoin',['bitcoin']),
    ('BitcoinBeginners',['bitcoin']),
    ('bitcointrading',['bitcoin']),
    ('BitcoinDiscussion',['bitcoin'])
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
    startTime = time.time()

    blob_pages = ['.jpg', '.png', '.gif', '.mp3', '.mp4'] # these give blob data; no point in scraping them

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
        ENTRIES_IN_THIS_SUBRDDIT = 0
        for submission in sr.top('week',limit=200):              #NOTE: max limit is 1000
            #Check1: if the post is unlocked by mods
            content = ''
            
            """ Fixing permalink type urls """
            url = submission.url
            if(url[:2]== '/r'):
                url = "https://www.reddit.com" + url 
            if(submission.locked == False):
                #Check2: if post is just an image, discard it
                if submission.url[-4:] not in blob_pages:  #as reddit currentluy hosts .png & .gif only
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
                    ENTRIES_IN_THIS_SUBRDDIT += 1
        pc.printMsg("\t\t\t\t\t ====> ENTRIES_IN_THIS_SUBRDDIT = {} \t\t\t ====>> TOTAL_ENTRIES_YET = {}".format(ENTRIES_IN_THIS_SUBRDDIT,TOTAL_ENTRIES_YET))
    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < r_SCRAPER: DB Connection Closed > ---------------------------------------------\n")
    pc.printSucc("\n\n***************************** Reddit Url Scraping is Complete. TABLE: {} *******************".format(wc_table))
    pc.printSucc("| \t\t TOTAL URLS FETCHED                    \t\t | \t\t {} \t\t |".format(TOTAL_ENTRIES_YET))
    pc.printSucc("| \t\t TIME TAKEN FOR URL SCRAPING           \t\t | \t\t {}  \t\t |".format(round((endTime - startTime),5)))
    pc.printSucc("*************************************************************************************************\n\n")
