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
    "gen_cse" : 0.98,
    "distribut_sys" : 0.98,
    "data_struct" : 0.98,
    "algo_dsa" : 0.98,
    "gametheory" : 0.98,
    "disco" : 0.98,
    "crypto_cse" : 0.98,
    "hardware" : 0.98,
    "plt_cse" : 0.98,
    "frmlmeth_cse" : 0.98,
    "logic" : 0.98,
    "comparch" : 0.98,
    "compiler" : 0.98,
    "network" : 0.98,
    "revengg" : 0.98,
    "osdev" : 0.98,
    "ios" : 0.98,
    "android" : 0.98,
    "mac" : 0.98,
    "windows" : 0.98,
    "linux" : 0.98,
    "archlinux" : 0.98,
    "unix" : 0.98,
    "hacking" : 0.98,
    "robotics" : 0.98,
    "arvr" : 0.98,
    "iot" : 0.98,
    "compvision" : 0.98,
    "imgprocess" : 0.98,
    "datamine" : 0.98,
    "gen_ml" : 0.98,
    "ann" : 0.98,
    "dl" : 0.98,
    "gen_ds" : 0.98,
    "database" : 0.98,
    "dataset" : 0.98,
    "statistics" : 0.98,
    "rlang" : 0.98,
    "matlab" : 0.98,
    "scala" : 0.98,
    "scikit" : 0.98,
    "jupyternote" : 0.98,
    "kaggle" : 0.98,
    "datacleaning" : 0.98,
    "nlp" : 0.98,
    "database" : 0.98,
    "gen_bigdata" : 0.98,
    "spark" : 0.98,
    "hadoop" : 0.98,
    "data_visn" : 0.98,
    "gen_datavis" : 0.98,
    "tableau" : 0.98,
    "excel" : 0.98,
    "ai" : 0.98,
    "gen_prog" : 0.98,
    "proglng" : 0.98,
    "plt" : 0.98,
    "asm" : 0.98,
    "c" : 0.98,
    "cpp" : 0.98,
    "golang" : 0.98,
    "python" : 0.98,
    "scala" : 0.98,
    "elixir" : 0.98,
    "elm" : 0.98,
    "erlang" : 0.98,
    "fortran" : 0.98,
    "haskell" : 0.98,
    "java" : 0.98,
    "js" : 0.98,
    "lisp" : 0.98,
    "perl" : 0.98,
    "php" : 0.98,
    "ruby" : 0.98,
    "rust" : 0.98,
    "dotnet" : 0.98,
    "kotlin" : 0.98,
    "html" : 0.98,
    "css" : 0.98,
    "ror" : 0.98,
    "django" : 0.98,
    "reactjs" : 0.98,
    "nodejs" : 0.98,
    "git" : 0.98,
    "virtualn" : 0.98,
    "browser" : 0.98,
    "aws" : 0.98,
    "azure" : 0.98,
    "k8s" : 0.98,
    "docker" : 0.98,
    "gcp" : 0.98,
    "editor" : 0.98,
    "vim" : 0.98,
    "emacs" : 0.98,
    "gen_appdev" : 0.98,
    "iosdev" : 0.98,
    "androiddev" : 0.98,
    "gen_devops" : 0.98,
    "aws" : 0.98,
    "azure" : 0.98,
    "k8s" : 0.98,
    "docker" : 0.98,
    "gcp" : 0.98,
    "infosec" : 0.98,
    "compsec" : 0.98,
    "websec" : 0.98,
    "privacy" : 0.98,
    "crypto_cse" : 0.98,
    "graphix" : 0.98,
    "compgphix" : 0.98,
    "webdes" : 0.98,
    "ui" : 0.98,
    "ux" : 0.98,
    "db" : 0.98,
    "webd" : 0.98,
    "sdt" : 0.98,
    "system" : 0.98,
    "devpract" : 0.98,
    "api" : 0.98,
    "gamedev" : 0.98,
    "codingchlg" : 0.98,
    "opensrc" : 0.98,
    "freesoft" : 0.98,
    "prog_query" : 0.98,
    "jobs" : 0.98,
    "carr_query" : 0.98,
    "interviewprep" : 0.98,
    "interviewexp" : 0.98,
    "codingchlg" : 0.98,
    "technews" : 0.98,
    "tech_discuss" : 0.98,
    "tech_query" : 0.98,
    "community" : 0.98,
    "person" : 0.98,
    "tech_blog" : 0.98,
    "tech_law" : 0.98,
    "cogsci" : 0.98,
    "torrent" : 0.98,
    "book" : 0.98,
    "write" : 0.98,
    "phil" : 0.98,
    "history" : 0.98,
    "gen_business" : 0.98,
    "startup" : 0.98,
    "freelance" : 0.98,
    "saas" : 0.98,
    "sideproj" : 0.98,
    "market" : 0.98,
    "seo" : 0.98,
    "opensrc" : 0.98,
    "gen_science" : 0.98,
    "sci_query" : 0.98,
    "chemistry" : 0.98,
    "biology" : 0.98,
    "medicine" : 0.98,
    "neuroscience" : 0.98,
    "geology" : 0.98,
    "env" : 0.98,
    "health" : 0.98,
    "gen_physics" : 0.98,
    "astro" : 0.98,
    "quantum" : 0.98,
    "nuclear" : 0.98,
    "fluid_mech" : 0.98,
    "gen_engg" : 0.98,
    "engg_ece" : 0.98,
    "engg_electric" : 0.98,
    "engg_query" : 0.98,
    "engg_mech" : 0.98,
    "engg_student" : 0.98,
    "rocket" : 0.98,
    "engg_struct" : 0.98,
    "robotics" : 0.98,
    "threedprint" : 0.98,
    "gen_maths" : 0.98,
    "calculus" : 0.98,
    "algebra" : 0.98,
    "gametheory" : 0.98,
    "graphtheory" : 0.98,
    "logic" : 0.98,
    "disco" : 0.98,
    "statistics" : 0.98,
    "crypto_cse" : 0.98,
    "economics" : 0.98,
    "finance" : 0.98,
    "accounting" : 0.98,
    "invest" : 0.98,
    "gen_blockchain" : 0.98,
    "crypto_fin" : 0.98,
    "bitcoin    " : 0.98
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