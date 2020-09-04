# Overall Approach

- **Dictionary**(once): Prepare a curated list of Topics & their subtopics - `dictionary.json`
- **Logic**(once): Create an algo to rank every topic, subtopic & content
- **Scraping**(weekly) : Scrape content-websites(HN, reddit, twitter, PH, IH etc)
    - Do Keyword detection in scraped content: (topic/subtopic)–< nXn >–(content)
    - Tag each content with category(#1.News, #2.Product for now??)
    - Store the scraped content in DB against their (topic/subtopic)
    - After all the scraping is done; assign PopI to each topic & subtopic
    - Update DB with PopI column

- **Website/Newsletter**( once ):
    - Decide whether to keep newsletter of plain website
    - Create website (and if; newsletter system)


## [Ticket1] POC_Approach: Scrape Data & Build Model : ( 12Aug20-13Aug20)
* [x] Scrape data from [arxiv](https://arxiv.org/) for 5 categories- 1000 entries each
  * csv file: {id, topic, title , content}
  * ISSUE: too many errors with python2, upgrading to python3. Got stuck! UPDARE: resolved
* [x] Build & compare 2 NLP models(as learnt in Udemy):
  * #1. **Naïve Bayes**: `text_clf_nb = Pipeline([('tfidf', TfidfVectorizer()),('clf', MultinomialNB()),])`
  * #2 **Linear SVC**: `text_clf_lsvc = Pipeline([('tfidf', TfidfVectorizer()),('clf', LinearSVC()),])`
* [?] Decide which approach to go with(LDA perhaps?/Best possible score one?/)
  * UPDATE: Conclusion:
  * Sometimes Model1(NV) predicts wrong category with high accuracy 
  * Sometimes Model2(LSCV or LSCV2) predicts right category with low accuracy
  * Where to go from here??

## [Ticket2] Get HN Topics List : (14Aug20-18Aug20)
* **Target** : Get the list of all the big topics in last month of HN articles
* [-] Figure Out scraping @Aayush
  * 1. HN Scrape: 
    * [x] Test which works better & meaningfully:
      * 1. [algolia](https://hn.algolia.com/api)   
      * 2. [HN's](https://blog.ycombinator.com/hacker-news-api/) - no tag for `Story` so, cant use
      * UPDATE: 
        * will go with algolia's `http://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=created_at_i>1597352419,created_at_i<1597525219,points>50`
        * Since API lim is 10k hits/hour; will give weekly epoch range & scrape per hour
        * Schema: ID,Source(=HN), Time(IST), Upvotes,NumComments, Title, Url , Content, WeightedContent
        * [x] Handle brokern/forbidden urls
        * [x] handle https urls: tmp fixed(https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror), permanent soln later
        * Need to have full title(not preprocessed) as I need to decide the topic based on that.Preprocessing to be done while feeding to Algo.Made the change.RUN `hn_scraper` again after 1 iteration is done
        * HN scraping failed for '1596240000-1594771200', rerun!
  * 2. Inidvidual article linked website.Things to keep in mind:
    * Get meaningful content only i.e. remove ads, comments etc.
      * Appr1: Use someting like [boilerpipe](https://stackoverflow.com/questions/13791316/how-to-extract-meaningful-and-useful-content-from-web-pages) and use Adblockers data [ref](https://www.researchgate.net/post/How_do_I_extract_the_content_from_dynamic_web_pages)
      * App2: `python-readability` [link](https://github.com/buriy/python-readability) seems to work & gives only the main body(along with `doc.title()` & `doc.summary()`)
        * [x] Test `python-readability` for credebility on misc types websites
        * [x] if it works, still have to do:
          * HTML:
            * get text *outside* tags => Content
            * get text *inside* tags => WeightedContent
          * images => get `alt` value of <img> for WeightedContent col 
          * videos/Anything else  => remove
  * 99. Last resort-PAID service [simplescrapper](https://simplescraper.io/)
* [-] Build LDA POC @Richa for finding all the topics list on HN
  * Tfidf will give good result in topic prediction(with comparison to Lda & bag of word)
  * LDA => word1->topic1, word2->topic2 ; this is not what we need
  * [x] Getting sentence-wise output Tfidf
  * [x] Then; do the same for other algorithms => NMF performing better
  * [] Then; get data from @Aayush and do the best performing algo on it
* **CONCLUSION** :[18Aug20]
  * Since the HN datset was totally random, the coherence graph plotted with NMF was stratight line-showing that coherence score is independent of #topics(5-100) => No conclusion!
  * So decided to assume all major Topics manually and get data for each of topic from multiple sources; build model on it; then predict HN articles to decide the %accuracy threshold.
  * If this approach works-continue; else scrape the project!

## [Ticket3]: ~~Classify OR Die~~ Get everything(scripts, sources ,logic, concepts) needed to build backend : (19Aug20-28Aug20)
* **TARGET** : Build model on scrambled data set & see if it can classify HN's content.If not, scrape the project

* [-] **Classify OR Die**
  * [-] Build NLP model on:
    * [-] First: on some sample data @Richa
    * [] Feed all the data
  * [] Test this model on:
    * HN
    * Other computer/tech based blogs sites/aggregators
  * [] See if model can predict on HN:
    * if yes- proceed towards `%accuracy_th` -> `rank` -> ...
    * ~~else- Burst!~~ 
  
* [i] Create Topics list- with domains which are contained in them
  * NOTE: One article will have multiple topics; figure it out

* [x] Figure out Data Sources;
  * [-] Static Data sources:
    * [x] [lobste.rs](https://lobste.rs/)
    * [x] ~~Subreddits~~
    * [-] arxiv
    * [] Other sites similar to arxiv:
      * [list with #submissions](https://www.inlexio.com/rising-tide-preprint-servers/)
  * [x] Dynamic Data sources(for v1):
    * HN(need classification)
    * Subreddits => Comes tagged already. But I can
        * still classify the article to see if it belongs to other topics as well i.e. add finer tagging
    * Business
      * IndieHacker(tagged already)
      * Produchunt(tagged already)
  
    * For v2:
      * arxiv++(already tagged) => need permission; so later
      * Stackoverflow?
      * Jobs
        * Leetcode-articles?(tagged already)
        * gfg?


* [x] **Subscriptionn Plans**
  * Plan1($5 pm): Any 3 topics
  * Plan2($10 pm): All the topics
* [@] Ranking logic:
  * Sources:
    * How HN & Reddit ranks: [medium.article](https://medium.com/jp-tech/how-are-popular-ranking-algorithms-such-as-reddit-and-hacker-news-working-724e639ed9f7) , [research_paper](https://arxiv.org/pdf/1501.07860.pdf)
  * 1. Ranking subtopics in a topic: 
    * => Could be only on the basis of number of (#items in subtopic)/(#items in topic)
  * 2. Ranking items in a topic & subtopic
    * Logic:
      * ISSUE: newer posts have lower votes & comments => have to use log in ranking
        * Why log10: The first 10 upvotes have the same weight as the next 100 upvotes which have the same weight as the next 1000 etc
      * Have to give importance to both: #votes & #comments
      * ISSUE: {HN, PH,IH} has upvote(&no downvotes), {reddit} has upvotes & downvotes ;how to rank theses 2 groups with a single formula??
      * TODO: weight factor for each platform
      * TODO: give more rank to recent(but low voted) posts???????? => "This is not what I need"
      * TODO: I cant use any platform's(reddit,HN,IH etc) own rank as "this is not what I need"
      * QUESTION: Do I really need `log`???????????
    * References(read them all and make accordingly):
      * How reddit scores [article](https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9)
      * Wilson score: [How Not To Sort By Average Rating](https://www.evanmiller.org/how-not-to-sort-by-average-rating.html)
        * its [code](https://gist.github.com/amix/8d14ff0a920d5c15738a)
      * ranking platforms relatively: [weighted_means](https://stackoverflow.com/questions/3934579/algorithm-to-determine-most-popular-article-last-week-month-and-year)
      * very nice & relatable strackexchange problem: [here](https://softwareengineering.stackexchange.com/questions/229622/coming-up-with-a-valid-ranking-algorithm-for-articles)
      * Lengthy article: [Implementing Real-Time Trending Topics with a Distributed Rolling Count Algorithm in Storm](https://www.michael-noll.com/blog/2013/01/18/implementing-real-time-trending-topics-in-storm/)
      * z-scores to get the trending topics [stackoverflow](https://stackoverflow.com/questions/787496/what-is-the-best-way-to-compute-trending-topics-or-tags)
      * Indiehacker's formula [article](https://medium.com/@catsarebetter98/how-i-hacked-indiehackers-and-google-seo-7d3861cd52b4)
      * Quora's formula [here](https://www.quora.com/What-is-Quoras-algorithm-formula-for-determining-the-ordering-ranking-of-answers-on-a-question?no_redirect=1)
      * reddits scoring [code](https://github.com/reddit-archive/reddit/blob/8af415476bcbecc6729c20ada7fcd1d041495140/r2/r2/lib/db/_sorts.pyx#L62)

* [x] How to use Model as API
    * [How to use model as api using flask](https://towardsdatascience.com/deploying-a-machine-learning-model-as-a-rest-api-4a03b865c166)
* [@] How to do automatic continuous enhancement model
  * Scrape StaticSites every {month} & rebuild the model??




## [Ticket4] : Build the Core Stuff #nuff_said (28Aug20- <6Sep20>)

* [] Fix [@Ticket3]'s unfinished tasks, which were abandoned as of then
* [-] System Design for the entire thing: [figma](https://www.figma.com/file/f5jeKqGe94oaqLLZz7iCvd/CynicalReader?node-id=0%3A1)
  * **Notes**
    * There are 2 types of tags-list:
      * `SourceTags` : come from the source site itself- found while scraping
      * `ModelTags` : assigned by the NLP model 
    * Each tag has different confidence threshold value?
  * **To Figure Out**
    * phScraperNeed separate scraper(with comments) for PH 
      * OR can we make comments(or makers's comment) data as `content`
      * See the list of all the tags here :[PH](https://www.producthunt.com/topics) & assign them to my own dictionary manually
    * [x] figure out schema for Domain Subdomain DB(DSD-DB)
      * Just have weekly content-counts for each tag in DB & keep the Domain-subdomain mapping in code itself
    * [ ] How & where to store DB:
      * 1. WeeklyContentDB (WC-DB) :
        * NOTE: each week should has its own table. All tables belong to one DB
      * 2. Domain-SubdomainDB (DDS-DB)
        * Just one table with fixed columns(new cols for new tags to be added later)
      * 3. StaticContentDB(SC-DB) 
        * should be dumped to Drive or S3
    * [x] Can I get rid of Content & weighted content after model has run on item 
      * => NO, as its needed to be put in StaticDB(to train model later)

* [-] Restrue everything & Build all the `CoreStuff`
* [] TODO: figure out DBs-its affecting the coding
  * => **Tmp Soln** : use local csv files for dev
* [-] Scraping: <29Aug30-30Aug30>
  * [x] `hn_scraper.py`
    * Special Story cases:
      * [x] TellHN
      * [x] LaunchHN
    * [x] ShowHN: with just the text(not url) => put text in content
    * [x] AskHN: content
    * LATER: For Jobs@HN entries put `job` tag => later as these entries dont have upvotes/comments
    * NOTE: takes 30s for a week's data(500 entries avg)
  * [x] `r_scraper.py`
    * NOTE: takes about 3 mins for a week's data(6.5k entries avg)
    * [x] Enrichments for non-stupid scraping
  * [@] **Postponed for v2** create ih_scraper.py
    * NO API: scraping banned(same for PH)
  * [-] create ph_scraper.py
    * NOTE: takes 20 seconds for week's data(150 avg)
    * [x] Handle Retries for 'Rate Limit on API': 900 requests every 15 min.[doc](https://api.producthunt.com/v1/docs/rate_limits/headers) =>Add 2 retries after 16 mins gap
    * [-] Create separate dictinary for PH tags & link them to orignal_dictionary.
    * [x] Create separate db for products- Weekly Products DB (WP-DB).
      * WHY? Becuase Product content already has tags (& also not enough data to apply NLP on and I'm not planning to scrape comments & then do NLP rn), and need thumbnail url as well.So keep wc-db & wp-db separate.
  * [x] Create `content_scraper.py`
    * NOTE: Run time:
      * first run on 1 week's data=(HN+r) took `17.5 hours` for scraping alone! , get 12MB file
      * Post Enrichment: `3 hours`, file size = `13.5 MB`
      * Post Enrichment+Async: ???
    * [x]why does it wait forever??????????? (was doing the same when I was scraping originally too)
      * => Timeout of 10 seconds with #retries = 2
    * [x] Do updating in the same file??? => NO
    * [x] **Enrichments to do efficinet scraping** .Checks:
      * #CHECK1(pre scraping): if (content != NULL) => no scraping, just put it in as is content = clean_text(row["content"])
      * #CHECK2(pre scraping): if(url == NULL)=>discard(we dont want such entreis in newsletter, duh!)
      * #CHECK3(pre scraping): if (row["title"]==NULL)=>discard
      * #CHECK1(post scraping): if (content == null)&&(row["Title"] != null)=>row["weightedContent"] = clean_text(row["title"]) and row["Content"] = clean_text(row["title"])
      * Feature: weightedContetn += clean_text(row["title"])
      * FIXME: [x] for HN post with content exists, there's just title in final content....seriously WTF!!
      * FIXME: [x] weightedcontent is same as content for HN#274
      * TODO: [-] Try async for content downloading
        * [x] Demo: time reduced exponantially as compared to sync
        * [x] Remove ssl error - `ClientSession(headers={'Connection': 'keep-alive'})`
        * [x] How to limit max_number fo requests: `asyncio.Semaphore(1000)` 
        * [x] Run getcontentFromHtml, getWeightedContent etc on response
        * [x] Retries on error
        * [ ] How to read & write with excel file
        * [ ] how to embed in content_scraper
        * [ ] Run one scraping round & analyse
      * [x] is it better to run `content_scraper` in sync with `url_scrapers` 
        * => NO, because; if url_scrapers failed, there's not point in running content_scraper; so try max_time & max_retries for url_scrapers
  * [-] TODO: Enrichment of `clean_text` function:
    * 1. [] Dont waste urls~~/anchor tag~~'s data => it does contain useful information
    * TODO: fix `getcontentfromhtml` before next scraping
    * TODO: do this again after 2nd scraping is done(with new content_scrpae) **ISSUES with getting useful text:**
      * FOR REDDIT:
        * [] `readability` isnt reliable at all( something wrong with `Document(response.text).summary()` .Search for alternatives???
        * [x] `getweightedcontent` isnt parsing url to get words, just copying url as it is
          * => find all urls in text->get useful words(other than 'http','www','com'), call it `urlString`
            * add them to weightedContent
            * replace that part of content with urlString
        * [x] Add title in `getweightedcontent`
      * FOR HN:
    * ISSUES with clean_text:
      * [x] Add <space> when deleting a special character
      * [] Create my own dictionary to exempt few words from getting remove(like c++, .py, .js , Node.js etc)
   * Set upvotes/comments threshold values for HN, /r, PH
  * Make `PopICalc.py`
    * [] `hn_scraper.py` =>update STORY_UP_TH. set to 50 as of now.Update after seeing the results & all.
  * Make map of maps:
    * [] Link dictionary.md's `startup` /`product-release` / `saas` etc ???

## [Ticket5] : Build Prelaunch stuff(<7Sep20-14Sep20>)
* [] Create Website
* [] Create User Management System & User Dashboard
* [] Mail User Mailer
* [] Run `BackBone` for 2 weeks in parallel


## [Ticket6] : FuckinLaunch(<21Aug20>)