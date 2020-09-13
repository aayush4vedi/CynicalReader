import requests
import csv
import sys
import string
import time
from datetime import datetime

from collections import OrderedDict


if __name__ == '__main__':

    """
        Part1: Get all the tags and their names 
    """
    # url = 'https://lobste.rs/tags'
    # data = requests.get(url, timeout=None)
    # soup = BeautifulSoup(data.text, 'lxml')
    # divs = soup.findAll("ol", class_="category_tags")
    # for div in divs:
    #         # print(div) 
    #         tag_code = div.find('a', {'class': 'tag', 'href': True}).contents[0]
    #         tag_name = div.find_all('span')[0].contents[0]
    #         print('(\'{}\' , \'{}\'),'.format(tag_code, tag_name))
    """
        ======================== **X** ============================
    """
    csv.field_size_limit(sys.maxsize)
    tags = OrderedDict([
        ('ai' , 'AI-ML'),
        ('compsci' , 'CSE'),
        ('distributed' , 'Distributed Systems'),
        ('formalmethods' , 'CSE-Formal methods'),
        ('graphics' , 'Graphics Programming'),
        ('networking' , 'Networking'),
        ('osdev' , 'OS'),
        ('plt' , 'Programming Language Theory'),
        ('programming' , 'Programming'),
        ('culture' , 'Tech Communities and culture'),
        # ('law' , 'Law, patents, and licensing'),
        # ('person' , 'Stories about particular persons'),
        # ('philosophy' , 'Philosophy'),
        # ('cogsci' , 'Cognitive Science'),
        # ('crypto' , 'Cryptography'),
        # # ('education' , 'Education'),
        # # ('finance' , 'Finance and economics'),
        # # ('hardware' , 'Hardware'),
        # # ('math' , 'Mathematics'),
        # # ('science' , 'Science'),
        # # ('art' , 'Art'),
        # # ('book' , 'Books'),
        # # ('historical' , 'History-CSE'),
        # # ('job' , 'Job'),
        # ('release' , 'Software Releases'),
        # ('design' , 'Visual Design'),
        # ('visualization' , 'Data Visualization'),
        # ('assembly' , 'Assembly Language'),
        # ('c' , 'C programming'),
        # ('c++' , 'C++ programming'),
        # ('clojure' , 'Clojure programming'),
        # ('css' , 'Cascading Style Sheets'),
        # ('d' , 'D programming'),
        # ('dotnet' , 'C#, F#, .NET programming'),
        # ('elixir' , 'Elixir programming'),
        # ('elm' , 'Elm programming'),
        # ('erlang' , 'Erlang development'),
        # ('fortran' , 'Fortran programming'),
        # ('go' , 'Golang programming'),
        # ('haskell' , 'Haskell programming'),
        # ('java' , 'Java programming'),
        # ('javascript' , 'Javascript programming'),
        # ('lisp' , 'Lisp programming'),
        # ('nodejs' , 'Node.js programming'),
        # ('objectivec' , 'Objective-C programming'),
        # ('perl' , 'Perl'),
        # ('php' , 'PHP programming'),
        # ('python' , 'Python programming'),
        # ('ruby' , 'Ruby programming'),
        # ('rust' , 'Rust programming'),
        # ('scala' , 'Scala programming'),
        # ('swift' , 'Swift programming'),
        # ('announce' , 'Site anouncement'),  
        # ('android' , 'Android'),
        # ('freebsd' , 'FreeBSD'),  #Not needed
        # ('ios' , 'Apple iOS'),
        # ('linux' , 'Linux'),
        # ('mac' , 'Apple macOS'),
        # ('unix' , 'Unix'),
        # ('windows' , 'Windows'), 
        # ('browsers' , 'Web Browsers'),
        # ('cryptocurrencies' , 'Bitcoin and Cryptocurrencies'),
        # ('games' , 'Game Design'),
        # ('ipv6' , 'IPv6'),
        # ('mobile' , 'Mobile Development'),
        # ('web' , 'Web Development'),
        # ('api' , 'API'),
        # ('debugging' , 'Debugging'),
        # ('devops' , 'DevOps'),
        # ('performance' , 'Performance and optimization'),
        # ('practices' , 'Development Practices'),
        # ('privacy' , 'Privacy'),
        # ('reversing' , 'Reverse engineering'), 
        # ('scaling' , 'Scaling and architecture'),
        # ('security' , 'Netsec, appsec, and infosec-Security'),
        # ('testing' , 'Software Testing'),
        # ('virtualization' , 'Virtualization'),
        # ('compilers' , 'Compiler design'),
        # ('databases' , 'Databases (SQL, NoSQL)'),
        # ('emacs' , 'Emacs editor'),
        # ('systemd' , 'Linux systemd'),
        # ('vcs' , 'Git & VCS')
    ])

    """
        Part2: Scrape the tags page to get list of tagwise articles: titles & links
    """

    # page_cnt = 50

    # for tag_code, tag_name in tags.items():
    #     csv_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/lobster/no_c/'+ str(tag_code) + '.csv'
    #     f = csv.writer(open(csv_file, "w"))          
    #     f.writerow(['ID', 'Source','Tag_Code','Tag_Name', 'Title', 'Url'])

    #     index_cnt = 1
    #     for p in range(page_cnt):
    #         # url = 'https://lobste.rs/t/ai/page/' + str(p)
    #         url = 'https://lobste.rs/t/'+tag_code + '/page/' + str(p)
    #         data = requests.get(url, timeout=None)
    #         soup = BeautifulSoup(data.text, 'lxml')
    #         divs = soup.findAll("div", class_="details")
    #         # print(" ===== Total Items: {}\n\n".format(len(divs)))

    #         for div in divs:
    #             content = div.find('a', {'class': 'u-url', 'href': True})
    #             title = content.contents[0]
    #             url = content['href']
    #             f.writerow([
    #                 index_cnt,
    #                 "Lobsters",
    #                 tag_code,
    #                 tag_name,
    #                 title,
    #                 url
    #             ])
    #             index_cnt=index_cnt+1

    #     print(' ===> Written for " {} "\n\n'.format(tag_name))
    # print("\n**************** Done Writing!!! ******************\n")

    """
        ======================== **X** ============================
    """


    """
        Part3: Scrape each list to get article content
    """
    MAX_LINES = 500
    csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/POC/data/lobster/one_chunk_model_poc/lobsters_small_dataset.csv'

    f = csv.writer(open(csv_dest_file, "w"))          # Flush the old file
    f.writerow(['ID', 'Tag_Code','Tag_Name','Url','Title','ProcessdedTitle', 'WeightedContent','Content'])
    for tag_code, tag_name in tags.items():
        lines_in_file = 0 
        csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/POC/data/lobster/wc/'+ str(tag_code) + '_wc.csv'
        

        with open(csv_src_file, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            line_count = 0
            for row in csv_reader:
                if lines_in_file < MAX_LINES:
                    if line_count == 0:
                        print("Doing for: {}".format(tag_code))
                        line_count += 1
                    lines_in_file += 1
                    f = csv.writer(open(csv_dest_file, "a"))          
                    f.writerow([
                        row["ID"],
                        row["Tag_Code"],
                        row["Tag_Name"],
                        row["Url"],
                        row["Title"],
                        row["ProcessdedTitle"],
                        row["WeightedContent"],
                        row["Content"]
                        ])
    print("\n\n********************** Writing is Complete ***********************\n\n")
    

    """
        ======================== **X** ============================
    """