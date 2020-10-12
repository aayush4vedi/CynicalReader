from flask import render_template,request

from components import th_query
from utilities import global_wars as gw
from app import app

@app.route('/')
@app.route('/index')
def index():
    nodes = [ "root","cse","prog","career","social","business","sme","fin_eco","gen_cse","tcse","distribut_sys","data_struct","algo_dsa","gametheory","disco","crypto_cse","hardware","plt_cse","frmlmeth_cse","logic","ce","comparch","compiler","network","revengg","os","osdev","ios","android","mac","windows","linux","archlinux","unix","csa","hacking","robotics","arvr","iot","compvision","imgprocess","datamine","ml","gen_ml","ann","dl","ds","gen_ds","database","dataset","statistics","rlang","matlab","kaggle","datacleaning","nlp","ai","ds_tool","scala","scikit","jupyternote","de","bigdata","gen_bigdata","spark","hadoop","data_visn","gen_datavis","tableau","excel","gen_prog","db","webd","sdt","system","devpract","api","gamedev","codingchlg","opensrc","freesoft","lng_n_frmwrk","lng","proglng","plt","asm","c","cpp","golang","python","scala","elixir","elm","erlang","fortran","haskell","java","js","lisp","perl","php","ruby","rust","dotnet","kotlin","html","css","frmwrk","ror","django","reactjs","nodejs","prog_tools","git","virtualn","browser","aws","azure","k8s","docker","gcp","txt_edit","editor","vim","emacs","appdev","gen_appdev","iosdev","androiddev","devops","gen_devops","security","infosec","compsec","websec","privacy","crypto_cse","design","graphix","compgphix","webdes","ui","ux","jobs","prog_query","carr_query","interviewprep","interviewexp","technews","tech_discuss","tech_query","community","person","tech_blog","tech_law","cogsci","torrent","read_n_write","book","write","phil","history","gen_business","startup","freelance","saas","sideproj","market","seo","science","gen_science","sci_query","chemistry","biology","medicine","neuroscience","geology","env","health","physics","gen_physics","astro","quantum","nuclear","fluid_mech","engg","gen_engg","engg_ece","engg_electric","engg_query","engg_mech","engg_student","rocket","engg_struct","threedprint","maths","gen_maths","calculus","algebra","graphtheory","economics","finance","accounting","invest","blockchain","gen_blockchain","crypto_fin","bitcoin"]
    return render_template('index.html', title='Home',nodes = nodes)

@app.route('/query')
def getform():
    nodes = [ "root","cse","prog","career","social","business","sme","fin_eco","gen_cse","tcse","distribut_sys","data_struct","algo_dsa","gametheory","disco","crypto_cse","hardware","plt_cse","frmlmeth_cse","logic","ce","comparch","compiler","network","revengg","os","osdev","ios","android","mac","windows","linux","archlinux","unix","csa","hacking","robotics","arvr","iot","compvision","imgprocess","datamine","ml","gen_ml","ann","dl","ds","gen_ds","database","dataset","statistics","rlang","matlab","kaggle","datacleaning","nlp","ai","ds_tool","scala","scikit","jupyternote","de","bigdata","gen_bigdata","spark","hadoop","data_visn","gen_datavis","tableau","excel","gen_prog","db","webd","sdt","system","devpract","api","gamedev","codingchlg","opensrc","freesoft","lng_n_frmwrk","lng","proglng","plt","asm","c","cpp","golang","python","scala","elixir","elm","erlang","fortran","haskell","java","js","lisp","perl","php","ruby","rust","dotnet","kotlin","html","css","frmwrk","ror","django","reactjs","nodejs","prog_tools","git","virtualn","browser","aws","azure","k8s","docker","gcp","txt_edit","editor","vim","emacs","appdev","gen_appdev","iosdev","androiddev","devops","gen_devops","security","infosec","compsec","websec","privacy","crypto_cse","design","graphix","compgphix","webdes","ui","ux","jobs","prog_query","carr_query","interviewprep","interviewexp","technews","tech_discuss","tech_query","community","person","tech_blog","tech_law","cogsci","torrent","read_n_write","book","write","phil","history","gen_business","startup","freelance","saas","sideproj","market","seo","science","gen_science","sci_query","chemistry","biology","medicine","neuroscience","geology","env","health","physics","gen_physics","astro","quantum","nuclear","fluid_mech","engg","gen_engg","engg_ece","engg_electric","engg_query","engg_mech","engg_student","rocket","engg_struct","threedprint","maths","gen_maths","calculus","algebra","graphtheory","economics","finance","accounting","invest","blockchain","gen_blockchain","crypto_fin","bitcoin"]
    return render_template("query_form.html",title='Query Page',nodes = nodes)

@app.route('/queryresult', methods=['POST'])
def response():
    query = request.form.get("query")
    gw.TIMESTAMP_OF_THE_WEEK = 123421  #FIXME: fix the hack
    
    imm_children = th_query.return_imm_children(gw.TIMESTAMP_OF_THE_WEEK,query)
    hn_items , r_items = th_query.ReturnTopTenItemsofTag(query,gw.TIMESTAMP_OF_THE_WEEK,10)
    return render_template("showresults.html", title = "Show Results page",query = query,hn_items = hn_items,r_items = r_items,imm_children=imm_children)



@app.route('/itemresult/<node>')
def itemresult(node):
    labels = [
        'JANN', 'FEBB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]

    values = [
        967.67, 1190.89, 1079.75, 1349.19,
        2328.91, 2504.28, 2873.83, 4764.87,
        4349.29, 6458.30, 9907, 16297
    ]
    # imm_children = [
    #     967.67, 1190.89, 1079.75, 1349.19,
    #     2328.91, 2504.28, 2873.83, 4764.87,
    #     4349.29, 6458.30, 9907, 16297
    # ]

    gw.TIMESTAMP_OF_THE_WEEK = 123421  #FIXME: fix the hack
    bar_labels=labels
    bar_values=values
    
    imm_children = th_query.return_imm_children(gw.TIMESTAMP_OF_THE_WEEK,node)
    max_popi = 0
    max_cnt = 0
    if len(imm_children) > 0:
        max_popi = max(imm_children,key=lambda item:item[6])[6]
        max_cnt = max(imm_children,key=lambda item:item[5])[5]
    print("max_popi: ",max_popi)
    print("max_cnt: ",max_cnt)
    hn_items , r_items = th_query.ReturnTopTenItemsofTag(node,gw.TIMESTAMP_OF_THE_WEEK,10)
    return render_template("showresults.html", title = "Show Results page",query = node,hn_items = hn_items,r_items = r_items,imm_children=imm_children,max_popi=max_popi,max_cnt = max_cnt ,labels=bar_labels, values=bar_values)


@app.route('/bar')
def bar():
    labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]

    values = [
        967.67, 1190.89, 1079.75, 1349.19,
        2328.91, 2504.28, 2873.83, 4764.87,
        4349.29, 6458.30, 9907, 16297
    ]

    bar_labels=labels
    bar_values=values
    return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values)
