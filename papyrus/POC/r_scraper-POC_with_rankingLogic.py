import praw
from math import sqrt, log10
from collections import OrderedDict
from datetime import datetime, timedelta
import json

# Ranking Logic- Wilson score - "Given the ratings I have, there is a 95% chance that the “real” fraction of positive ratings is at least what?"
def _confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.281551565545   #  (1-α/2) quantile of the standard normal distribution # 80% confidence
    p = float(ups) / n

    left = p + 1/(2*n)*z*z
    right = z*sqrt(p*(1-p)/n + z*z/(4*n*n))
    under = 1+1/n*z*z

    return (left - right) / under

def confidence(ups, downs):
    if ups + downs == 0:
        return 0
    else:
        return _confidence(ups, downs)

def cynicalRank(votes, comments):
    vote_based_rank = confidence(votes)/80  #80% share of votes : confidence_range = 0-1
    comment_based_rank = log10(comments)/20 #20% share of comments : comment_score_range = 
    return vote_based_rank + comment_based_rank

# NOTE: API documentation: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html

# Credts( get from creating new app here: https://www.reddit.com/prefs/apps)
# reddit = praw.Reddit(client_id="Vv3BPojEaumOSA",                             # PERSONAL_USE_SCRIPT_14_CHARS
#                      client_secret="GWuEtPAgrMv9CpZq2aQZCBHxaYM",            # SECRET_KEY_27_CHARS
#                      user_agent="RedditScraper",                             # YOUR_APP_NAME
#                      username = "parivraajak",                               # YOUR_REDDIT_USER_NAME
#                      password = "BS@4vedi")                                  # YOUR_REDDIT_LOGIN_PASSWORD

# sub = ['programming'] 

# for s in sub:
#     subreddit = reddit.subreddit(s) 
#     # query = ['Gaming']  # put tags you want to scrape data for

#     # for item in query:
#     post_dict = {
#         "title" : [],
#         "score" : [],
#         "upvote_ratio" : [],
#         "id" : [],
#         "url" : [],
#         "comms_num": [],
#         "created" : [],
#         "body" : []
#     }
#     # comments_dict = {
#     #     "comment_id" : [],
#     #     "comment_parent_id" : [],
#     #     "comment_body" : [],
#     #     "comment_link_id" : []
#     # }
#     # for submission in subreddit.search(query,sort = "top",limit = 1):
#     for submission in subreddit.top('day',limit = 50):          #NOTE: max limit is 1000
#         post_dict["title"].append(submission.title)
#         post_dict["score"].append(submission.score)    # number of upvotes
#         post_dict["upvote_ratio"].append(submission.upvote_ratio)    # The raion of upvotes/(upvotes+downvotes)
#         post_dict["id"].append(submission.id)
#         post_dict["url"].append(submission.url)
#         post_dict["comms_num"].append(submission.num_comments)
#         post_dict["created"].append(submission.created)
#         post_dict["body"].append(submission.selftext)
#         myrank = confidence(submission.score, submission.score*(1 - submission.upvote_ratio))
#         print("{} -> {} :: MyRank = {}\n".format(submission.score,submission.upvote_ratio,myrank))
        
#         ##### Acessing comments on the post
#         # submission.comments.replace_more(limit = 1)
#         # for comment in submission.comments.list():
#         #     comments_dict["comment_id"].append(comment.id)
#         #     comments_dict["comment_parent_id"].append(comment.parent_id)
#         #     comments_dict["comment_body"].append(comment.body)
#         #     comments_dict["comment_link_id"].append(comment.link_id)
    
#     # post_comments = pd.DataFrame(comments_dict)

#     # post_comments.to_csv(s+"_comments_"+ item +"subreddit.csv")
#     # post_data = pd.DataFrame(post_dict)
#     # post_data.to_csv(s+"_"+ item +"subreddit.csv")
#     print("======================== POST ==================\n")
#     print(post_dict)



LIST = OrderedDict([
    ('compsci',['cse']),
    ('computerscience',['cse']),
    ('systems',['cse','peropt.prog']),
    ('algorithms',['algo.cse']),
    ('crypto',['crypto.cse']),
    ('cryptography',['crypto.cse'])])


if __name__ == "__main__":
    """
        Get top 1000 submissions of the listed subreddits (max_limit is 1000; should be enough)
        Hence no use of `ts` here
    """

    print(' >>>>>> Started r-scraper ................... \n')

    # csv_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/dbs/wc-db/wc_table_'+str(int(ts))+'.csv'
    # index = 1
    TOTAL_ENTRIES_YET = 0
    # Setup Client
    reddit = praw.Reddit(client_id="Vv3BPojEaumOSA",                             # PERSONAL_USE_SCRIPT_14_CHARS
                        client_secret="GWuEtPAgrMv9CpZq2aQZCBHxaYM",            # SECRET_KEY_27_CHARS
                        user_agent="RedditScraper",                             # YOUR_APP_NAME
                        username = "parivraajak",                               # YOUR_REDDIT_USER_NAME
                        password = "BS@4vedi")                                  # YOUR_REDDIT_LOGIN_PASSWORD

    for subreddit,tag_arr in LIST.items():
        print("\t ............  Subreddit: {}  .............".format(subreddit))
        sr = reddit.subreddit(subreddit)
        # for submission in sr.top('day',limit=10):                   # For testing....
        for s in sr.top('week',limit=10):              
            print("\t ============> id: {}".format(s.id))
            print("\t\t =====> is_original_content: {}".format(s.is_original_content))  # Not useful; = False for most of the cases
            print("\t\t =====> link_flair_text: {}".format(s.link_flair_text))

            print("\t\t =====> locked: {}".format(s.locked))                      
            """
                TODO: only proceed further if s.locked == False
            """
            print("\t\t =====> name: {}".format(s.name))

            print("\t\t =====> is_self: {}".format(s.is_self))
            print("\t\t =====> url: {}".format(s.url))  
            if(s.url[-4:] == ".jpg" or s.url[-4:] == ".gif"): #as reddit currentluy hosts these 2 formats only
                print("-----------------------img ({}) ------------------------".format(s.url))
            print("\t\t =====> permalink: {}".format(s.permalink))
            """
                TODO: in url:
                    1. if url ends with `.jpg' =>discard the entry
                    2. if( s.permalink in s.url)||(s.is_self == True): #i.e. if permalink is a substring of url OR submission is a selfpost (text-only)
                        => (no need to scrape) table.content = s.selftext
                        # No need to scrape for content(I know there might be links in post with some discription+link to other article he's reffering; but not worth wasting precious processing time)
                TODO: for content_scraper 
                    1. => if(table.content != NUll): dont scrape, just run clean_text on it(NOTE: dont just put "uncleaned text" there.Bc poora code hi likh dete hai log!!)
                    2. run clean_text on title & links in body => put in `weightedContent`
                    3. Where to do no scraping on HN if table.Conent is not null #Simple as that!
                        3.1. And for this case, process table.Title for table.WeightedContent
                TODO: for `clean_text()`
                    1. Dont waste urls/anchor tag's data => it does contain useful information
                    2. Not efficient at all. See how you massacard my boy:
                        * EG1#INPUT:
                                TITLE: [Pure gold] The internet explained
                                BODY:
                                    I'd like to share a masterpiece article I found by accident that explains the internet.
                                    If the author sees this, please know that I'm following you, keep being awesome.
                                    [https://explained-from-first-principles.com/internet/](https://explained-from-first-principles.com/internet/#number-encoding)"

                        * EG1#OUTPUT:
                                overflow last week good read
                        * EG2#INPUT:
                                TITLE: Matplot++: A C++ Graphics Library for Data Visualization
                                BODY:"Data visualization can help programmers and scientists identify trends in their data and efficiently communicate these 
                                    results with their peers. Modern C++ is being used for a variety of scientific applications, and this environment can benefit 
                                    considerably from graphics libraries that attend the typical design goals toward scientific data visualization. Besides the 
                                    option of exporting results to other environments, the customary alternatives in C++ are either non-dedicated libraries that 
                                    depend on existing user interfaces or bindings to other languages. Matplot++ is a graphics library for data visualization that 
                                    provides interactive plotting, means for exporting plots in high-quality formats for scientific publications, a compact syntax 
                                    consistent with similar libraries, dozens of plot categories with specialized algorithms, multiple coding styles, and supports 
                                    generic backends.
                                    &#x200B;[https://github.com/alandefreitas/matplotplusplus](https://github.com/alandefreitas/matplotplusplus)"
                        * EG2#OUTPUT:
                                WEIGHTEDCONTENT: 
                                    http githubcomalandefreitasmatplotplusplus
                                CONTENT:
                                    data visualization help programmer scientist identify trend data efficiently communicate result peer modern c used variety 
                                    scientific application environment benefit considerably graphic library attend typical design goal toward scientific data 
                                    visualization besides option exporting result environment customary alternative c either nondedicated library depend existing 
                                    user interface binding language matplot graphic library data visualization provides interactive plotting mean exporting plot 
                                    highquality format scientific publication compact syntax consistent similar library dozen plot category specialized algorithm 
                                    multiple coding style support generic backendshttps githubcomalandefreitasmatplotplusplus
            """

            print("\t\t =====> score: {}".format(s.score))
            print("\t\t =====> title: {}".format(s.title))

            print("\t\t =====> selftext: {}".format(s.selftext))

            print("\t ============ x ============= \n")
            # entry = [
            #     index,
            #     "r/"+subreddit,
            #     datetime.fromtimestamp(ts),
            #     int(ts),
            #     datetime.fromtimestamp(submission.created),
            #     submission.title,              
            #     submission.url,
            #     tag_arr,
            #     '',
            #     submission.score,
            #     submission.num_comments,
            #     '',
            #     '',
            #     submission.selftext
            #     ]
            # # print('\t\t => entry: {}'.format(entry))
            # csv_functions.putToCsv(csv_file,entry)
            # index += 1
            TOTAL_ENTRIES_YET += 1
        print("\t\t\t ====>> TOTAL_ENTRIES_YET = {}".format(TOTAL_ENTRIES_YET))

    print("\n****************** Reddit Url Scraping is Complete : TOTAL_ENTRIES_YET = {} ********************\n".format(TOTAL_ENTRIES_YET))
