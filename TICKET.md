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


# HN_exclusive:

## [Ticket1] POC_Approach: Scrape Data & Build Model : ( 12Aug20- )
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

## [Ticket2] Get HN Topics List : (14Aug20-23Aug)
* **Target** : Get the list of all the big topics in last month of HN articles
* [] Figure Out scraping @Aayush
  * 1. HN Scrape: 
    * [x] Test which works better & meaningfully:
      * 1. [algolia](https://hn.algolia.com/api)   
      * 2. [HN's](https://blog.ycombinator.com/hacker-news-api/) - no tag for `Story` so, cant use
      * UPDATE: 
        * will go with algolia's `http://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=created_at_i>1597352419,created_at_i<1597525219,points>50`
        * Since API lim is 10k hits/hour; will give weekly epoch range & scrape per hour
        * Schema: ID,Source(=HN), Time(IST), Upvotes,NumComments, Title, Url 
  * 2. Inidvidual article linked website.Things to keep in mind:
    * Get meaningful content only i.e. remove ads, comments etc.
      * Appr1: Use someting like [boilerpipe](https://stackoverflow.com/questions/13791316/how-to-extract-meaningful-and-useful-content-from-web-pages) and use Adblockers data [ref](https://www.researchgate.net/post/How_do_I_extract_the_content_from_dynamic_web_pages)
      * App2: `python-readability` [link](https://github.com/buriy/python-readability) seems to work & gives only the main body(along with `doc.title()` & `doc.summary()`)
        * [] Test `python-readability` for credebility on misc types websites
        * [] if it works, still have to do:
          * remove videos/images
          * remove HTML tags(while keeping content inside <a> & <h12..>)-is there any way to give more weight to <hx>words</hx>
  * 99. Last resort-PAID service [simplescrapper](https://simplescraper.io/)
* [] Build LDA POC @Manchan for finding all the topics list on HN
  * Tfidf will give good result in topic prediction(with comparison to Lda & bag of word)
  * LDA => word1->topic1, word2->topic2 ; this is not what we need
  * [] Getting sentence-wise output Tfidf
  * [] Then; do the same for other algorithms => MNF performing better
  * [] Then; get data from @Aayush and do the best performing algo on it