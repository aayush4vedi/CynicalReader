import time
import json
from datetime import datetime
import logging

import sqlite3
from utilities import print_in_color as pc
from utilities import tree_printer_pretty

from components import th_query



"""
    NOTE: To add a new node in tree(& vis-a-vis in th_table)
    (0). If LeafNode->(It its an actual topic tag(with its own item_count & popi)) Add its name in tags_name       E.g. : "new_tag"
    1. create its node                  E.g. : new_tag_n = Node("new_tag")
    (2). If LeafNode-> map these two in `node_dict`         E.g.: "new_tag" : new_tag_n
    3. Adding in tree-structure:
        * (If Not leaf) Declare isTag = false               E.g.: new_tag_n.isTag = False
        * Add it to its place                               E.g.: existing_parent_n.add_child(new_tag_n)

"""



"""
    1. Define Tree schema
"""
class Node(object):
    def __init__(self, name,isTag = True,count=0,popi=0):
        self.name = name
        self.isTag = isTag              # means if it is one of the topics classified by model & not an aggregator
        self.count = count
        self.popi = popi
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

# NOTE: list of all the leaf nodes only
tags_names = [
    "cse",
    "prog",
    "career",
    "social",
    "business",
    "sme",
    "fin_eco",
    "gen_cse",
    "tcse",
    "distribut_sys",
    "data_struct",
    "algo_dsa",
    "gametheory",
    "disco",
    "crypto_cse",
    "hardware",
    "plt_cse",
    "frmlmeth_cse",
    "logic",
    "ce",
    "comparch",
    "compiler",
    "network",
    "revengg",
    "os",
    "osdev",
    "ios",
    "android",
    "mac",
    "windows",
    "linux",
    "archlinux",
    "unix",
    "csa",
    "hacking",
    "robotics",
    "arvr",
    "iot",
    "compvision",
    "imgprocess",
    "datamine",
    "ml",
    "gen_ml",
    "ann",
    "dl",
    "gen_ds",
    "database",
    "dataset",
    "statistics",
    "rlang",
    "matlab",
    "ds_tool",
    "scala",
    "scikit",
    "jupyternote",
    "de",
    "kaggle",
    "datacleaning",
    "nlp",
    "database",
    "bigdata",
    "gen_bigdata",
    "spark",
    "hadoop",
    # "data_visn",
    "gen_datavis",
    "tableau",
    "excel",
    "ai",
    "gen_prog",
    "lng_n_frmwrk",
    "lng",
    "proglng",
    "plt",
    "asm",
    "c",
    "cpp",
    "golang",
    "python",
    "scala",
    "elixir",
    "elm",
    "erlang",
    "fortran",
    "haskell",
    "java",
    "js",
    "lisp",
    "perl",
    "php",
    "ruby",
    "rust",
    "dotnet",
    "kotlin",
    "html",
    "css",
    "frmwrk",
    "ror",
    "django",
    "reactjs",
    "nodejs",
    "prog_tools",
    "git",
    "virtualn",
    "browser",
    "aws",
    "azure",
    "k8s",
    "docker",
    "gcp",
    "txt_edit",
    "editor",
    "vim",
    "emacs",
    "appdev",
    "devops",
    "gen_appdev",
    "iosdev",
    "androiddev",
    "gen_devops",
    "aws",
    "azure",
    "k8s",
    "docker",
    "gcp",
    "security",
    "infosec",
    "compsec",
    "websec",
    "privacy",
    "crypto_cse",
    "graphix",
    "compgphix",
    "webdes",
    "ui",
    "ux",
    "db",
    "webd",
    "sdt",
    "system",
    "devpract",
    "api",
    "gamedev",
    "codingchlg",
    "opensrc",
    "freesoft",
    "prog_query",       
    "jobs",
    "carr_query",
    "interviewprep",
    "interviewexp",
    "codingchlg",
    "technews",
    "tech_discuss",
    "tech_query",
    "community",
    "person",
    "tech_blog",
    "tech_law",
    "cogsci",
    "torrent",
    "book",
    "write",
    "phil",
    "history",
    "gen_business",
    "startup",
    "freelance",
    "saas",
    "sideproj",
    "market",
    "seo",
    "opensrc",
    "gen_science",
    "sci_query",
    "chemistry",
    "biology",
    "medicine",
    "neuroscience",
    "geology",
    "env",
    "health",
    "gen_physics",
    "astro",
    "quantum",
    "nuclear",
    "fluid_mech",
    "gen_engg",
    "engg_ece",
    "engg_electric",
    "engg_query",
    "engg_mech",
    "engg_student",
    "rocket",
    "engg_struct",
    "robotics",
    "threedprint",
    "gen_maths",
    "calculus",
    "algebra",
    "gametheory",
    "graphtheory",
    "logic",
    "disco",
    "statistics",
    "crypto_cse",
    "economics",
    "finance",
    "accounting",
    "invest",
    "gen_blockchain",
    "crypto_fin",
    "bitcoin",
]

# create all the nodes(leaf+parent) in tree

root_n = Node("root")
cse_n = Node("cse")
prog_n = Node("prog")
career_n = Node("career")
social_n = Node("social")
business_n = Node("business")
sme_n = Node("sme")
fin_eco_n = Node("fin_eco")
gen_cse_n = Node("gen_cse")
tcse_n = Node("tcse")
distribut_sys_n = Node("distribut_sys")
data_struct_n = Node("data_struct")
algo_dsa_n = Node("algo_dsa")
gametheory_n = Node("gametheory")
disco_n = Node("disco")
crypto_cse_n = Node("crypto_cse")
hardware_n = Node("hardware")
plt_cse_n = Node("plt_cse")
frmlmeth_cse_n = Node("frmlmeth_cse")
logic_n = Node("logic")
ce_n = Node("ce")
comparch_n = Node("comparch")
compiler_n = Node("compiler")
network_n = Node("network")
revengg_n = Node("revengg")
os_n = Node("os")
osdev_n = Node("osdev")
ios_n = Node("ios")
android_n = Node("android")
mac_n = Node("mac")
windows_n = Node("windows")
linux_n = Node("linux")
archlinux_n = Node("archlinux")
unix_n = Node("unix")
csa_n = Node("csa")
hacking_n = Node("hacking")
robotics_n = Node("robotics")
arvr_n = Node("arvr")
iot_n = Node("iot")
compvision_n = Node("compvision")
imgprocess_n = Node("imgprocess")
datamine_n = Node("datamine")
ml_n = Node("ml")
gen_ml_n = Node("gen_ml")
ann_n = Node("ann")
dl_n = Node("dl")
ds_n = Node("ds")
gen_ds_n = Node("gen_ds")
database_n = Node("database")
dataset_n = Node("dataset")
statistics_n = Node("statistics")
rlang_n = Node("rlang")
matlab_n = Node("matlab")
kaggle_n = Node("kaggle")
datacleaning_n = Node("datacleaning")
nlp_n = Node("nlp")
ai_n = Node("ai")
ds_tool_n = Node("ds_tool")
scala_n = Node("scala")
scikit_n = Node("scikit")
jupyternote_n = Node("jupyternote")
de_n = Node("de")
bigdata_n = Node("bigdata")
gen_bigdata_n = Node("gen_bigdata")
spark_n = Node("spark")
hadoop_n = Node("hadoop")
data_visn_n = Node("data_visn")
gen_datavis_n = Node("gen_datavis")
tableau_n = Node("tableau")
excel_n = Node("excel")
gen_prog_n = Node("gen_prog")
db_n = Node("db")
webd_n = Node("webd")
sdt_n = Node("sdt")
system_n = Node("system")
devpract_n = Node("devpract")
api_n = Node("api")
gamedev_n = Node("gamedev")
codingchlg_n = Node("codingchlg")
opensrc_n = Node("opensrc")
freesoft_n = Node("freesoft")
lng_n_frmwrk_n = Node("lng_n_frmwrk")
lng_n = Node("lng")
proglng_n = Node("proglng")
plt_n = Node("plt")
asm_n = Node("asm")
c_n = Node("c")
cpp_n = Node("cpp")
golang_n = Node("golang")
python_n = Node("python")
scala_n = Node("scala")
elixir_n = Node("elixir")
elm_n = Node("elm")
erlang_n = Node("erlang")
fortran_n = Node("fortran")
haskell_n = Node("haskell")
java_n = Node("java")
js_n = Node("js")
lisp_n = Node("lisp")
perl_n = Node("perl")
php_n = Node("php")
ruby_n = Node("ruby")
rust_n = Node("rust")
dotnet_n = Node("dotnet")
kotlin_n = Node("kotlin")
html_n = Node("html")
css_n = Node("css")
frmwrk_n = Node("frmwrk")
ror_n = Node("ror")
django_n = Node("django")
reactjs_n = Node("reactjs")
nodejs_n = Node("nodejs")
prog_tools_n = Node("prog_tools")
git_n = Node("git")
virtualn_n = Node("virtualn")
browser_n = Node("browser")
aws_n = Node("aws")
azure_n = Node("azure")
k8s_n = Node("k8s")
docker_n = Node("docker")
gcp_n = Node("gcp")
txt_edit_n = Node("txt_edit")
editor_n = Node("editor")
vim_n = Node("vim")
emacs_n = Node("emacs")
appdev_n = Node("appdev")
gen_appdev_n = Node("gen_appdev")
iosdev_n = Node("iosdev")
androiddev_n = Node("androiddev")
devops_n = Node("devops")
gen_devops_n = Node("gen_devops")
security_n = Node("security")
infosec_n = Node("infosec")
compsec_n = Node("compsec")
websec_n = Node("websec")
privacy_n = Node("privacy")
crypto_cse_n = Node("crypto_cse")
design_n = Node("design")
graphix_n = Node("graphix")
compgphix_n = Node("compgphix")
webdes_n = Node("webdes")
ui_n = Node("ui")
ux_n = Node("ux")
prog_query_n = Node("prog_query")
jobs_n = Node("jobs")
carr_query_n = Node("carr_query")
interviewprep_n = Node("interviewprep")
interviewexp_n = Node("interviewexp")
technews_n = Node("technews")
tech_discuss_n = Node("tech_discuss")
tech_query_n = Node("tech_query")
community_n = Node("community")
person_n = Node("person")
tech_blog_n = Node("tech_blog")
tech_law_n = Node("tech_law")
cogsci_n = Node("cogsci")
torrent_n = Node("torrent")
read_n_write_n = Node("read_n_write")
book_n = Node("book")
write_n = Node("write")
phil_n = Node("phil")
history_n = Node("history")
gen_business_n = Node("gen_business")
startup_n = Node("startup")
freelance_n = Node("freelance")
saas_n = Node("saas")
sideproj_n = Node("sideproj")
market_n = Node("market")
seo_n = Node("seo")
science_n = Node("science")
gen_science_n = Node("gen_science")
sci_query_n = Node("sci_query")
chemistry_n = Node("chemistry")
biology_n = Node("biology")
medicine_n = Node("medicine")
neuroscience_n = Node("neuroscience")
geology_n = Node("geology")
env_n = Node("env")
health_n = Node("health")
physics_n = Node("physics")
gen_physics_n = Node("gen_physics")
astro_n = Node("astro")
quantum_n = Node("quantum")
nuclear_n = Node("nuclear")
fluid_mech_n = Node("fluid_mech")
engg_n = Node("engg")
gen_engg_n = Node("gen_engg")
engg_ece_n = Node("engg_ece")
engg_electric_n = Node("engg_electric")
engg_query_n = Node("engg_query")
engg_mech_n = Node("engg_mech")
engg_student_n = Node("engg_student")
rocket_n = Node("rocket")
engg_struct_n = Node("engg_struct")
threedprint_n = Node("threedprint")
maths_n = Node("maths")
gen_maths_n = Node("gen_maths")
calculus_n = Node("calculus")
algebra_n = Node("algebra")
graphtheory_n = Node("graphtheory")
economics_n = Node("economics")
finance_n = Node("finance")
accounting_n = Node("accounting")
invest_n = Node("invest")
blockchain_n = Node("blockchain")
gen_blockchain_n = Node("gen_blockchain")
crypto_fin_n = Node("crypto_fin")
bitcoin_n = Node("bitcoin")


# make dictironay to map strings to above created roots
node_dict = {
    "root"   : root_n,
    "cse"   : cse_n,
    "prog"   : prog_n,
    "career"   : career_n,
    "social"   : social_n,
    "business"   : business_n,
    "sme"   : sme_n,
    "fin_eco"   : fin_eco_n,
    "gen_cse"   : gen_cse_n,
    "tcse"   : tcse_n,
    "distribut_sys"   : distribut_sys_n,
    "data_struct"   : data_struct_n,
    "algo_dsa"   : algo_dsa_n,
    "gametheory"   : gametheory_n,
    "disco"   : disco_n,
    "crypto_cse"   : crypto_cse_n,
    "hardware"   : hardware_n,
    "plt_cse"   : plt_cse_n,
    "frmlmeth_cse"   : frmlmeth_cse_n,
    "logic"   : logic_n,
    "ce"   : ce_n,
    "comparch"   : comparch_n,
    "compiler"   : compiler_n,
    "network"   : network_n,
    "revengg"   : revengg_n,
    "os"   : os_n,
    "osdev"   : osdev_n,
    "ios"   : ios_n,
    "android"   : android_n,
    "mac"   : mac_n,
    "windows"   : windows_n,
    "linux"   : linux_n,
    "archlinux"   : archlinux_n,
    "unix"   : unix_n,
    "csa"   : csa_n,
    "hacking"   : hacking_n,
    "robotics"   : robotics_n,
    "arvr"   : arvr_n,
    "iot"   : iot_n,
    "compvision"   : compvision_n,
    "imgprocess"   : imgprocess_n,
    "datamine"   : datamine_n,
    "ml"   : ml_n,
    "gen_ml"   : gen_ml_n,
    "ann"   : ann_n,
    "dl"   : dl_n,
    "ds"   : ds_n,
    "gen_ds"   : gen_ds_n,
    "database"   : database_n,
    "dataset"   : dataset_n,
    "statistics"   : statistics_n,
    "rlang"   : rlang_n,
    "matlab"   : matlab_n,
    "kaggle"   : kaggle_n,
    "datacleaning"   : datacleaning_n,
    "nlp"   : nlp_n,
    "ai"   : ai_n,
    "ds_tool"   : ds_tool_n,
    "scala"   : scala_n,
    "scikit"   : scikit_n,
    "jupyternote"   : jupyternote_n,
    "de"   : de_n,
    "bigdata"   : bigdata_n,
    "gen_bigdata"   : gen_bigdata_n,
    "spark"   : spark_n,
    "hadoop"   : hadoop_n,
    "data_visn"    : data_visn_n,
    "gen_datavis"    : gen_datavis_n,
    "tableau"    : tableau_n,
    "excel"    : excel_n,
    "gen_prog"   : gen_prog_n,
    "db"   : db_n,
    "webd"   : webd_n,
    "sdt"   : sdt_n,
    "system"   : system_n,
    "devpract"   : devpract_n,
    "api"   : api_n,
    "gamedev"   : gamedev_n,
    "codingchlg"   : codingchlg_n,
    "opensrc"   : opensrc_n,
    "freesoft"   : freesoft_n,
    "lng_n_frmwrk"   : lng_n_frmwrk_n,
    "lng"   : lng_n,
    "proglng"   : proglng_n,
    "plt"   : plt_n,
    "asm"   : asm_n,
    "c"   : c_n,
    "cpp"   : cpp_n,
    "golang"   : golang_n,
    "python"   : python_n,
    "scala"   : scala_n,
    "elixir"   : elixir_n,
    "elm"   : elm_n,
    "erlang"   : erlang_n,
    "fortran"   : fortran_n,
    "haskell"   : haskell_n,
    "java"   : java_n,
    "js"   : js_n,
    "lisp"   : lisp_n,
    "perl"   : perl_n,
    "php"   : php_n,
    "ruby"   : ruby_n,
    "rust"   : rust_n,
    "dotnet"   : dotnet_n,
    "kotlin"   : kotlin_n,
    "html"   : html_n,
    "css"   : css_n,
    "frmwrk"   : frmwrk_n,
    "ror"   : ror_n,
    "django"   : django_n,
    "reactjs"   : reactjs_n,
    "nodejs"   : nodejs_n,
    "prog_tools"   : prog_tools_n,
    "git"   : git_n,
    "virtualn"   : virtualn_n,
    "browser"   : browser_n,
    "aws"   : aws_n,
    "azure"   : azure_n,
    "k8s"   : k8s_n,
    "docker"   : docker_n,
    "gcp"   : gcp_n,
    "txt_edit"   : txt_edit_n,
    "editor"   : editor_n,
    "vim"   : vim_n,
    "emacs"   : emacs_n,
    "appdev"   : appdev_n,
    "gen_appdev"   : gen_appdev_n,
    "iosdev"   : iosdev_n,
    "androiddev"   : androiddev_n,
    "devops"   : devops_n,
    "gen_devops"   : gen_devops_n,
    "security"   : security_n,
    "infosec"   : infosec_n,
    "compsec"   : compsec_n,
    "websec"   : websec_n,
    "privacy"   : privacy_n,
    "crypto_cse"   : crypto_cse_n,
    "design"   : design_n,
    "graphix"   : graphix_n,
    "compgphix"   : compgphix_n,
    "webdes"   : webdes_n,
    "ui"   : ui_n,
    "ux"   : ux_n,
    "jobs"   : jobs_n,
    "prog_query" : prog_query_n,
    "carr_query"   : carr_query_n,
    "interviewprep"   : interviewprep_n,
    "interviewexp"   : interviewexp_n,
    "technews"   : technews_n,
    "tech_discuss"   : tech_discuss_n,
    "tech_query"   : tech_query_n,
    "community"   : community_n,
    "person"   : person_n,
    "tech_blog"   : tech_blog_n,
    "tech_law"   : tech_law_n,
    "cogsci"   : cogsci_n,
    "torrent"   : torrent_n,
    "read_n_write"   : read_n_write_n,
    "book"   : book_n,
    "write"   : write_n,
    "phil"   : phil_n,
    "history"   : history_n,
    "gen_business"   : gen_business_n,
    "startup"   : startup_n,
    "freelance"   : freelance_n,
    "saas"   : saas_n,
    "sideproj"   : sideproj_n,
    "market"   : market_n,
    "seo"   : seo_n,
    "science"   : science_n,
    "gen_science"   : gen_science_n,
    "sci_query"   : sci_query_n,
    "chemistry"   : chemistry_n,
    "biology"   : biology_n,
    "medicine"   : medicine_n,
    "neuroscience"   : neuroscience_n,
    "geology"   : geology_n,
    "env"   : env_n,
    "health"   : health_n,
    "physics"   : physics_n,
    "gen_physics"   : gen_physics_n,
    "astro"   : astro_n,
    "quantum"   : quantum_n,
    "nuclear"   : nuclear_n,
    "fluid_mech"   : fluid_mech_n,
    "engg"   : engg_n,
    "gen_engg"   : gen_engg_n,
    "engg_ece"   : engg_ece_n,
    "engg_electric"   : engg_electric_n,
    "engg_query"   : engg_query_n,
    "engg_mech"   : engg_mech_n,
    "engg_student"   : engg_student_n,
    "rocket"   : rocket_n,
    "engg_struct"   : engg_struct_n,
    "threedprint"   : threedprint_n,
    "maths"   : maths_n,
    "gen_maths"   : gen_maths_n,
    "calculus"   : calculus_n,
    "algebra"   : algebra_n,
    "graphtheory"   : graphtheory_n,
    "economics"   : economics_n,
    "finance"   : finance_n,
    "accounting"   : accounting_n,
    "invest"   : invest_n,
    "blockchain"   : blockchain_n,
    "gen_blockchain"   : gen_blockchain_n,
    "crypto_fin"   : crypto_fin_n,
    "bitcoin"   : bitcoin_n,
}


def TreeGermination():

    """  Populate Root node """
    root_n.isTag=False

    cse_n.isTag=False
    prog_n.isTag=False
    career_n.isTag=False
    social_n.isTag=False
    business_n.isTag=False
    sme_n.isTag=False
    fin_eco_n.isTag=False

    root_n.add_child(cse_n)
    root_n.add_child(prog_n)
    root_n.add_child(career_n)
    root_n.add_child(social_n)
    root_n.add_child(business_n)
    root_n.add_child(sme_n)
    root_n.add_child(fin_eco_n)

    """ Populate CSE node"""

    cse_n.add_child(gen_cse_n)

    """  ----| Populate Theoretical CSE Node"""
    tcse_n.isTag=False
    cse_n.add_child(tcse_n)

    tcse_n.add_child(distribut_sys_n)    
    tcse_n.add_child(data_struct_n)
    tcse_n.add_child(algo_dsa_n)
    tcse_n.add_child(gametheory_n)
    tcse_n.add_child(disco_n)
    tcse_n.add_child(crypto_cse_n)
    tcse_n.add_child(hardware_n)
    tcse_n.add_child(plt_cse_n)
    tcse_n.add_child(frmlmeth_cse_n)
    tcse_n.add_child(logic_n)

    """  ----| Populate Computer Engineering Node"""
    ce_n.isTag=False
    cse_n.add_child(ce_n)

    ce_n.add_child(comparch_n)    
    ce_n.add_child(compiler_n)
    ce_n.add_child(network_n)
    ce_n.add_child(revengg_n)

    """  ----|----| Populate Operating Systems Node"""
    os_n.isTag=False
    ce_n.add_child(os_n)

    os_n.add_child(osdev_n)
    os_n.add_child(ios_n)
    os_n.add_child(android_n)
    os_n.add_child(mac_n)
    os_n.add_child(windows_n)
    os_n.add_child(linux_n)
    os_n.add_child(archlinux_n)
    os_n.add_child(unix_n)

    """  ----| csa """
    csa_n.isTag=False
    cse_n.add_child(csa_n)

    """ ----|----| children of csa """

    csa_n.add_child(hacking_n)
    csa_n.add_child(robotics_n)
    csa_n.add_child(arvr_n)
    csa_n.add_child(iot_n)
    csa_n.add_child(compvision_n)
    csa_n.add_child(imgprocess_n)
    csa_n.add_child(datamine_n)
    csa_n.add_child(ai_n)

    """ ----|----|----| ml """
    ml_n.isTag=False
    csa_n.add_child(ml_n)

    gen_ml_n    = Node("gen_ml")
    ann_n       = Node("ann")
    dl_n        = Node("dl")

    """ ----|----|----| ds """
    ds_n.isTag=False
    csa_n.add_child(ds_n)

    ds_n.add_child(gen_ds_n)
    ds_n.add_child(database_n)
    ds_n.add_child(dataset_n)
    ds_n.add_child(statistics_n)
    ds_n.add_child(rlang_n)
    ds_n.add_child(matlab_n)
    ds_n.add_child(kaggle_n)
    ds_n.add_child(datacleaning_n)
    ds_n.add_child(nlp_n)
    ds_n.add_child(ai_n)

    """ ----|----|----|----| ds_tool """
    ds_tool_n.isTag=False
    ds_n.add_child(ds_tool_n)

    ds_tool_n.add_child(scala_n)
    ds_tool_n.add_child(scikit_n)
    ds_tool_n.add_child(jupyternote_n)

    """ ----|----|----| de """
    de_n.isTag=False
    csa_n.add_child(de_n)

    de_n.add_child(database_n)

    """ ----|----|----|----| bigdata """
    bigdata_n.isTag=False
    de_n.add_child(bigdata_n)

    bigdata_n.add_child(gen_bigdata_n)
    bigdata_n.add_child(spark_n)
    bigdata_n.add_child(hadoop_n)

    """ ----|----|----| data_visn """
    data_visn_n.isTag=False
    csa_n.add_child(data_visn_n)

    data_visn_n.add_child(gen_datavis_n)    
    data_visn_n.add_child(tableau_n)
    data_visn_n.add_child(excel_n)    


    """ ----| prog children"""

    prog_n.add_child(gen_prog_n)
    prog_n.add_child(db_n)
    prog_n.add_child(webd_n)
    prog_n.add_child(sdt_n)
    prog_n.add_child(system_n)
    prog_n.add_child(devpract_n)
    prog_n.add_child(api_n)
    prog_n.add_child(gamedev_n)
    prog_n.add_child(codingchlg_n)
    prog_n.add_child(opensrc_n)
    prog_n.add_child(freesoft_n)
    prog_n.add_child(os_n)

    """ ----|----| lng_n_frmwrk """
    lng_n_frmwrk_n.isTag=False
    prog_n.add_child(lng_n_frmwrk_n)

    """ ----|----|----| lng """
    lng_n.isTag=False
    lng_n_frmwrk_n.add_child(lng_n)

    """ ----|----|----|----| lng children"""

    lng_n.add_child(proglng_n)
    lng_n.add_child(plt_n)
    lng_n.add_child(asm_n)
    lng_n.add_child(c_n)
    lng_n.add_child(cpp_n)
    lng_n.add_child(golang_n)
    lng_n.add_child(python_n)
    lng_n.add_child(scala_n)
    lng_n.add_child(elixir_n)
    lng_n.add_child(elm_n)
    lng_n.add_child(erlang_n)
    lng_n.add_child(fortran_n)
    lng_n.add_child(haskell_n)
    lng_n.add_child(java_n)
    lng_n.add_child(js_n)
    lng_n.add_child(lisp_n)
    lng_n.add_child(perl_n)
    lng_n.add_child(php_n)
    lng_n.add_child(ruby_n)
    lng_n.add_child(rust_n)
    lng_n.add_child(dotnet_n)
    lng_n.add_child(kotlin_n)
    lng_n.add_child(html_n)
    lng_n.add_child(css_n)

    """ ----|----|----| frmwrk """
    frmwrk_n.isTag=False
    lng_n_frmwrk_n.add_child(frmwrk_n)

    """ ----|----|----|----| frmwrk children"""

    frmwrk_n.add_child(ror_n)
    frmwrk_n.add_child(django_n)
    frmwrk_n.add_child(reactjs_n)
    frmwrk_n.add_child(nodejs_n)

    """ ----|----| prog_tools """
    prog_tools_n.isTag=False
    prog_n.add_child(prog_tools_n)

    prog_tools_n.add_child(git_n)
    prog_tools_n.add_child(virtualn_n)
    prog_tools_n.add_child(browser_n)
    prog_tools_n.add_child(aws_n)
    prog_tools_n.add_child(azure_n)
    prog_tools_n.add_child(k8s_n)
    prog_tools_n.add_child(docker_n)
    prog_tools_n.add_child(gcp_n)

    """ ----|----| txt_edit """
    txt_edit_n.isTag=False
    prog_tools_n.add_child(txt_edit_n)

    txt_edit_n.add_child(editor_n)
    txt_edit_n.add_child(vim_n)
    txt_edit_n.add_child(emacs_n)

    """ ----|----| appdev """
    appdev_n.isTag=False
    prog_n.add_child(appdev_n)

    appdev_n.add_child(gen_appdev_n)
    appdev_n.add_child(iosdev_n)
    appdev_n.add_child(androiddev_n)

    """ ----|----| devops """
    devops_n.isTag=False
    prog_n.add_child(devops_n)

    gen_devops_n       = Node("gen_devops")

    devops_n.add_child(gen_devops_n)
    devops_n.add_child(aws_n)
    devops_n.add_child(azure_n)
    devops_n.add_child(k8s_n)
    devops_n.add_child(docker_n)
    devops_n.add_child(gcp_n)

    """ ----|----| security """
    security_n.isTag=False
    prog_n.add_child(security_n)

    security_n.add_child(infosec_n)
    security_n.add_child(compsec_n)
    security_n.add_child(websec_n)
    security_n.add_child(privacy_n)
    security_n.add_child(crypto_cse_n)

    """ ----|----| design """
    design_n.isTag=False
    prog_n.add_child(design_n)

    design_n.add_child(graphix_n)
    design_n.add_child(compgphix_n)
    design_n.add_child(webdes_n)
    design_n.add_child(ui_n)
    design_n.add_child(ux_n)

    """ ----| career children"""

    career_n.add_child(jobs_n)
    career_n.add_child(carr_query_n)
    career_n.add_child(interviewprep_n)
    career_n.add_child(interviewexp_n)

    """ ----| social children"""

    social_n.add_child(technews_n)
    social_n.add_child(tech_discuss_n)
    social_n.add_child(tech_query_n)
    social_n.add_child(community_n)
    social_n.add_child(person_n)
    social_n.add_child(tech_blog_n)
    social_n.add_child(tech_law_n)
    social_n.add_child(cogsci_n)
    social_n.add_child(torrent_n)

    """ ----|----| read_n_write """
    read_n_write_n.isTag=False
    social_n.add_child(read_n_write_n)
    
    read_n_write_n.add_child(book_n)
    read_n_write_n.add_child(write_n)
    read_n_write_n.add_child(phil_n)
    read_n_write_n.add_child(history_n)

    """ ----| business children"""

    business_n.add_child(gen_business_n)
    business_n.add_child(startup_n)
    business_n.add_child(freelance_n)
    business_n.add_child(saas_n)
    business_n.add_child(sideproj_n)
    business_n.add_child(market_n)
    business_n.add_child(seo_n)
    business_n.add_child(opensrc_n)


    """ ----| sme children"""

    """ ----|----| science """ 
    science_n.isTag=False
    sme_n.add_child(science_n)   

    science_n.add_child(gen_science_n)
    science_n.add_child(sci_query_n)
    science_n.add_child(chemistry_n)
    science_n.add_child(biology_n)
    science_n.add_child(medicine_n)
    science_n.add_child(neuroscience_n)
    science_n.add_child(geology_n)
    science_n.add_child(env_n)
    science_n.add_child(health_n)


    """ ----|----|----| physics """ 
    physics_n.isTag=False
    science_n.add_child(physics_n) 

    physics_n.add_child(gen_physics_n)
    physics_n.add_child(astro_n)
    physics_n.add_child(quantum_n)
    physics_n.add_child(nuclear_n)
    physics_n.add_child(fluid_mech_n)

    """ ----|----| engg """   
    engg_n.isTag=False
    sme_n.add_child(engg_n)

    engg_n.add_child(gen_engg_n)
    engg_n.add_child(engg_ece_n)
    engg_n.add_child(engg_electric_n)
    engg_n.add_child(engg_query_n)
    engg_n.add_child(engg_mech_n)
    engg_n.add_child(engg_student_n)
    engg_n.add_child(rocket_n)
    engg_n.add_child(engg_struct_n)
    engg_n.add_child(robotics_n)
    engg_n.add_child(threedprint_n)

    """ ----|----| maths"""    
    maths_n.isTag=False
    sme_n.add_child(maths_n)   

    maths_n.add_child(gen_maths_n)
    maths_n.add_child(calculus_n)
    maths_n.add_child(algebra_n)
    maths_n.add_child(gametheory_n)
    maths_n.add_child(graphtheory_n)
    maths_n.add_child(logic_n)
    maths_n.add_child(disco_n)
    maths_n.add_child(statistics_n)
    maths_n.add_child(crypto_cse_n)

    """ ----| fin_eco children"""

    fin_eco_n.add_child(economics_n)
    fin_eco_n.add_child(finance_n)
    fin_eco_n.add_child(accounting_n)
    fin_eco_n.add_child(invest_n)

    """ ----|----| blockchain"""
    blockchain_n.isTag=False      
    fin_eco_n.add_child(blockchain_n)

    blockchain_n.add_child(gen_blockchain_n)
    blockchain_n.add_child(crypto_fin_n)
    blockchain_n.add_child(bitcoin_n)

    return root_n

# Not in use
def BFS(root): 
    if len(root.children) == 0:
        return  
    q = [] 
    q.append(root) 
          
    while q: 
        count = len(q) 
        while count > 0: 
            temp = q.pop(0) 
            if temp.isTag == True:
                print(" <{}>  \t=> count: {} , popi: {}".format(temp.name, temp.count, temp.popi), end= '\n\t')
            else : 
                print(" [<{}>]  \t=> count: {} , popi: {}".format(temp.name, temp.count, temp.popi), end= '\n\t')
            
            for c in temp.children:
                q.append(c)
            count -= 1
        print(' ') 

# from wc_table
def updateLeafNodes(ts):

    """     
        This is the query:
           select count(ID) from wc_1601292562 where ModelTags like "%prog_query%" or SourceTags like "%prog_query%";

    """

    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    pc.printSucc('@[{}] >>>>>> Started  UpdateLeafNodes@wc ................... => TABLE: {}\n'.format(datetime.fromtimestamp(ts),wc_table))
    conn = sqlite3.connect(wc_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < UpdateLeafNodes@wc : DB Connection Opened > ---------------------------------------------\n")
    pc.printWarn("\tRunning UpdateLeafNodes for wc ....... \t NOW: {}".format(time.strftime("%H:%M:%S", time.localtime())))
    pc.printWarn("\t\t. .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .")
    startTime = time.time()

    for tag in tags_names:
        q = 'select count(ID) from ' + wc_table + ' where ModelTags like ? or SourceTags like ?'
        d = ('%"{}"%'.format(tag),'%"{}"%'.format(tag),)
        item_count = c.execute(q,d)
        item_count = c.fetchone()[0]
        q = 'select avg(PopI) from ' + wc_table + ' where ModelTags like ? or SourceTags like ?'
        avg_popi = c.execute(q,d)
        avg_popi = c.fetchone()[0]
        if avg_popi == None:
            avg_popi = 0
        else:
            avg_popi = round(avg_popi,10)
        curr_node = node_dict[tag]
        if curr_node.isTag :            #update only if its a leaf
            curr_node.count = item_count
            curr_node.popi = avg_popi
            pc.printSucc(" \t\t\t..... Updated node: {}  \t => c = {}  , p = {}".format(curr_node.name,item_count,avg_popi))


    endTime = time.time()
    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < UpdateLeafNodes@wc: DB Connection Closed > ---------------------------------------------\n")
    pc.printWarn("\t\t ---------------> TIME TAKEN FOR UpdateLeafNodes In Tree  (sec)   =>  {} \n".format(round((endTime - startTime),5)))



def updateParentPopi(root):
    if(len(root.children)==0):
        return root.popi
    children_popi_sum = 0
    for child in root.children:
        children_popi_sum += updateParentPopi(child)

    children_avg_popi = children_popi_sum/len(root.children)
    children_avg_popi = round(children_avg_popi,10)
    root.popi = children_avg_popi
    return root.popi

def updateParentCount(root):
    if(len(root.children)==0):
        return root.count
    children_item_count = 0
    for child in root.children:
        children_item_count += updateParentCount(child)

    root.count += children_item_count
    return root.count

def updateParentNodes(root):
    """ 
        update one thing at a time as doing both in one traversal doesnt seem doable
    """
    updateParentCount(root)
    updateParentPopi(root)

def queryTreeNodeForCountNPopi(search):
    """
        returns in this format:
            query_from_tree = queryTreeNodeForCountNPopi("cse")
            print("\t\t\ ====================> cse : {} , {}".format(query_from_tree[0], query_from_tree[1]))


    """
    return node_dict[search].count, node_dict[search].popi

def create_th(ts):
    """
        Just creates the th_table(Topic Hotness); if not exists already
    """
    th_db = 'dbs/th.db'
    th_table = 'th_' + str(int(ts)) 
    conn = sqlite3.connect(th_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < Create_th: DB Connection Opened > ---------------------------------------------\n")
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'".format(th_table))
    if c.fetchone()[0]==1 :                        # table exists, flush away!
        c.execute("delete from {}".format(th_table))
    else :                                         # creting new table
        c.execute("CREATE TABLE {} (ID, NodeName, LeftMptt, RightMptt, DepthLevel, ItemCount, AvgPopI, ItemIDs)".format(th_table))

    index = 1
    q = 'INSERT INTO ' + th_table + ' VALUES (?,?,?,?,?,?,?,?)'
    for node_name in node_dict:
        query_from_tree = queryTreeNodeForCountNPopi(node_name)
        d = (index, node_name, -1,-1,0,query_from_tree[0],query_from_tree[1],'EMPTY')
        c.execute(q,d)
        index += 1

    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < Create_th: DB Connection Closed > ---------------------------------------------\n")
    pc.printSucc("\t **************************************** TH Table Created: {} ******************************************************\n".format(th_table))
    
    # pc.printWarn("\t\t -------------------------------------------- Now updating TH Table --------------------------------------------\n")


def update_th_mptt(root, lft, level, ts):
    """
        Recursive function to update (lft, rgt,level) values in th_<ts> table.
        PS: No interaction with wc_table here, thought the nodes in tree get their (item_count, avg_popi) values from wc_<ts>; but that has no correlation here
    """
    rght = lft + 1
    for child in root.children:
        rght = update_th_mptt(child, rght, level + 1,ts)

    """ update (lft, rgt,level) for root in th_table """
    th_db = 'dbs/th.db'
    th_table = 'th_' + str(int(ts)) 
    conn = sqlite3.connect(th_db, timeout=10)
    c = conn.cursor()
    # pc.printMsg("\t -------------------------------------- < update_th: DB Connection Opened > ---------------------------------------------\n")
    
    q = 'update ' + th_table + ' set LeftMptt = ? , RightMptt = ? , DepthLevel = ? where NodeName = ?'
    d = (lft, rght, level, root.name)
    c.execute(q,d)

    conn.commit()
    conn.close()
    # pc.printMsg("\t -------------------------------------- < update_th: DB Connection Closed > ---------------------------------------------\n")
    return rght + 1


def update_th_table_for_itemIDs(root,ts):
    """
        For every node in th_table: get item-<IDs & SourcSite> from wc_table which have node.Name as one of their tags in desc order of Popi
            * [1] for leaf nodes- fetch items from wc_table
            * [2] for non-leaf nodes; use th_query.return_imm_children // maybe move it here
    """
    #recursively go to leaf nodes
    for child in root.children:
            update_th_table_for_itemIDs(child, ts)

    #if root is a leaf node
    if(len(root.children) == 0):
        #get list of items from wc_table
        wc_db = 'dbs/wc.db'
        wc_table = 'wc_' + str(int(ts))
        conn = sqlite3.connect(wc_db, timeout=10)
        c = conn.cursor()
        q = 'select ID, SourceSite from ' + wc_table + ' where ModelTags like ? or SourceTags like ? order by PopI DESC'
        d = ('%"{}"%'.format(root.name),'%"{}"%'.format(root.name),)
        rows = c.execute(q,d)
        rows = rows.fetchall()
        list_ids = []
        for row in rows:
            list_ids.append((row[0],row[1]))
        conn.commit()
        conn.close()
    else:
        # 'select ID from ' + wc_table + ' where ModelTags like "%ai%" or  ModelTags like "%maths%" or ... order by PopI DESC;'
        imm_children = th_query.return_imm_children(ts,root.name)
        model_tag_string = ''
        for child in imm_children:
            model_tag_string += 'ModelTags like "%{}%" or SourceTags like "%{}%" or '.format(child[1],child[1])
        # remove last 'or '
        model_tag_string = model_tag_string[:-3] 

        wc_db = 'dbs/wc.db'
        wc_table = 'wc_' + str(int(ts))
        conn = sqlite3.connect(wc_db, timeout=10)
        c = conn.cursor()
        q = 'select ID, SourceSite from ' + wc_table + ' where ' + model_tag_string +' order by PopI DESC'
        rows = c.execute(q)
        rows = rows.fetchall()
        list_ids = []
        for row in rows:
            list_ids.append((row[0],row[1]))
        # print("[{}]\t  \t::\t {} \n\t\t\t=> {}".format(root.name, model_tag_string,list_ids))
        conn.commit()
        conn.close()
        
    # print("[{}]\t  => {}".format(root.name, list_ids))

    #Update the node in th_table
    list_ids = json.dumps(list_ids)
    th_db = 'dbs/th.db'
    th_table = 'th_' + str(int(ts)) 
    conn = sqlite3.connect(th_db, timeout=10)
    c = conn.cursor()
    q = 'update ' + th_table + ' set ItemIDs = ? where NodeName = ?'
    d = (list_ids, root.name)
    c.execute(q,d)

    conn.commit()
    conn.close()

def run(ts):
    """
        This function does:
            * Creates the Tree Schema(germination)
            * Update Nodes(leaves & accumulated) with item_count(count) & avg_popi in schema iteself
            * Creates & updates th_table for given timestamp(ts)
    """

    """ create the tree """
    startTime = time.time()
    pc.printWarn("\t\t .   .   .   .   .   .   .   .   .   ....... Tree Germination in progress .......    .   .   .   .   .   .   .   .   .\n")
    root = TreeGermination()
    pc.printSucc("\t\t <----------------------------------------------- Tree is Germinated ------------------------------------------------>\n")

    """ update leafnodes """
    pc.printWarn("\t\t .   .   .   .   .   .   .   .   .   ....... Updating Leaf(tag) Nodes.......    .   .   .   .   .   .   .   .   .\n")
    updateLeafNodes(ts)
    pc.printSucc("\t\t <--------------------------------------------- Leaf Nodes updated ------------------------------------------------>\n")

    """ update parents """
    pc.printWarn("\t\t .   .   .   .   .   .   .   .   .   ....... Updating Parent Nodes.......    .   .   .   .   .   .   .   .   .\n")
    updateParentNodes(root)
    pc.printSucc("\t\t <--------------------------------------------- Parent Nodes updated ------------------------------------------------>\n")
    
    """ NOTE: Print the Tree if you want """
    tree_printer_pretty.print_tree(root)  

    
    """ Create & Populate Tag Hotness(TH) Table"""
    pc.printWarn("\t\t .   .   .   .   .   .   .   .   .   ....... Creating & Populating TH Table .......    .   .   .   .   .   .   .   .   .\n")
    create_th(ts)
    update_th_mptt(root,1,1,ts)  # update_th_mptt(root,left,level,ts)
    pc.printSucc("\t\t <--------------------------------------------- TH Table Created & Populated ------------------------------------------------>\n")

    endTime = time.time()
    th_table = 'th_' + str(int(ts)) 
    pc.printWarn("\t\t ---------------> TIME TAKEN FOR th_creating@th (sec)   =>  {} => TABLE: {}\n".format(round((endTime - startTime),5),th_table))

    """ Update th_table for ItemIDs of wc_table """
    pc.printWarn("\t\t .   .   .   .   .   .   .   .   .   ....... Updating th_table for ItemIDs from wc_table.......    .   .   .   .   .   .   .   .   .\n")
    update_th_table_for_itemIDs(root,ts)
    pc.printSucc("\t\t <--------------------------------------------- th_table now has ItemIDs from wc_table ------------------------------------------------>\n")
