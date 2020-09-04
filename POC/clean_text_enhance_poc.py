from utilities import text_actions, web_requests
import re 
import string
from urlextract import URLExtract
  
def findUrl(intxt): 
  
    extractor = URLExtract()
    urls = extractor.find_urls(intxt)
    return ' '.join(urls)

def getStringFromUrls(intxt): #lets suppose its a url rn; will integrate with findUrl later
    # dont count 'http', 'https' 'www' 'com' etc???
    # return intxt.translate(str.maketrans('', '', string.punctuation))
    return re.sub('[^A-Za-z0-9]+', ' ', intxt)

def getUrlString(intxt):
    common_url_words = ['http', 'https', 'www', 'com']
    extractor = URLExtract()
    urls = extractor.find_urls(intxt)
    urlstring = ' '.join(urls)
    clean_url_string = re.sub('[^A-Za-z0-9]+', ' ', urlstring)
    print("clean_url_string: ",clean_url_string)
    clean_url_list = [w for w in clean_url_string.split()]
    print("clean_url_list: ",clean_url_list)
    new_list = [word for word in clean_url_list if word not in common_url_words]
    return ' '.join(new_list)
    

if __name__ == "__main__":
    # url = "https://www.reddit.com/r/compsci/comments/ij6x7g/pure_gold_the_internet_explained/"   #--------> FIXME: takin just the last comment in .summary()
    # url = "https://www.reddit.com/r/compsci/comments/ihxlif/compsci_weekend_superthread_august_28_2020/" #----> FIXME: skipping last heading
    # url = "https://www.reddit.com/r/compsci/comments/c15nbn/psa_this_is_not_rprogramming_quick_clarification/"  #---> Good
    # url = "https://www.reddit.com/r/compsci/comments/ikrxyq/my_turing_machine_simulator/" #-------> FIXME: getWeightedContent is not parsing urls
    # url = "https://www.reddit.com/r/compsci/comments/iku09s/map_of_computer_science/"  #------> FIXME: sicne there's no content in post, its givinv me content in /r About 
    # url = "https://www.reddit.com/r/compsci/comments/iklv6p/pythonsat_toy_package_manager_under_200_sloc_on/"


    # response = web_requests.hitGetWithRetry(url,'',False ,2,5,10)
    # if response.status_code == 200:
    #     content = text_actions.contentfromhtml(response)
    #     print("===============CONTENT================\n {} \n".format(content))
    #     wtcontent = text_actions.weightedcontentfromhtml(response)
    #     print("===============Wt-CONTENT================\n {} \n\n".format(wtcontent))
    #     intxt = content
    #     outtxt = text_actions.clean_text(intxt)
    #     print("===============<<<<<< clean_text(CONTENT): \n{}".format(outtxt))
    # intxt = """
    #     I'd like to share a master-piece article I fou::nd by ac/cident that explains the internet.

    #     If the author sees this, please know that I'm following you, keep being awesome.

    #     [https://explained-from-first-principles.com/internet/](https://explained-from-first-principles.com/internet/#number-encoding)"
    # """
    # # intxt = 'https://explained-from-first-principles.com/internet/'

    # print("===============>>>>>> INPUT: \n{}".format(intxt))
    # # print("===============<<<<<< URLS: \n{}".format(findUrl(intxt)))


    # # print("===============<<<<<< URLString: \n{}".format(getStringFromUrls(intxt)))
    # # outtxt = text_actions.clean_text(intxt)
    # outtxt = getUrlString(intxt)
    # print("===============<<<<<< OUTPUT: \n{}".format(outtxt))
    intext = """
    Share your information if you are looking for work. Please use this format:  Location:
        Remote:
        Willing to relocate:
        Technologies:
        Résumé/CV:
        Email:

    Readers: please only email these addresses to discuss work opportunities.
    """

    outtext = text_actions.clean_text(row["Content"]) 
