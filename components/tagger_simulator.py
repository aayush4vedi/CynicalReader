import time
import json
from datetime import datetime
import logging

import sqlite3
from random import randrange, uniform

from utilities import print_in_color as pc

"""
#TODO: take into account both: modelTag(conf value) & sourceTag(conf =100%) with diff weights ofc

"""

"""  (tag_name, CONFIDENCE_THRESHOLD) """

tags_threshold = {           
        'cse' : 0.95,
        'algo.cse' : 0.95,
        'law.cse' : 0.95,
        'crypto.cse' : 0.95,
        'hardware' : 0.95,
        'plt.cse' : 0.95,
        'frme.cse' : 0.95,
        'logic.cse' : 0.95,
        'compiler' : 0.95,
        'netwrk' : 0.95,
        'os' : 0.95,
        'ios.os' : 0.95,
        'android.os' : 0.95,
        'mac.os' : 0.95,
        'windows.os' : 0.95,
        'linux.os' : 0.95,
        'unix.os' : 0.95,
        'reveng.prog' : 0.95,
        'ml' : 0.95,
        'ai' : 0.95,
        'bigdata' : 0.95,
        'dataset' : 0.95,
        'dsc' : 0.95,
        'ml' : 0.95,
        'ai' : 0.95,
        'nlp' : 0.95,
        'cvis' : 0.95,
        'dataming' : 0.95,
        'database' : 0.95,
        'datavis.ds' : 0.95,
        'stats' : 0.95,
        'prog' : 0.95,
        'proglng' : 0.95,
        'plt.cse' : 0.95,
        'assem' : 0.95,
        'c' : 0.95,
        'cpp' : 0.95,
        'golang' : 0.95,
        'python' : 0.95,
        'scala' : 0.95,
        'elixir' : 0.95,
        'elm' : 0.95,
        'erlang' : 0.95,
        'fortran' : 0.95,
        'haskell' : 0.95,
        'java' : 0.95,
        'javascript' : 0.95,
        'lisp' : 0.95,
        'perl' : 0.95,
        '' : 0.95,
        'objc' : 0.95,
        'perl' : 0.95,
        'php' : 0.95,
        'ruby' : 0.95,
        'rust' : 0.95,
        'swift' : 0.95,
        'd' : 0.95,
        'chash' : 0.95,
        'fhash' : 0.95,
        'dotnet' : 0.95,
        'html' : 0.95,
        'kotlin' : 0.95,
        'css' : 0.95,
        'frm.prog' : 0.95,
        'ror' : 0.95,
        'django' : 0.95,
        'reactjs' : 0.95,
        'nodejs' : 0.95,
        'tools.prog' : 0.95,
        'vcs.prog' : 0.95,
        'api.prog' : 0.95,
        'virtualn.prog' : 0.95,
        'editor.prog' : 0.95,
        'browser' : 0.95,
        'aws' : 0.95,
        'dbs' : 0.95,
        'webd.prog' : 0.95,
        'appd.prog' : 0.95,
        'android' : 0.95,
        'ios' : 0.95,
        'sofrel.prog' : 0.95,
        'debugging' : 0.95,
        'testing.prog' : 0.95,
        'devops' : 0.95,
        'security' : 0.95,
        'compsec' : 0.95,
        'websec' : 0.95,
        'privacy' : 0.95,
        'crypto.cse' : 0.95,
        'design' : 0.95,
        'cmpgr' : 0.95,
        'webdes' : 0.95,
        'scaling.prog' : 0.95,
        'peropt.prog' : 0.95,
        'devpract.prog' : 0.95,
        'gamedev' : 0.95,
        'codingchlg' : 0.95,
        'law.cse' : 0.95,
        'opensrc' : 0.95,
        'os' : 0.95,
        'ios.os' : 0.95,
        'android.os' : 0.95,
        'mac.os' : 0.95,
        'windows.os' : 0.95,
        'linux.os' : 0.95,
        'unix.os' : 0.95,
        'query' : 0.95,
        'career' : 0.95,
        'advise.carr' : 0.95,
        'codingchlg' : 0.95,
        'technews' : 0.95,
        'discuss' : 0.95,
        'query' : 0.95,
        'community' : 0.95,
        'person' : 0.95,
        'edu' : 0.95,
        'cogsci' : 0.95,
        'art' : 0.95,
        'book' : 0.95,
        'hist.it' : 0.95,
        'phil' : 0.95,
        'startup' : 0.95,
        'selfproj' : 0.95,
        'opensrc' : 0.95,
        'law.cse' : 0.95,
        'science' : 0.95,
        'maths' : 0.95,
        'stats' : 0.95,
        'crypto.cse' : 0.95,
        'logic' : 0.95,
        'finance' : 0.95,
        'bitcoin' : 0.95,
        'crypto.fin' : 0.95
}

#TODO: replace with real model
def SimulatorApi(content, Weighted_content):
    conf_arr = []
    i = 0
    for tag in tags_threshold:
        # conf_arr.append((tags,uniform(0,1)))
        #Trying to uniformly distribute the randomization
        if i%5 == 0:
            conf_arr.append((tag,uniform(0.95,1)))
        elif i%7 == 0:
            conf_arr.append((tag,uniform(0,0.3)))
        elif i%9 == 0:
            conf_arr.append((tag,uniform(0.7,1)))
        elif i%10 == 0:
            conf_arr.append((tag,uniform(0.4,0.8)))
        else:
            conf_arr.append((tag,uniform(0,1)))
        i += 1
    return conf_arr


def update_modelTags(ts):
    """
        runs on the table(wc_ts) in wc.db & update ModelTag
    """
    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    pc.printSucc('@[{}] >>>>>> Started  TaggerSimulator@wc ................... => TABLE: {}\n'.format(datetime.fromtimestamp(ts),wc_table))
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < TaggerSimulator@wc : DB Connection Opened > ---------------------------------------------\n")
    pc.printWarn("\tRunning PopiCalculator for wc ....... \t NOW: {}".format(time.strftime("%H:%M:%S", time.localtime())))
    pc.printWarn("\t\t. .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .")
    startTime = time.time()

    q = "select * from " + wc_table
    rows_head = c.execute(q)
    rows = rows_head.fetchall()
    for row in rows:
        """
            ============= row is an array with indices: 
            ID(0),SourceSite(1),ProcessingDate(2),ProcessingEpoch(3),CreationDate(4),Title(5),Url(6),
            SourceTags(7),ModelTags(8),NumUpvotes(9),NumComments(10),PopI(11),WeightedContent(12),Content(13)
        """
        modelTags = []

        #TODO: call actual Api here, when model is ready
        pc.printMsg("\t <ID = {}><src= {} > [Tagger] Start................ ".format(row[0],row[1]))

        conf_arr = SimulatorApi(row[13],row[12])
        for item in conf_arr:
            tag = item[0]
            conf = item[1]
            if(conf >= tags_threshold[tag]):
                modelTags.append(tag)
                pc.printWarn(" \t\t\t\t => Added \t {} \t conf = {}".format(tag,conf))
        modelTags = json.dumps(modelTags)
        query = 'update ' + wc_table + ' set ModelTags = ? where ID = ? and SourceSite = ?'
        data = (modelTags,row[0],row[1])
        c.execute(query,data)


    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < TaggerSimulator@wc: DB Connection Closed > ---------------------------------------------\n")
    pc.printWarn("\t\t ---------------> TIME TAKEN FOR TaggerSimulator@wc(sec)    =>  {} => TABLE: {}\n".format(round((endTime - startTime),5),wc_table))


def run(ts):
    startTime = time.time()

    try:
        update_modelTags(ts)
    except Exception as e:
        pc.printErr(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in Running Tagger Simulator for wc table xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\t>>> Error = {}".format(str(e)))
        logging.error(traceback.format_exc())
        pass

    endTime = time.time()

    pc.printSucc("**************************** Tagger(Simulator) Run is Complete for wc **********************************************")
    pc.printWarn("| \t\t TIME TAKEN FOR Tagger(Simulator) Run(sec)     \t\t | \t\t {}  \t\t |".format(round((endTime - startTime),5)))
    pc.printSucc("***********************************************************************************************************************\n\n")