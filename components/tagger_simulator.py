from random import randrange, uniform


"""
#TODO: take into account both: modelTag(conf value) & sourceTag(conf =100%) with diff weights ofc

"""

"""  (tag_name, CONFIDENCE_THRESHOLD) """

tags_threshold = {           
        'cse' : 0.5,
        'algo.cse' : 0.5,
        'law.cse' : 0.5,
        'crypto.cse' : 0.5,
        'hardware' : 0.5,
        'plt.cse' : 0.5,
        'frme.cse' : 0.5,
        'logic.cse' : 0.5,
        'compiler' : 0.5,
        'netwrk' : 0.5,
        'os' : 0.5,
        'ios.os' : 0.5,
        'android.os' : 0.5,
        'mac.os' : 0.5,
        'windows.os' : 0.5,
        'linux.os' : 0.5,
        'unix.os' : 0.5,
        'reveng.prog' : 0.5,
        'ml' : 0.5,
        'ai' : 0.5,
        'bigdata' : 0.5,
        'dataset' : 0.5,
        'dsc' : 0.5,
        'ml' : 0.5,
        'ai' : 0.5,
        'nlp' : 0.5,
        'cvis' : 0.5,
        'dataming' : 0.5,
        'database' : 0.5,
        'datavis.ds' : 0.5,
        'stats' : 0.5,
        'prog' : 0.5,
        'proglng' : 0.5,
        'plt.cse' : 0.5,
        'assem' : 0.5,
        'c' : 0.5,
        'cpp' : 0.5,
        'golang' : 0.5,
        'python' : 0.5,
        'scala' : 0.5,
        'elixir' : 0.5,
        'elm' : 0.5,
        'erlang' : 0.5,
        'fortran' : 0.5,
        'haskell' : 0.5,
        'java' : 0.5,
        'javascript' : 0.5,
        'lisp' : 0.5,
        'perl' : 0.5,
        '' : 0.5,
        'objc' : 0.5,
        'perl' : 0.5,
        'php' : 0.5,
        'ruby' : 0.5,
        'rust' : 0.5,
        'swift' : 0.5,
        'd' : 0.5,
        'chash' : 0.5,
        'fhash' : 0.5,
        'dotnet' : 0.5,
        'html' : 0.5,
        'kotlin' : 0.5,
        'css' : 0.5,
        'frm.prog' : 0.5,
        'ror' : 0.5,
        'django' : 0.5,
        'reactjs' : 0.5,
        'nodejs' : 0.5,
        'tools.prog' : 0.5,
        'vcs.prog' : 0.5,
        'api.prog' : 0.5,
        'virtualn.prog' : 0.5,
        'editor.prog' : 0.5,
        'browser' : 0.5,
        'aws' : 0.5,
        'dbs' : 0.5,
        'webd.prog' : 0.5,
        'appd.prog' : 0.5,
        'android' : 0.5,
        'ios' : 0.5,
        'sofrel.prog' : 0.5,
        'debugging' : 0.5,
        'testing.prog' : 0.5,
        'devops' : 0.5,
        'security' : 0.5,
        'compsec' : 0.5,
        'websec' : 0.5,
        'privacy' : 0.5,
        'crypto.cse' : 0.5,
        'design' : 0.5,
        'cmpgr' : 0.5,
        'webdes' : 0.5,
        'scaling.prog' : 0.5,
        'peropt.prog' : 0.5,
        'devpract.prog' : 0.5,
        'gamedev' : 0.5,
        'codingchlg' : 0.5,
        'law.cse' : 0.5,
        'opensrc' : 0.5,
        'os' : 0.5,
        'ios.os' : 0.5,
        'android.os' : 0.5,
        'mac.os' : 0.5,
        'windows.os' : 0.5,
        'linux.os' : 0.5,
        'unix.os' : 0.5,
        'query' : 0.5,
        'career' : 0.5,
        'advise.carr' : 0.5,
        'codingchlg' : 0.5,
        'technews' : 0.5,
        'discuss' : 0.5,
        'query' : 0.5,
        'community' : 0.5,
        'person' : 0.5,
        'edu' : 0.5,
        'cogsci' : 0.5,
        'art' : 0.5,
        'book' : 0.5,
        'hist.it' : 0.5,
        'phil' : 0.5,
        'startup' : 0.5,
        'selfproj' : 0.5,
        'opensrc' : 0.5,
        'law.cse' : 0.5,
        'science' : 0.5,
        'maths' : 0.5,
        'stats' : 0.5,
        'crypto.cse' : 0.5,
        'logic' : 0.5,
        'finance' : 0.5,
        'bitcoin' : 0.5,
        'crypto.fin' : 0.5
}

#TODO: replace with real model
def SimulatorApi(content, Weighted_content):
    conf_arr = []
    i = 0
    for tag in tags_threshold:
        # conf_arr.append((tags,uniform(0,1)))
        #Trying to uniformly distribute the randomization
        if i%5 == 0:
            conf_arr.append((tag,uniform(0.5,1)))
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
    pc.printSucc('@[{}] >>>>>> Started  TaggerSimulator@wc ................... => TABLE: {}\n'.format(datetime.datetime.fromtimestamp(ts),wc_table))
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

        conf_arr = SimulatorApi(row[13],row[12])
        for item in conf_arr:
            tag = item[0]
            conf = item[1]
            if(conf >= tags_threshold[tag]):
                modelTags.append(tag)
        query = 'update ' + wc_table + ' set ModelTags = ? where ID = ? and SourceSite = ?'
        data = (modelTags,row[0],row[1])
        c.execute(query,data)


    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < TaggerSimulator@wc: DB Connection Closed > ---------------------------------------------\n")
    pc.printWarn("\t\t ---------------> TIME TAKEN FOR TaggerSimulator@wc    =>  {} => TABLE: {}\n".format(round((endTime - startTime),5),wc_table))


def run(ts):
    startTime = time.time()

    try:
        update_modelTags(ts)
    except Exception as e:
        pc.printErr(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in Running Tagger Simulator for wc table xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\t>>> Error = {}".format(str(e)))
        logging.error(traceback.format_exc())
        pass

    endTime = time.time()

    pc.printSucc("**************************** Tagger(Simulator) Run is Complete for wc ********************************\n\n")
    pc.printWarn("| \t\t TIME TAKEN FOR Tagger(Simulator) Run     \t\t | \t\t {}  \t\t |".format(round((endTime - startTime),5)))
    pc.printSucc("*************************************************************************************************\n\n")


# if __name__ == "__main__":
#     # for tag in tags_threshold:
#     #     print(tag, "   \t : Threshold Value =  ", tags_threshold[tag], "   \t \t Calculated Value = ", uniform(0,1))
#     conf_arr = SimulatorApi("content","wt_content")
#     # print(conf_arr)
#     for conf in conf_arr:
#         print(" tag: {} \t confidence: {}".format(conf[0],conf[1]))