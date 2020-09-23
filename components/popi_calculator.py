import time
import datetime
import traceback
import logging
import collections

import sqlite3

from utilities import print_in_color as pc



""" ======================================================= Utility Functions : START  ======================================================="""

def GetLastSevenDays(ts):
    """
        returns array with last 7 days dates(including today's): ['2020-09-12','2020-09-11',...]
    """
    days = [str(int(ts))]
    for i in range(6):
        prev_day = datetime.datetime.fromtimestamp(int(days[-1])) + datetime.timedelta(days=-1)
        prev_day = prev_day.timestamp()
        days.append(str(int(prev_day)))
    
    days_arr =[]
    for d in days:
        date = datetime.datetime.fromtimestamp(int(d)).date()
        days_arr.append(str(date))

    # for day in days_arr:
    #     print(day)
    return days_arr
    

class PopiItem:
    """
        Object to be used while making Hashmap for daily & weekly max num of comments & upvotes
        For DailyMaxMap: `Date` = `CreationDate`
        For WeeklyMaxMap: `Date` = `ProcessingDate`
    """
    def __init__(self, SourceSite, Date):
        self.SourceSite = SourceSite
        self.Date = Date


""" ======================================================= Utility Functions : END    ======================================================="""


""" ======================================================= Main Functions : START ======================================================="""


def CalculatePopi(upvotes, comments, max_upvotes_day, max_comments_day, max_upvotes_week, max_comments_week, creation_date, first_day_of_week,source_site):

    date_i = datetime.datetime.strptime(creation_date, '%Y-%m-%d')
    date_0 = datetime.datetime.strptime(first_day_of_week, '%Y-%m-%d')
    days_life_since_day_0 = min(max((date_i - date_0).days, 0),7)       # now it will be in [0,7] .Needed as some APIs return months old posts :(

    # print("\t\t creation_date    -> {}".format(creation_date))
    # print("\t\t\t upvotes    -> {}".format(upvotes))
    # print("\t\t\t comments    -> {}".format(comments))
    # print("\t\t\t max_upvotes_day    -> {}".format(max_upvotes_day))
    # print("\t\t\t max_comments_day    -> {}".format(max_comments_day))
    # print("\t\t\t max_upvotes_week    -> {}".format(max_upvotes_week))
    # print("\t\t\t max_comments_week    -> {}".format(max_comments_week))
    # print("\t\t\t days_life_since_day_0    -> {}".format(days_life_since_day_0))
    # print("\t\t\t date_i    -> {}".format(date_i))
    # print("\t\t\t date_0    -> {}".format(date_0))

    """
    #NOTE: for now d(source damping factor)
        HN: D = 0.8
        r : D = 0.8
        PH: D = 0.8

        DailyWeightage:  DW = 0.3

        WeeklyWeightage: WW = 0.5

        TimeWildcard:    TW = 0.2
        #TODO: put conditions to filter out 'source_site' & assign these constants accordingly
        # if str(source_site).find("r/programming") != -1:
            #     print(" \t\t\t row: {}".format(row))
    """ 

    D = 0.8
    DW = 0.3
    WW = 0.6
    TW = 0.1
    UW = 0.6
    CW = 0.5

    popi = (DW)*(UW*(upvotes/max(max_upvotes_day,1)) +  CW*(comments/max(max_comments_day,1)))                  # x = max(x,1) to avoid 'Dividing by 0' error
    popi += (WW)*(UW*(upvotes/max(max_upvotes_week,1)) + CW*(comments/max(max_comments_week,1)))
    popi += TW*(days_life_since_day_0/7)

    popi = D*popi
    # print("\t\t popi    -> {}".format(popi))
    return popi


def run_wc(ts):
    """
        runs on the table(wc_ts) in wc.db & updates PopI column in it
    """

    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    pc.printSucc('@[{}] >>>>>> Started  PopICalculator@wc ................... => TABLE: {}\n'.format(datetime.datetime.fromtimestamp(ts),wc_table))
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < PopICalculator@wc : DB Connection Opened > ---------------------------------------------\n")
    pc.printWarn("\tRunning PopiCalculator for wc ....... \t NOW: {}".format(time.strftime("%H:%M:%S", time.localtime())))
    pc.printWarn("\t\t. .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .")
    startTime = time.time()

    days = GetLastSevenDays(ts)

    """ Initialize both maps(weekly & daily): key = PopiItem, Value = (max_upvotes, max_comments) """

    DailyMaxMap = collections.defaultdict(list)
    WeeklyMaxMap = collections.defaultdict(list)

    q = "select * from " + wc_table
    rows_head = c.execute(q)
    rows = rows_head.fetchall()
    for row in rows:
        """
            ============= row is an array with indices: 
            ID(0),SourceSite(1),ProcessingDate(2),ProcessingEpoch(3),CreationDate(4),Title(5),Url(6),
            SourceTags(7),ModelTags(8),NumUpvotes(9),NumComments(10),PopI(11),WeightedContent(12),Content(13)
        """
        popi_item_daily = PopiItem(row[1],row[4])
        popi_item_weekly = PopiItem(row[1],row[2])

        # for daily max
        if popi_item_daily in DailyMaxMap:
            max_upvotes_day = DailyMaxMap[popi_item_daily][0]
            max_comments_day = DailyMaxMap[popi_item_daily][1]
        else:
            q = "select max(NumUpvotes) from " + wc_table + " where SourceSite = ? and CreationDate = ?"
            d = (row[1],row[4])
            max_upvotes_day = c.execute(q,d)
            max_upvotes_day = c.fetchone()[0]
            q = "select max(NumComments) from " + wc_table + " where SourceSite = ? and CreationDate = ?"
            max_comments_day = c.execute(q,d)
            max_comments_day = c.fetchone()[0]
            DailyMaxMap[popi_item_daily] = (max_upvotes_day,max_comments_day)

        # For weekly max
        if popi_item_weekly in WeeklyMaxMap:
            max_upvotes_week = WeeklyMaxMap[popi_item_daily][0]
            max_comments_week = WeeklyMaxMap[popi_item_daily][1]
        else:
            q = "select max(NumUpvotes) from " + wc_table + " where SourceSite = ? and ProcessingDate = ?"
            d = (row[1],row[2])
            max_upvotes_week = c.execute(q,d)
            max_upvotes_week = c.fetchone()[0]
            q = "select max(NumComments) from " + wc_table + " where SourceSite = ? and ProcessingDate = ?"
            max_comments_week = c.execute(q,d)
            max_comments_week = c.fetchone()[0]
            WeeklyMaxMap[popi_item_weekly] = (max_upvotes_week,max_comments_week)

        popI = CalculatePopi(row[9],row[10],max_upvotes_day, max_comments_day, max_upvotes_week, max_comments_week,row[4],days[6],row[1])
        popI = round(popI,10)
        # pc.printWarn(" \t\t [wc_popi calculation] <ID={}><Source={}> ...................... PopI = {}".format(row[0],row[1],popI))
        # pc.printMsg("\t\t\t\t ........................ Updated PopI in wc_table..............")
        query = 'update ' + wc_table + ' set PopI = ? where ID = ? and SourceSite = ?'
        data = (popI,row[0],row[1])
        c.execute(query,data)

    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < PopICalculator@wc: DB Connection Closed > ---------------------------------------------\n")
    pc.printWarn("\t\t ---------------> TIME TAKEN FOR PopICalculator@wc    =>  {} => TABLE: {}\n".format(round((endTime - startTime),5),wc_table))

def run_wp(ts):
    """
        runs on the table(wp_ts) in wp.db & updates PopI column in it
    """

    wp_db = 'dbs/wp.db'
    wp_table = 'wp_' + str(int(ts))
    pc.printSucc('@[{}] >>>>>> Started  PopICalculator@wp ................... => TABLE: {}\n'.format(datetime.datetime.fromtimestamp(ts),wp_table))
    conn = sqlite3.connect(wp_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- <  PopICalculator@wp : DB Connection Opened > ---------------------------------------------\n")
    startTime = time.time()
    pc.printWarn("\tRunning PopiCalculator for wp ....... \t NOW: {}".format(time.strftime("%H:%M:%S", time.localtime())))
    pc.printWarn("\t\t. .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .")

    days = GetLastSevenDays(ts)

    """ Initialize both maps(weekly & daily): key = PopiItem, Value = (max_upvotes, max_comments) """

    DailyMaxMap = collections.defaultdict(list)
    WeeklyMaxMap = collections.defaultdict(list)

    q = "select * from " + wp_table
    rows_head = c.execute(q)
    rows = rows_head.fetchall()
    for row in rows:
        """
           * ============= row is an array with indices: 
            (ID(0), SourceSite(1), ProcessingDate(2),ProcessingEpoch(3),CreationDate(4),Title(5), Url(6),
            ThumbnailUrl(7),SourceTags(8),NumUpvotes(9),NumComments(10),PopI(11),Content(12))
        """
        popi_item_daily = PopiItem(row[1],row[4])
        popi_item_weekly = PopiItem(row[1],row[2])

        # for daily max
        if popi_item_daily in DailyMaxMap:
            max_upvotes_day = DailyMaxMap[popi_item_daily][0]
            max_comments_day = DailyMaxMap[popi_item_daily][1]
        else:
            q = "select max(NumUpvotes) from " + wp_table + " where SourceSite = ? and CreationDate = ?"
            d = (row[1],row[4])
            max_upvotes_day = c.execute(q,d)
            max_upvotes_day = c.fetchone()[0]
            q = "select max(NumComments) from " + wp_table + " where SourceSite = ? and CreationDate = ?"
            max_comments_day = c.execute(q,d)
            max_comments_day = c.fetchone()[0]
            DailyMaxMap[popi_item_daily] = (max_upvotes_day,max_comments_day)

        # For weekly max
        if popi_item_weekly in WeeklyMaxMap:
            max_upvotes_week = WeeklyMaxMap[popi_item_daily][0]
            max_comments_week = WeeklyMaxMap[popi_item_daily][1]
        else:
            q = "select max(NumUpvotes) from " + wp_table + " where SourceSite = ? and ProcessingDate = ?"
            d = (row[1],row[2])
            max_upvotes_week = c.execute(q,d)
            max_upvotes_week = c.fetchone()[0]
            q = "select max(NumComments) from " + wp_table + " where SourceSite = ? and ProcessingDate = ?"
            max_comments_week = c.execute(q,d)
            max_comments_week = c.fetchone()[0]
            WeeklyMaxMap[popi_item_weekly] = (max_upvotes_week,max_comments_week)

        popI = CalculatePopi(row[9],row[10],max_upvotes_day, max_comments_day, max_upvotes_week, max_comments_week,row[4],days[6],row[1])
        # pc.printWarn(" \t\t [wc_popi calculation] <ID={}><Source={}> ...................... PopI = {}".format(row[0],row[1],popI))
        # pc.printMsg("\t\t\t\t ........................ Updated PopI in wp_table..............")
        query = 'update ' + wp_table + ' set PopI = ? where ID = ? and SourceSite = ?'
        data = (popI,row[0],row[1])
        c.execute(query,data)

    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < PopICalculator@wp: DB Connection Closed > ---------------------------------------------\n")
    pc.printWarn("\t\t ---------------> TIME TAKEN FOR PopICalculator@wp    =>  {} => TABLE: {}\n".format(round((endTime - startTime),5),wp_table))



def run(ts):
    startTime = time.time()

    try:
        run_wc(ts)
    except Exception as e:
        pc.printErr(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in Running PopICalculator for wc table xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\t>>> Error = {}".format(str(e)))
        logging.error(traceback.format_exc())
        pass

    try:
        run_wp(ts)
    except Exception as e:
        pc.printErr(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in Running PopICalculator for wc table xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\t>>> Error = {}".format(str(e)))
        logging.error(traceback.format_exc())
        pass
    
    endTime = time.time()

    pc.printSucc("**************************** PopI Calculation is Done for wc & wp ********************************\n\n")
    pc.printWarn("| \t\t TIME TAKEN FOR PopICalculators-both     \t\t | \t\t {}  \t\t |".format(round((endTime - startTime),5)))
    pc.printSucc("*************************************************************************************************\n\n")





""" ======================================================= Main Functions : END   ======================================================="""



""" ====================================== Few Case Studies :START ==================================== 
---------> Case Study #1.
(A)
creation_date    -> 2020-09-13
creation_date    -> HN/show
    upvotes    -> 27
    comments    -> 3
    max_upvotes_day    -> 27
    max_comments_day    -> 3
    max_upvotes_week    -> 401
    max_comments_week    -> 266
    days_life_since_day_0    -> 6
popi    -> 0.35466971668572933
[wc_popi calculation] <ID=35><Source=HN/show> ...................... PopI = 0.35466971668572933

(B)
creation_date    -> 2020-09-10
creation_date    -> HN/show
    upvotes    -> 122
    comments    -> 32
    max_upvotes_day    -> 197
    max_comments_day    -> 48
    max_upvotes_week    -> 401
    max_comments_week    -> 266
    days_life_since_day_0    -> 3
popi    -> 0.31995650734238407
[wc_popi calculation] <ID=247><Source=HN/show> ...................... PopI = 0.31995650734238407




====================================== Few Case Studies :END ==================================== """