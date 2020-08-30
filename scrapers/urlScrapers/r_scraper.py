import praw
from math import sqrt, log10

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
reddit = praw.Reddit(client_id="Vv3BPojEaumOSA",                             # PERSONAL_USE_SCRIPT_14_CHARS
                     client_secret="GWuEtPAgrMv9CpZq2aQZCBHxaYM",            # SECRET_KEY_27_CHARS
                     user_agent="RedditScraper",                             # YOUR_APP_NAME
                     username = "parivraajak",                               # YOUR_REDDIT_USER_NAME
                     password = "BS@4vedi")                                  # YOUR_REDDIT_LOGIN_PASSWORD

sub = ['programming'] 

for s in sub:
    subreddit = reddit.subreddit(s) 
    # query = ['Gaming']  # put tags you want to scrape data for

    # for item in query:
    post_dict = {
        "title" : [],
        "score" : [],
        "upvote_ratio" : [],
        "id" : [],
        "url" : [],
        "comms_num": [],
        "created" : [],
        "body" : []
    }
    # comments_dict = {
    #     "comment_id" : [],
    #     "comment_parent_id" : [],
    #     "comment_body" : [],
    #     "comment_link_id" : []
    # }
    # for submission in subreddit.search(query,sort = "top",limit = 1):
    for submission in subreddit.top('day',limit = 50):          #NOTE: max limit is 1000
        post_dict["title"].append(submission.title)
        post_dict["score"].append(submission.score)    # number of upvotes
        post_dict["upvote_ratio"].append(submission.upvote_ratio)    # The raion of upvotes/(upvotes+downvotes)
        post_dict["id"].append(submission.id)
        post_dict["url"].append(submission.url)
        post_dict["comms_num"].append(submission.num_comments)
        post_dict["created"].append(submission.created)
        post_dict["body"].append(submission.selftext)
        myrank = confidence(submission.score, submission.score*(1 - submission.upvote_ratio))
        print("{} -> {} :: MyRank = {}\n".format(submission.score,submission.upvote_ratio,myrank))
        
        ##### Acessing comments on the post
        # submission.comments.replace_more(limit = 1)
        # for comment in submission.comments.list():
        #     comments_dict["comment_id"].append(comment.id)
        #     comments_dict["comment_parent_id"].append(comment.parent_id)
        #     comments_dict["comment_body"].append(comment.body)
        #     comments_dict["comment_link_id"].append(comment.link_id)
    
    # post_comments = pd.DataFrame(comments_dict)

    # post_comments.to_csv(s+"_comments_"+ item +"subreddit.csv")
    # post_data = pd.DataFrame(post_dict)
    # post_data.to_csv(s+"_"+ item +"subreddit.csv")
    print("======================== POST ==================\n")
    print(post_dict)