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
    "gen_cse" : 0.99,
    "distribut_sys" : 0.99,
    "data_struct" : 0.99,
    "algo_dsa" : 0.99,
    "gametheory" : 0.99,
    "disco" : 0.99,
    "crypto_cse" : 0.99,
    "hardware" : 0.99,
    "plt_cse" : 0.99,
    "frmlmeth_cse" : 0.99,
    "logic" : 0.99,
    "comparch" : 0.99,
    "compiler" : 0.99,
    "network" : 0.99,
    "revengg" : 0.99,
    "osdev" : 0.99,
    "ios" : 0.99,
    "android" : 0.99,
    "mac" : 0.99,
    "windows" : 0.99,
    "linux" : 0.99,
    "archlinux" : 0.99,
    "unix" : 0.99,
    "hacking" : 0.99,
    "robotics" : 0.99,
    "arvr" : 0.99,
    "iot" : 0.99,
    "compvision" : 0.99,
    "imgprocess" : 0.99,
    "datamine" : 0.99,
    "gen_ml" : 0.99,
    "ann" : 0.99,
    "dl" : 0.99,
    "gen_ds" : 0.99,
    "database" : 0.99,
    "dataset" : 0.99,
    "statistics" : 0.99,
    "rlang" : 0.99,
    "matlab" : 0.99,
    "scala" : 0.99,
    "scikit" : 0.99,
    "jupyternote" : 0.99,
    "kaggle" : 0.99,
    "datacleaning" : 0.99,
    "nlp" : 0.99,
    "database" : 0.99,
    "gen_bigdata" : 0.99,
    "spark" : 0.99,
    "hadoop" : 0.99,
    "data_visn" : 0.99,
    "gen_datavis" : 0.99,
    "tableau" : 0.99,
    "excel" : 0.99,
    "ai" : 0.99,
    "gen_prog" : 0.99,
    "proglng" : 0.99,
    "plt" : 0.99,
    "asm" : 0.99,
    "c" : 0.99,
    "cpp" : 0.99,
    "golang" : 0.99,
    "python" : 0.99,
    "scala" : 0.99,
    "elixir" : 0.99,
    "elm" : 0.99,
    "erlang" : 0.99,
    "fortran" : 0.99,
    "haskell" : 0.99,
    "java" : 0.99,
    "js" : 0.99,
    "lisp" : 0.99,
    "perl" : 0.99,
    "php" : 0.99,
    "ruby" : 0.99,
    "rust" : 0.99,
    "dotnet" : 0.99,
    "kotlin" : 0.99,
    "html" : 0.99,
    "css" : 0.99,
    "ror" : 0.99,
    "django" : 0.99,
    "reactjs" : 0.99,
    "nodejs" : 0.99,
    "git" : 0.99,
    "virtualn" : 0.99,
    "browser" : 0.99,
    "aws" : 0.99,
    "azure" : 0.99,
    "k8s" : 0.99,
    "docker" : 0.99,
    "gcp" : 0.99,
    "editor" : 0.99,
    "vim" : 0.99,
    "emacs" : 0.99,
    "gen_appdev" : 0.99,
    "iosdev" : 0.99,
    "androiddev" : 0.99,
    "gen_devops" : 0.99,
    "aws" : 0.99,
    "azure" : 0.99,
    "k8s" : 0.99,
    "docker" : 0.99,
    "gcp" : 0.99,
    "infosec" : 0.99,
    "compsec" : 0.99,
    "websec" : 0.99,
    "privacy" : 0.99,
    "crypto_cse" : 0.99,
    "graphix" : 0.99,
    "compgphix" : 0.99,
    "webdes" : 0.99,
    "ui" : 0.99,
    "ux" : 0.99,
    "db" : 0.99,
    "webd" : 0.99,
    "sdt" : 0.99,
    "system" : 0.99,
    "devpract" : 0.99,
    "api" : 0.99,
    "gamedev" : 0.99,
    "codingchlg" : 0.99,
    "opensrc" : 0.99,
    "freesoft" : 0.99,
    "prog_query" : 0.99,
    "jobs" : 0.99,
    "carr_query" : 0.99,
    "interviewprep" : 0.99,
    "interviewexp" : 0.99,
    "codingchlg" : 0.99,
    "technews" : 0.99,
    "tech_discuss" : 0.99,
    "tech_query" : 0.99,
    "community" : 0.99,
    "person" : 0.99,
    "tech_blog" : 0.99,
    "tech_law" : 0.99,
    "cogsci" : 0.99,
    "torrent" : 0.99,
    "book" : 0.99,
    "write" : 0.99,
    "phil" : 0.99,
    "history" : 0.99,
    "gen_business" : 0.99,
    "startup" : 0.99,
    "freelance" : 0.99,
    "saas" : 0.99,
    "sideproj" : 0.99,
    "market" : 0.99,
    "seo" : 0.99,
    "opensrc" : 0.99,
    "gen_science" : 0.99,
    "sci_query" : 0.99,
    "chemistry" : 0.99,
    "biology" : 0.99,
    "medicine" : 0.99,
    "neuroscience" : 0.99,
    "geology" : 0.99,
    "env" : 0.99,
    "health" : 0.99,
    "gen_physics" : 0.99,
    "astro" : 0.99,
    "quantum" : 0.99,
    "nuclear" : 0.99,
    "fluid_mech" : 0.99,
    "gen_engg" : 0.99,
    "engg_ece" : 0.99,
    "engg_electric" : 0.99,
    "engg_query" : 0.99,
    "engg_mech" : 0.99,
    "engg_student" : 0.99,
    "rocket" : 0.99,
    "engg_struct" : 0.99,
    "robotics" : 0.99,
    "threedprint" : 0.99,
    "gen_maths" : 0.99,
    "calculus" : 0.99,
    "algebra" : 0.99,
    "gametheory" : 0.99,
    "graphtheory" : 0.99,
    "logic" : 0.99,
    "disco" : 0.99,
    "statistics" : 0.99,
    "crypto_cse" : 0.99,
    "economics" : 0.99,
    "finance" : 0.99,
    "accounting" : 0.99,
    "invest" : 0.99,
    "gen_blockchain" : 0.99,
    "crypto_fin" : 0.99,
    "bitcoin    " : 0.99
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
        # pc.printMsg("\t <ID = {}><src= {} > [Tagger] Start................ ".format(row[0],row[1]))

        conf_arr = SimulatorApi(row[13],row[12])
        for item in conf_arr:
            tag = item[0]
            conf = item[1]
            if(conf >= tags_threshold[tag]):
                modelTags.append(tag)
                # pc.printWarn(" \t\t\t\t => Added \t {} \t conf = {}".format(tag,conf))
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