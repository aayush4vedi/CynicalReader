import re

""" Paste your updated text here"""
text = """


* 1. [x] Computer Science [<CSE>]  
  * [x] General CS Content <gen_cse>                     - [compsci@lobsters]                           -[r/compsci,r/computerscience]  
  * [x] Theoretical Computer Science  [<tcse>]                                                             
    * [x] Distributed systems <distribut_sys>             - [distributed@lobsters]                     -[r/distributed]
    * [x] Data Structures <data_struct>                              - [gfg??,]                        -[r/datastructures]
    * [x] Algorithms <algo_dsa>                         - [gfg??,]                                     -[r/algorithms,r/cpp_questions]         
    * [@] Coding Philosophy
    * [x] Game Theory <gametheory>                                                                      -[r/GAMETHEORY]
    * [x] Discrete Mathematics <disco>                                                                 -[r/Discretemathematics]
    * [x] Cryptography(0)<crypto_cse>                  - [crypto@lobsters,]                            -[r/crypto,r/cryptography]
    * [x] Hardware   <hardware>                         - [hardware@lobsters]
    * [@] Parallel Programming
    * [@] Computability Theory
    * [x] Programming Language Theory <plt_cse>          - [plt@lobsters]
    * [x] Formal Methods  <frmlmeth_cse>                     - [formalmethods@@lobsters]
    * [x] CSE & Mathematic Logic  <logic>                - ........                                    -[r/logic]
  * 1.2. [x] ComputerEngineering [<ce>]
    * [x] Computer Architecture <comparch>                                                             -[r/computerarchitecture]
    * [x] Compilers <compiler>                           - [compilers@lobsters]                        -[r/compilers]
    * [x] Computer Network  <network>                     - [networking@lobsters]                       -[r/Network]
    * [x] Reverse Engineering <revengg>              - [reversing@lobsters,]                       -[r/ReverseEngineering]
    * [x] Operating Systems [<os>]
      * [x] OS Dev <osdev>                               - [osdev@lobsters]                            -[r/osdev]
      * [x] iOS <ios>                                 - [ios@lobsters]
      * [x] android <android>                         - [android@lobsters]                          -[r/Android]
      * [x] macOS <mac>                               - [mac@lobsters]                              -[r/MacOS,r/osx]
      * [x] windows <windows>                         - [windows@lobsters]                          -[r/windows]
      * [x] Linux  <linux>                            - [linux@lobsters]                            -[r/linux,r/kernel,r/linuxdev,r/linuxquestions,r/Ubuntu]
      * [x] Archlinux <archlinux>                                                                   -[r/archlinux,r/linuxmasterrace]
      * [x] Unix <unix>                               - [unix@lobsters]
    * [@] [Software Development]
  * [x] CSApplications [<csa>]
    * [x] Hacking <hacking>                                                                            -[r/hacking,r/HowToHack,r/Hacking_Tutorials,r/hackers]
    * [x] Robotics(0)  <robotics>                                                                      -[r/robotics,r/arduino]
    * [x] AR-VR <arvr>                                                                                 -[r/virtualreality,r/augmentedreality]
    * [x] IOT <iot>                                                                                    -[r/IOT]
    * [x] Computer Vision <compvision>                                                                 -[r/computervision,r/opencv]
    * [x] Image Processing <imgprocess>                                                                -[r/imageprocessing,r/dip]
    * [x] Data Mining <datamine>                      -   .....                                        -[r/datamining,r/textdatamining]
    * [x] MachineLearning  [<ml>]
      *  [x] GeneralML <gen_ml>                               -  .....                                     -[r/MachineLearning,r/learnmachinelearning,r/ResearchML,r/neuralnetworks]
      *  [x] Artificial Neural Networks <ann>                                                            -[r/neuralnetworks,r/NeuralNetwork]
      *  [x] Deep Learning <dl>                                                                          -[r/neuralnetworks,r/deeplearning,r/DeepLearningPapers,r/deeplearners]
    * [x] DataScience [<ds>]                               -  .....                                        -[r/datascience,r/learndatascience]
      * [x] General Data Science <gen_dS>                               -  .....                                     -[r/datascience,r/learndatascience]
      * [x] Database(0) <database>                           - [databases@lobsters]                      -[r/Database]
      * [x] Datasets <dataset>                             -  ......                                     -[r/datasets]
      * [x] Statistics <statistics>                                                                      -[r/statistics,r/AskStatistics]
      * [x]  R Language<rlang>                                                                           -[r/Rlanguage,r/rstats]
      * [x]  Matlab <matlab>                                                                             -[r/matlab]
      * [x]  DS Tools [<ds_tool>]
        * [x] Scala <scala>                                                                              -[r/scala]
        * Pandas                                                                         
        * Matplotlib 
        * NLTK 
        * [x] Scikit-learn <scikit>                                                                      -[r/scikit_learn]
        * TensorFlow <tf>       
        * [x] Jupyter Notebook <jupyternote>                                                               -[r/JupyterNotebooks]
      *  [x] Kaggle <kaggle>                                                                              -[r/kaggle]
      *  [x] Data Cleaning <datacleaning>                                                                 -[r/datacleaning]
      * [x] NLP <nlp>                                                                                    -[r/NLP,r/LanguageTechnology]
        * Chatbot
    * [x] DataEngineering [<de>]
      * [x] [[<database>]]                                      - [databases@lobsters]                     -[r/Database]
      * [x] BigData [<bigdata>]
        * [x] General Big Data <gen_bigdata>                -  ......                                     -[r/bigdata]
        * [x] Apache Spark <spark>                                                                       -[r/apachespark]
        * [x] Hadoop <hadoop>                                                                            -[r/hadoop]
    * [x] DataVisualisation  [<data_visn>]
      * [x] General Data Visualisation <gen_datavis>          - [visualization@lobsters,]                   -[r/visualization,r/dataisbeautiful]
      * [x] Tableau <tableau>                                                                         -[r/tableau]
      * [x] Microsoft Excel <excel>                                                                   -[r/excel,r/ExcelTips]
    * [x] Artificial Intelligence  <ai>                                       - [ai@lobsters]                               -[r/artificial,r/ArtificialInteligence]
* Programming   / Software Development <prog>
  * General Programming <gen_prog>                      - [programming@lobsters]                      -[r/programming,r/coding,r/softwaredevelopment(0),r/SoftwareEngineering]
  * [x] Languages&Frameworks [<lng_n_frmwrk>]
    * [x] Languages [<lng>]
      * [x] Programming Languages  <proglng>              -  .......                                    -[r/ProgrammingLanguages,r/learnprogramming,r/functionalprogramming]
      * [x] Programming Language Theory <plt>             - [plt@lobsters]
      * [x] Assembly Language <asm>                     - [assembly@lobsters,]                        -[r/asm]
      * [x] C <c>                                     - [c@lobsters,]                               -[r/C_Programming,r/c_language]
      * [x] C++  <cpp>                                - [c++@lobsters,]                             -[r/cpp,r/Cplusplus]
      * [x] Golang <golang>                           - [go@lobsters]                               -[r/golang]
      * [x] Python <python>                           - [python@lobsters,]                          -[r/Python]
      * [x] Scala <scala>                             - [scala@lobsters,]                           -[r/scala]
      * [x] Elixir <elixir>                           - [elixir@lobsters]
      * [x] Elm <elm>                                 - [elm@lobsters]
      * [x] Erlang  <erlang>                          - [erlang@lobsters,]                          -[r/erlang]
      * [x] Fortran <fortran>                         - [fortran@lobsters]
      * [x] Haskell <haskell>                         - [haskell@lobsters,]                         -[r/haskell]
      * [x] Java <java>                               - [java@lobsters,]                            -[r/java]
      * [x] Javascript <js>                           - [javascript@lobsters,]                      -[r/javascript]
      * [x] Lisp <lisp>                               - [lisp@lobsters,]                            -[r/lisp]
      * [x] Perl <perl>                               - [perl@lobsters]                             -[r/perl]
      * [x] PHP <php>                                 - [php@lobsters,]                             -[r/PHP]
      * [x] Ruby <ruby>                               - [ruby@lobsters,]                            -[r/ruby]
      * [x] Rust <rust>                               - [rust@lobsters]                             -[r/rust]
      * [@] C#                                        - [dotnet@lobsters, ...]
      * [@] F#                                        - [dotnet@lobsters, ...]
      * [x] .NET <dotnet>                             - [dotnet@lobsters,]                          -[r/dotnet]
      * [x] Kotlin  <kotlin>                          -  .....                                      -[[r/Kotlin]
      * [x] HTML <html>                               - [css@lobsters, ...]                         -[r/HTML,/r/html5]
      * [x] CSS  <css>                                - [css@lobsters]                              -[r/css]
  * [x] Frameworks  [<frmwrk>]         
    * [x] Ruby on Rails <ror>                           - .....                                       -[r/rails]
    * [x] Django  <django>                              - .....                                       -[r/django]
    * [x] ReactJS <reactjs>                             - .....                                       -[r/reactjs]
    * [x] NodeJS <nodejs>                               - [nodejs@lobsters,r/node]
  * [x] ProgrammingTools [<prog_tools>]
    * [x] Git & VCS <git>                               - [vcs@lobsters]                              -[r/git,r/github,r/gitlab]
    * [x] Virtualization <virtualn>                     - [virtualization@lobsters]                   -[r/virtualization]
    * [x] Web Browsers <browser>                        - [browsers@lobsters]                         -[r/browsers]
    * [x] AWS <aws>                                     - .....                                       -[r/aws,r/AWS_cloud]
    * [x] Azure <azure>                                                                               -[r/AZURE,r/azuredevops]  
    * [x] Kubernetes <k8s>                                                                            -[r/kubernetes,r/k8s]  
    * [x] Docker <docker>                                                                             -[r/docker]
    * [x] GCP <gcp>                                                                                   -[r/GCP]                  
    * [x] TextEditors [<txt_edit>]
      * [x] Editors <editor>                              - [emacs@lobsters,...]
      * [x] Vim <vim>                                                                                 -[r/vim,r/neovim,r/vim_magic]
      * [x] Emacs <emacs>                                                                             -[r/emacs]
  * [x] AppDevelopment [<appdev>]
    * [x] General App Development <gen_appdev>              - [mobile@lobsters]                          -[r/appdev,r/AppDevelopment]
    * [x] iOS Dev <iosdev>                                  - [ios@lobsters]                             -[r/iosdev,r/iOSProgramming]
    * [x] Android Dev <androiddev>                          - [android@lobsters]                         -[r/androiddev]
  * [x] DevOps [<devops>]
    * [x] General DevOps <gen_devops>                        - [devops@lobsters]                           -[r/devops]
    * [x] [AWS](1) 
    * [x] [Azure](1)
    * [x] [Kubernetes](1)
    * [x] [Docker](1)
    * [x] [GCP](1)
  * [x] Security  [<security>]
    * [x] Information Security <infosec>               - [security@lobsters]                         -[r/netsec]
    * [x] Computer Security <compsec>                   - .....                                       -[[r/compsec]
    * [x] Web Security <websec>                         - .....                                       -[[r/websec]
    * [x] Privacy <privacy>                             - [privacy@lobsters]                          -[r/privacy]
    * [x] Cryptography(1)<crypto_cse>                   - [crypto@lobsters,]                          -[r/crypto,r/cryptography]
  * [@] System Design
  * [x] Design [<design>]
    * [x] Graphix Design  <graphix>                     - [design@lobsters]
    * [x] Computer Graphics <compgphix>                 - [graphics@@lobsters,]                       -[r/computergraphics]
    * [x] Web Design <webdes>                           - .....                                       -[r/web_design]
    * [x] UI <ui>                                                                                     -[r/UI_Design,r/UI_programming]
    * [x] UX <ux>                                                                                     -[r/UXDesign,r/UXResearch,r/UX_Design]
  * [x] Database <db>                                    - .....                                    -[r/Database]
      * SQL
      * MongoDB
      * Cassandra
      * DashDB 
  * [x] Web Development <webd>                       - [web@lobsters,]                            -[r/webdev]
  * [@] Software Releases                            - [release@lobsters,announce@lobsters]
  * [@] Debugging                                    - [debugging@lobsters]
  * [x] Software Testing <sdt>                      - [testing@lobsters]                         -[r/softwaretesting]
  * [@] Scaling                                     - [scaling@lobsters]
  * [x] System Performance & Optimisation <system>  - [performance@lobsters,]                     -[r/systems]
  * [x] Development Practices <devpract>            - [practices@lobsters,]                       -[r/tinycode,r/softwaredevelopment(2)]
  *  Acrhitecture
  * Product Management 
  * [x] API <api>                                       - [api@lobsters]                              -[r/api]
  * [x] Game Dev <gamedev>                         - [games@lobsters,]                           -[r/gamedev]
  * [x] Coding Challanges<codingchlg> (0)               - .....                                       -[r/programmingchallenges]
  * [@] Law, patents, and licensing(+2)                 - [law@lobsters]
  * [x] Open Source (0) <opensrc>                       - .....                                       -[[r/opensource]
  * [x] Free Software <freesoft>                        -  ....                                       -[r/freeculture,r/freesoftware]
  * [x] [[<os>]]
  * [x] Technical Queries <prog_query>(0)               - .....                                     -[r/AskComputerScience,askHN]
* [x] Career [<career>]
  * [x] Jobs <jobs>                                    - [job@lobsters]                               -[r/forhire]
  * [x] Career Queestions<carr_query>                    - .....                                      -[r/cscareerquestions]
  * [@] Openings
  * [x] Interview Preparation <interviewprep>                                                          -[r/interviewpreparations,r/csinterviewproblems]
  * [x] Interview Experiences <interviewexp>                                                           -[r/interviews]
  * [x] [Coding Challanges](1)    
* [x] Social [<social>] (or Community) 
  * [x] Tech News <technews>                       - .....                                            - [r/technology,r/TrueReddit,r/wikipedia,r/geek]                          
  * [x] Technical discussions <tech_discuss>                 - .....                                  - [tellHN]
  * [x] Technical Queries <tech_query>(1)                       - .....                               - [r/AskComputerScience(1),askHN(1)]
  * [x] Technical communities and culture <community>   -[culture@lobsters]                           - [r/skeptic]                     
  * Social Philosophy                                   - ......                                      - [r/Agorism]
  * Rants(rant@lobsters)
  * Stories about particular persons <person>       - [person@lobsters]
  * Interviews -->
  * [x] Blogs <tech_blog>                                                                             - [r/blog]
  * Education                                            - [education@lobsters] 
  * Travel/Geography 
  * [x] Law, patents, and licensing <tech_law>          - [law@lobsters]                              -[r/COPYRIGHT,r/noip]
  * Politics 
  * Intellectual Property Laws                           - ...                                         - [r/noip] 
  * [x] Cognitive Science <cogsci>                      - [cogsci@lobsters]                           - [r/cognitivescience]
  * [x] Torrents <torrent>                                                                            - [r/torrents]
  * [x] Reading&Writing [<read_n_write>]
    * Art                                            - [art@lobsters]  
    * [x] Books  <book>                                 - [book@lobsters]                             - [r/books,r/scifi,r/bookclub]
    * [x] Writing <write>                                                                           - [r/writing]
    * [x] Philosophy(general)  <phil>  ...              - .....                                       - [r/atheism,r/philosophy]
    * [x] History <history>                             - [historical@lobsters]                       - [r/history,r/AskHistorians]
* 6. Business [<business>]
  * [x] Gen. Business <gen_business>                        - .....                                       - [r/business,r/Flipping]
  * [x] Startup  <startup>                              - .....                                       - [launchHN,PH,r/startups,r/Entrepreneur,r/digitalnomad]
  * [x] Freelancing <freelance>                                                                       - [r/freelance,r/Upwork]
  * [x] Saas <saas>                                                                                   - [r/SaaS]
  * [x] Side Project <sideproj>                         - ......                                      - [showHN,r/SideProject]
  * [x] Marketing & Advertising <market>               - .....                                        - [r/marketing]
  * [x] SEO <seo>                                  - .....                                        - [r/SEO,r/bigseo,r/SEO_Digital_Marketing]
  * [x] [[<opensrc>]](1)                                 - .....                                        - [r/opensource]
* [x] Science [<science>]
  * [x] General Science <gen_science>                             - [science@lobsters]                    - [r/science]
  * [x] Scinece Queries <sci_query>                                                                   - [r/askscience,r/AskPhysics]
  * [x] Chemistry <chemistry>                                                                         - [r/chemistry]
  * [x] Biology <biology>                                                                             - [r/biology]
  * [x] Medicine <medicine>                                                                           - [r/medicine]
  * [x] Neuroscience <neuroscience>                                                                   - [r/neuroscience]
  * [x] Geology <geology>                                                                             - [r/geology]
  * [x] Ecology/Environment <env>                                                                      - [r/environment]
  * Psychology                                                                            
  * [x] Health <health>                                                                                - [r/Health]
  * [x] Physics [<physica>]
    * [x] Gen. Physics <gen_physics>                                                                      - [r/Physics]
    * [x] Astronomy, Astrophysics, space <astro>                                                      - [r/space,r/aerospace]  #TODO: add more for 'astro' part
    * [x] Quantum Physics <quantum>                                                                   - [r/quantum,r/QuantumPhysics]
    * [x] Nuclear Physics <nuclear>                                                                   - [r/energy]
    * [x] Fluid Mechanics <fluid_mech>                                                                - [r/FluidMechanics]
* [x] Engineering  [<engg>]
  * [x] Gen. Engineering <gen_engg>                                                                         - [r/engineering]   
  * [x] Electronics Engg <engg_ece>                                                                         - [r/electronics,r/ECE]
  * [x] Electrical Engg <engg_electric>                                                                - [r/ElectricalEngineering]
  * [x] Engineering Queries <engg_query>                                                               - [r/AskEngineers,r/LearnEngineering,r/AskElectronics]
  * [x] Mechanical Engineering <engg_mech>                                                        - [r/MechanicalEngineering]
  * [x] Engineering Students <engg_student>                                                            - [r/EngineeringStudents]
  * [x] Aviation, Rockets & aerodynamics <rocket>                                                      - [r/rocketry,r/aviation,r/nasa,r/spacex,r/aerodynamics]
  * [x] Structural Engineering <engg_struct>                                                           - [r/StructuralEngineering]
  * [x] [[<robotics>]](1)   
  * [x] 3D Printing <3dprint>                                                                          - [r/3Dprinting]
* [x] Mathematics [<maths>]
  * [x] Gen.Mathematics <gen_maths>                           - [math@lobsters,]                            - [r/math,r/mathematics]
  * [@] Geometry
  * [x] Calculus <calculus>                                                                           -[r/calculus,r/DifferentialEquations]
  * [x] Algebra <algebra>                                                                             -[r/Algebra] 
  * [x] [<gametheory>]
  * [x] Graph Theory <graphtheory>                                                                    -[r/GraphTheory]
  * [x] [[<logic>]](1)                                       - .....                                       -[r/logic(1)]
  * [x] [[<disco>]](1)    
  * [x] [[<statistics>]](1-R_part)                          - .....                                       - [r/statistics]
  * [x] [[<crypto_cse>]](2)                               - [crypto@lobsters,]                          -[r/crypto,r/cryptography]
* [x] Finance&Economics [<fin_eco>]
  * [x] Economics <economics>                                                                         -[r/Economics,r/economy]
  * [x] Finance & Personal Finance  <finance>                              - [finance@lobsters]                          -[r/finance,r/personalfinance]
  * Money
  * [x] Accounting <accounting>                                                                       -[r/Accounting]
  * [x] Investment <invest>                                                                           -[r/invest,r/investing]
  * [x] Blockchain [<blockchain>]
    * [x] Gen. Blockchain <gen_blockchain>                                                                       -[r/BlockchainStartups]
    * [x] Cryptocurrencies <crypto_fin>                   - [cryptocurrencies@lobsters]                 -[r/CryptoCurrency]
    * [x] Bitcoin <bitcoin>                             - .....                                       -[r/Bitcoin,r/BitcoinBeginners,r/bitcointrading,r/BitcoinDiscussion]


"""

text2 = """

root = Node("Root",isTag=False)

    cse_n            = Node("cse",isTag=False)
    prog_n           = Node("prog",isTag=False)
    career_n         = Node("career",isTag=False)
    social_n         = Node("social",isTag=False)
    business_n       = Node("business",isTag=False)
    sme_n            = Node("sme",isTag=False)
    fin_eco_n        = Node("fin_eco",isTag=False)

    root.add_child(cse_n)
    root.add_child(prog_n)
    root.add_child(career_n)
    root.add_child(social_n)
    root.add_child(business_n)
    root.add_child(sme_n)
    root.add_child(fin_eco_n)


    gencse_n = Node("gen_cse")
    cse_n.add_child(gencse_n)

    tcse_n = Node("tcse",isTag=False)
    cse_n.add_child(tcse_n)

    distribut_sys_n     =  Node("distribut_sys")
    data_struct_n       =  Node("data_struct")
    algo_dsa_n          =  Node("algo_dsa")
    gametheory_n        =  Node("gametheory")
    disco_n             =  Node("disco")
    crypto_cse_n        =  Node("crypto_cse")
    hardware_n          =  Node("hardware")
    plt_cse_n           =  Node("plt_cse")
    frmlmeth_cse_n      =  Node("frmlmeth_cse")
    logic_n             =  Node("logic")

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

    ce_n = Node("ce",isTag=False)
    cse_n.add_child(ce_n)

    comparch_n          = Node("comparch")    
    compiler_n          = Node("compiler")
    network_n           = Node("network")
    revengg_n           = Node("revengg")

    ce_n.add_child(comparch_n)    
    ce_n.add_child(compiler_n)
    ce_n.add_child(network_n)
    ce_n.add_child(revengg_n)

    os_n = Node("os",isTag=False)
    ce_n.add_child(os_n)

    osdev_n         = Node("osdev")
    ios_n           = Node("ios")
    android_n       = Node("android")
    mac_n           = Node("mac")
    windows_n       = Node("windows")
    linux_n         = Node("linux")
    archlinux_n     = Node("archlinux")
    unix_n          = Node("unix")

    os_n.add_child(osdev_n)
    os_n.add_child(ios_n)
    os_n.add_child(android_n)
    os_n.add_child(mac_n)
    os_n.add_child(windows_n)
    os_n.add_child(linux_n)
    os_n.add_child(archlinux_n)
    os_n.add_child(unix_n)

    csa_n = Node("csa",isTag=False)
    cse_n.add_child(csa_n)


    hacking_n       = Node("hacking")
    robotics_n      = Node("robotics")
    arvr_n          = Node("arvr")
    iot_n           = Node("iot")
    compvision_n    = Node("compvision")
    imgprocess_n    = Node("imgprocess")    
    datamine_n      = Node("datamine")

    csa_n.add_child(hacking_n)
    csa_n.add_child(robotics_n)
    csa_n.add_child(arvr_n)
    csa_n.add_child(iot_n)
    csa_n.add_child(compvision_n)
    csa_n.add_child(imgprocess_n)
    csa_n.add_child(datamine_n)

    ml_n = Node("ml",isTag=False)
    csa_n.add_child(ml_n)

    gen_ml_n    = Node("gen_ml")
    ann_n       = Node("ann")
    dl_n        = Node("dl")

    ml_n.add_child(gen_ml_n)
    ml_n.add_child(ann_n)
    ml_n.add_child(dl_n)

    ds_n = Node("ds",isTag=False)
    csa_n.add_child(ds_n)

    gen_dS_n          = Node("gen_dS")
    database_n        = Node("database")
    dataset_n         = Node("dataset")
    statistics_n      = Node("statistics")
    rlang_n           = Node("rlang")
    matlab_n          = Node("matlab")
    kaggle_n          = Node("kaggle")
    datacleaning_n    = Node("datacleaning")
    nlp_n             = Node("nlp")
    ai_n              = Node("ai")

    ds_n.add_child(gen_dS_n)
    ds_n.add_child(database_n)
    ds_n.add_child(dataset_n)
    ds_n.add_child(statistics_n)
    ds_n.add_child(rlang_n)
    ds_n.add_child(matlab_n)
    ds_n.add_child(kaggle_n)
    ds_n.add_child(datacleaning_n)
    ds_n.add_child(nlp_n)
    ds_n.add_child(ai_n)

    ds_tool_n = Node("ds_tool",isTag=False)
    ds_n.add_child(ds_tool_n)

    scala_n             = Node("scala")    
    scikit_n            = Node("scikit")
    jupyternote_n       = Node("jupyternote")

    ds_tool_n.add_child(scala_n)
    ds_tool_n.add_child(scikit_n)
    ds_tool_n.add_child(jupyternote_n)

    de_n = Node("de",isTag=False)
    csa_n.add_child(de_n)

    de_n.add_child(database_n)

    bigdata_n = Node("bigdata",isTag=False)
    de_n.add_child(bigdata_n)

    gen_bigdata_n       = Node("gen_bigdata")
    spark_n             = Node("spark")
    hadoop_n            = Node("hadoop")

    bigdata_n.add_child(gen_bigdata_n)
    bigdata_n.add_child(spark_n)
    bigdata_n.add_child(hadoop_n)


    gen_prog_n          = Node("gen_prog")
    db_n                = Node("db")
    webd_n              = Node("webd")
    sdt_n               = Node("sdt")
    system_n            = Node("system")
    devpract_n          = Node("devpract")
    api_n               = Node("api")
    gamedev_n           = Node("gamedev")
    codingchlg_n        = Node("codingchlg")
    opensrc_n           = Node("opensrc")
    freesoft_n          = Node("freesoft")

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

    lng_n_frmwrk_n = Node("lng_n_frmwrk",isTag=False)
    prog_n.add_child(lng_n_frmwrk_n)

    lng_n = Node("lng",isTag=False)
    lng_n_frmwrk_n.add_child(lng_n)


    proglng_n       = Node("proglng")
    plt_n           = Node("plt")
    asm_n           = Node("asm")
    c_n             = Node("c")
    cpp_n           = Node("cpp")
    golang_n        = Node("golang")
    python_n        = Node("python")
    scala_n         = Node("scala")
    elixir_n        = Node("elixir")
    elm_n           = Node("elm")
    erlang_n        = Node("erlang")
    fortran_n       = Node("fortran")
    haskell_n       = Node("haskell")
    java_n          = Node("java")
    js_n            = Node("js")
    lisp_n          = Node("lisp")
    perl_n          = Node("perl")
    php_n           = Node("php")
    ruby_n          = Node("ruby")
    rust_n          = Node("rust")
    dotnet_n        = Node("dotnet")
    kotlin_n        = Node("kotlin")
    html_n          = Node("html")
    css_n           = Node("css")

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

    frmwrk_n = Node("frmwrk",isTag=False)
    lng_n_frmwrk_n.add_child(frmwrk_n)


    ror_n           = Node("ror")
    django_n        = Node("django")
    reactjs_n       = Node("reactjs")
    nodejs_n        = Node("nodejs")

    frmwrk_n.add_child(ror_n)
    frmwrk_n.add_child(django_n)
    frmwrk_n.add_child(reactjs_n)
    frmwrk_n.add_child(nodejs_n)

    prog_tools_n = Node("prog_tools",isTag=False)
    prog_n.add_child(prog_tools_n)

    git_n          = Node("git")
    virtualn_n     = Node("virtualn")
    browser_n      = Node("browser")
    aws_n          = Node("aws")
    azure_n        = Node("azure")
    k8s_n          = Node("k8s")
    docker_n       = Node("docker")
    gcp_n          = Node("gcp")

    prog_tools_n.add_child(git_n)
    prog_tools_n.add_child(virtualn_n)
    prog_tools_n.add_child(browser_n)
    prog_tools_n.add_child(aws_n)
    prog_tools_n.add_child(azure_n)
    prog_tools_n.add_child(k8s_n)
    prog_tools_n.add_child(docker_n)
    prog_tools_n.add_child(gcp_n)

    txt_edit_n = Node("txt_edit",isTag=False)
    prog_tools_n.add_child(txt_edit_n)

    editor_n       = Node("editor")
    vim_n          = Node("vim")
    emacs_n        = Node("emacs")

    txt_edit_n.add_child(editor_n)
    txt_edit_n.add_child(vim_n)
    txt_edit_n.add_child(emacs_n)

    appdev_n = Node("appdev",isTag=False)
    prog_n.add_child(appdev_n)

    gen_appdev_n       = Node("gen_appdev")
    iosdev_n           = Node("iosdev")
    androiddev_n       = Node("androiddev")

    appdev_n.add_child(gen_appdev_n)
    appdev_n.add_child(iosdev_n)
    appdev_n.add_child(androiddev_n)

    devops_n = Node("devops",isTag=False)
    prog_n.add_child(devops_n)

    gen_devops_n       = Node("gen_devops")

    devops_n.add_child(gen_devops_n)
    devops_n.add_child(aws_n)
    devops_n.add_child(azure_n)
    devops_n.add_child(k8s_n)
    devops_n.add_child(docker_n)
    devops_n.add_child(gcp_n)

    security_n = Node("security",isTag=False)
    prog_n.add_child(security_n)

    infosec_n          = Node("infosec")
    compsec_n          = Node("compsec")
    websec_n           = Node("websec")
    privacy_n          = Node("privacy")
    crypto_cse_n       = Node("crypto_cse")

    security_n.add_child(infosec_n)
    security_n.add_child(compsec_n)
    security_n.add_child(websec_n)
    security_n.add_child(privacy_n)
    security_n.add_child(crypto_cse_n)

    design_n = Node("design",isTag=False)
    prog_n.add_child(design_n)

    graphix_n      = Node("graphix")
    compgphix_n    = Node("compgphix")
    webdes_n       = Node("webdes")
    ui_n           = Node("ui")
    ux_n           = Node("ux")

    design_n.add_child(graphix_n)
    design_n.add_child(compgphix_n)
    design_n.add_child(webdes_n)
    design_n.add_child(ui_n)
    design_n.add_child(ux_n)


    jobs_n              = Node("jobs")
    carr_query_n        = Node("carr_query")
    interviewprep_n     = Node("interviewprep")
    interviewexp_n      = Node("interviewexp")

    career_n.add_child(jobs_n)
    career_n.add_child(carr_query_n)
    career_n.add_child(interviewprep_n)
    career_n.add_child(interviewexp_n)


    technews_n          =  Node("technews")
    tech_discuss_n      =  Node("tech_discuss")
    tech_query_n        =  Node("tech_query")
    community_n         =  Node("community")
    person_n            =  Node("person")
    tech_blog_n         =  Node("tech_blog")
    tech_law_n          =  Node("tech_law")
    cogsci_n            =  Node("cogsci")
    torrent_n           =  Node("torrent")

    social_n.add_child(technews_n)
    social_n.add_child(tech_discuss_n)
    social_n.add_child(tech_query_n)
    social_n.add_child(community_n)
    social_n.add_child(person_n)
    social_n.add_child(tech_blog_n)
    social_n.add_child(tech_law_n)
    social_n.add_child(cogsci_n)
    social_n.add_child(torrent_n)

    read_n_write_n = Node("read_n_write",isTag=False)
    social_n.add_child(read_n_write_n)
    
    book_n          =  Node("book")
    write_n         =  Node("write")
    phil_n          =  Node("phil")
    history_n       =  Node("history")

    read_n_write_n.add_child(book_n)
    read_n_write_n.add_child(write_n)
    read_n_write_n.add_child(phil_n)
    read_n_write_n.add_child(history_n)


    gen_business_n      =  Node("gen_business")
    startup_n           =  Node("startup")
    freelance_n         =  Node("freelance")
    saas_n              =  Node("saas")
    sideproj_n          =  Node("sideproj")
    market_n            =  Node("market")
    seo_n               =  Node("seo")

    business_n.add_child(gen_business_n)
    business_n.add_child(startup_n)
    business_n.add_child(freelance_n)
    business_n.add_child(saas_n)
    business_n.add_child(sideproj_n)
    business_n.add_child(market_n)
    business_n.add_child(seo_n)
    business_n.add_child(opensrc_n)

    science_n = Node("science",isTag=False)
    sme_n.add_child(science_n)   

    gen_science_n       =  Node("gen_science")
    sci_query_n         =  Node("sci_query")
    chemistry_n         =  Node("chemistry")
    biology_n           =  Node("biology")
    medicine_n          =  Node("medicine")
    neuroscience_n      =  Node("neuroscience")
    geology_n           =  Node("geology")
    env_n               =  Node("env")
    health_n            =  Node("health")

    science_n.add_child(gen_science_n)
    science_n.add_child(sci_query_n)
    science_n.add_child(chemistry_n)
    science_n.add_child(biology_n)
    science_n.add_child(medicine_n)
    science_n.add_child(neuroscience_n)
    science_n.add_child(geology_n)
    science_n.add_child(env_n)
    science_n.add_child(health_n)


    physics_n = Node("physics",isTag=False)
    science_n.add_child(physics_n) 

    gen_physics_n       =  Node("gen_physics")
    astro_n             =  Node("astro")
    quantum_n           =  Node("quantum")
    nuclear_n           =  Node("nuclear")
    fluid_mech_n        =  Node("fluid_mech")

    physics_n.add_child(gen_physics_n)
    physics_n.add_child(astro_n)
    physics_n.add_child(quantum_n)
    physics_n.add_child(nuclear_n)
    physics_n.add_child(fluid_mech_n)

    engg_n = Node("engg",isTag=False)
    sme_n.add_child(engg_n)

    gen_engg_n          =  Node("gen_engg")
    engg_ece_n          =  Node("engg_ece")
    engg_electric_n     =  Node("engg_electric")
    engg_query_n        =  Node("engg_query")
    engg_mech_n         =  Node("engg_mech")
    engg_student_n      =  Node("engg_student")
    rocket_n            =  Node("rocket")
    engg_struct_n       =  Node("engg_struct")
    threedprint_n       =  Node("threedprint")

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

    maths_n = Node("maths",isTag=False)
    sme_n.add_child(maths_n)   

    gen_maths_n         =  Node("gen_maths")
    calculus_n          =  Node("calculus")
    algebra_n           =  Node("algebra")
    graphtheory_n       =  Node("graphtheory")

    maths_n.add_child(gen_maths_n)
    maths_n.add_child(calculus_n)
    maths_n.add_child(algebra_n)
    maths_n.add_child(gametheory_n)
    maths_n.add_child(graphtheory_n)
    maths_n.add_child(logic_n)
    maths_n.add_child(disco_n)
    maths_n.add_child(statistics_n)
    maths_n.add_child(crypto_cse_n)


    economics_n     =  Node("economics")
    finance_n       =  Node("finance")
    accounting_n    =  Node("accounting")
    invest_n        =  Node("invest")

    fin_eco_n.add_child(economics_n)
    fin_eco_n.add_child(finance_n)
    fin_eco_n.add_child(accounting_n)
    fin_eco_n.add_child(invest_n)

    blockchain_n    =  Node("blockchain",isTag=False)    
    fin_eco_n.add_child(blockchain_n)

    gen_blockchain_n      = Node("gen_blockchain")
    crypto_fin_n          = Node("crypto_fin")
    bitcoin_n             = Node("bitcoin")

    blockchain_n.add_child(gen_blockchain_n)
    blockchain_n.add_child(crypto_fin_n)
    blockchain_n.add_child(bitcoin_n)

"""

tags = re.findall('<(.*?)>', text)
# tags = re.findall('("(.*?)")', text2)

for tag in tags:
    print('"{}",'.format(tag))
