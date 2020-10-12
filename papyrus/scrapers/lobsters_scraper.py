import requests
import csv
import string
import time
from datetime import datetime

from collections import OrderedDict
from bs4 import BeautifulSoup

from readability import Document
import nltk

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def contentfromhtml(response):
    """
        get meaningful content from article page.Uses `readability` pkg
    """

    article = Document(response.text)
    html = article.summary()
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    return text


def weightedcontentfromhtml(response):
    """
        get emphasised words from meaningful content from article page
    """
    article = Document(response.text)
    html = article.summary()
    soup = BeautifulSoup(html)
    whitelist = [
        'h1',
        'h2',
        'h3',
        'h4',
        'strong',
        'title',
        'u',
        'a',
        # other elements,
        ]
    weightedcontent = ' '.join(t for t in soup.find_all(text=True) if t.parent.name in whitelist) 
    # imgaltcontent = ' '.join(img.get('alt') for img in soup.find_all('img') if soup.find_all('img') ) # FIXME: not working: TypeError: sequence item 0: expected str instance, NoneType found
    # return weightedcontent + imgaltcontent
    return weightedcontent

def clean_text(text):
    """Clean raw text using different methods :
       1. tokenize text
       2. lower text
       3. remove punctuation
       4. remove non-alphabetics char
       5. remove stopwords
       6. lemmatize
    """
    
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    stemmed = [wordnet.lemmatize(word) for word in words]
    return ' '.join(stemmed)

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
        ('law' , 'Law, patents, and licensing'),
        ('person' , 'Stories about particular persons'),
        ('philosophy' , 'Philosophy'),
        ('cogsci' , 'Cognitive Science'),
        ('crypto' , 'Cryptography'),
        ('education' , 'Education'),
        ('finance' , 'Finance and economics'),
        ('hardware' , 'Hardware'),
        ('math' , 'Mathematics'),
        ('science' , 'Science'),
        ('art' , 'Art'),
        ('book' , 'Books'),
        ('historical' , 'History-CSE'),
        ('job' , 'Job'),
        ('release' , 'Software Releases'),
        ('design' , 'Visual Design'),
        ('visualization' , 'Data Visualization'),
        ('assembly' , 'Assembly Language'),
        ('c' , 'C programming'),
        ('c++' , 'C++ programming'),
        ('clojure' , 'Clojure programming'),
        ('css' , 'Cascading Style Sheets'),
        ('d' , 'D programming'),
        ('dotnet' , 'C#, F#, .NET programming'),
        ('elixir' , 'Elixir programming'),
        ('elm' , 'Elm programming'),
        ('erlang' , 'Erlang development'),
        ('fortran' , 'Fortran programming'),
        ('go' , 'Golang programming'),
        ('haskell' , 'Haskell programming'),
        ('java' , 'Java programming'),
        ('javascript' , 'Javascript programming'),
        ('lisp' , 'Lisp programming'),
        ('nodejs' , 'Node.js programming'),
        ('objectivec' , 'Objective-C programming'),
        ('perl' , 'Perl'),
        ('php' , 'PHP programming'),
        ('python' , 'Python programming'),
        ('ruby' , 'Ruby programming'),
        ('rust' , 'Rust programming'),
        ('scala' , 'Scala programming'),
        ('swift' , 'Swift programming'),
        ('announce' , 'Site anouncement'),  
        ('android' , 'Android'),
        ('freebsd' , 'FreeBSD'),  #Not needed
        ('ios' , 'Apple iOS'),
        ('linux' , 'Linux'),
        ('mac' , 'Apple macOS'),
        ('unix' , 'Unix'),
        ('windows' , 'Windows'), 
        ('browsers' , 'Web Browsers'),
        ('cryptocurrencies' , 'Bitcoin and Cryptocurrencies'),
        ('games' , 'Game Design'),
        ('ipv6' , 'IPv6'),
        ('mobile' , 'Mobile Development'),
        ('web' , 'Web Development'),
        ('api' , 'API'),
        ('debugging' , 'Debugging'),
        ('devops' , 'DevOps'),
        ('performance' , 'Performance and optimization'),
        ('practices' , 'Development Practices'),
        ('privacy' , 'Privacy'),
        ('reversing' , 'Reverse engineering'), 
        ('scaling' , 'Scaling and architecture'),
        ('security' , 'Netsec, appsec, and infosec-Security'),
        ('testing' , 'Software Testing'),
        ('virtualization' , 'Virtualization'),
        ('compilers' , 'Compiler design'),
        ('databases' , 'Databases (SQL, NoSQL)'),
        ('emacs' , 'Emacs editor'),
        ('systemd' , 'Linux systemd'),
        ('vcs' , 'Git & VCS')
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
    wordnet = WordNetLemmatizer()

    for tag_code, tag_name in tags.items():
        csv_src_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/lobster/no_c/'+ str(tag_code) + '.csv'
        csv_dest_file = '/Users/aayush.chaturvedi/Sandbox/cynicalReader/data/lobster/wc/'+ str(tag_code) + '_wc.csv'

        f = csv.writer(open(csv_dest_file, "w"))          # Flush the old file
        f.writerow(['ID', 'Source', 'Tag_Code','Tag_Name','Title', 'Url','ProcessdedTitle', 'WeightedContent','Content'])

        with open(csv_src_file, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Headers are {", ".join(row)}')
                    line_count += 1
                url = row["Url"]
                print("sleeping for 0.1 second ZZZZZZzzzzzzzzz....................\n")
                time.sleep(0.1) 
                try:
                    response = requests.get(url,verify=False,timeout=30)
                    if response.status_code == 200:
                        content = contentfromhtml(response)  
                        weightedcontent = weightedcontentfromhtml(response)  
                        line_count += 1

                        f = csv.writer(open(csv_dest_file, "a"))          
                        f.writerow([
                                row["ID"],
                                row["Source"],
                                row["Tag_Code"],
                                row["Tag_Name"],
                                row["Title"],
                                row["Url"],
                                clean_text(row["Title"]),
                                clean_text(weightedcontent),
                                clean_text(content)])
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print("[@{}] ===> [{}] \t ID: {},  Title: {} \n".format(current_time,row["Tag_Code"],row["ID"],row["Title"]))
                    else:
                        print("[@{}] \txxxxx Found Error code: {} , SKIPPING...\n".format(current_time,response.status_code))
                except Exception as e:
                    print(" === XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ======\n >> [ID]= {} Skipping...Failed due to: {} \n".format(row["ID"], e))
                    pass
    print("\n\n********************** All the Scraping is Complete ***********************\n\n")
    

    """
        ======================== **X** ============================
    """