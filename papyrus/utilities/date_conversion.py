import datetime


"""
    HN (ISO): 2020-09-11T06:28:51.000Z
    r  (IST) : 2020-09-09 05:23:05
    PH (): 2020-09-11T00:37:38.685-07:00
"""

"""  ========================= ISO (used in HN) ============================="""

def IsoToIst(s):
    """
        ISO TO IST
            * INPUT: ISO date <string> (e.g. '2020-09-11T06:28:51.000Z' )
            * OUTPUT: IST date <datetime>  (e.g. '2007-03-04 21:08:12' )
    """
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")


def IsoToDate(s):
    """
        ISO TO Date
            * INPUT: ISO date <string> (e.g. '2020-09-11T06:28:51.000Z' )
            * OUTPUT: IST date <datetime.date>  (e.g. '2007-03-04 21:08:12' )
    """
    ist_date =  datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return ist_date.date()

def HNDate(s):
    """
        Duplicate of 'IsoToDate()'
            * INPUT: ISO date <string> (e.g. '2020-09-11T06:28:51.000Z' )
            * OUTPUT: IST date <datetime.date>  (e.g. '2007-03-04 21:08:12' )
    """
    ist_date =  datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return ist_date.date()

"""  ========================= IST (used in Reddit) ============================="""

def IstToDate(s):
    """
        IST TO Date
            * INPUT: ISO date (e.g. '2007-03-04 21:08:12' )
            * OUTPUT: IST date (e.g. '2007-03-04' )
    """
    # date_time = datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S.%f')
    date_time = datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
    return date_time.date()

def IstToTime(s):
    """
        IST TO Time
            * INPUT: ISO date (e.g. '2007-03-04 21:08:12' )
            * OUTPUT: IST date (e.g. '21:08:12' )
    """
    # date_time = datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S.%f')
    date_time = datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
    return date_time.time()


def RedditDate(s):
    """
        Duplicate of 'IstToDate()'
            * INPUT: ISO date (e.g. '2007-03-04 21:08:12' )
            * OUTPUT: IST date (e.g. '2007-03-04' )
    """
    date_time = datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
    return date_time.date()

""" =================================== ISO with timegap (As used in PH ) ======================================= """

def PHDate(s):
    """
        IST TO Time
            * INPUT: ISO date (e.g. '2020-09-11T00:37:38.685-07:00' )
            * OUTPUT: IST date (e.g. '21:08:12' )
    """
    date_time = datetime.datetime.fromisoformat(s)
    return date_time.date()
