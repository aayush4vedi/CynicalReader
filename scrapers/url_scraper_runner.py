from scrapers.urlScrapers import hn_scraper, r_scraper


def run(ts):

    """ Runs following scrapers serially and updates them in WC-DB:
        1. hn_scraper.py
        2. r_scraper.py
        3. ih_scraper.py
        4. ph_scraper.py

        Input: float(timestamp) - set when the main.py run is triggered
            * float because o/w `datetime.fromtimestamp(ts)` wont run on int
        Outpu: None, just put data in WC-DB
    """

    try:
        hn_scraper.run(ts)
        print("\n================ HH url scraper run: Complete ================n")
    except Exception as e:
        print(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in scraping HN for url xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\t>>> Error = {}".format(str(e)))
        pass

    try:
        r_scraper.run(ts)
        print(" \n================ Reddit url scraper run: Complete ================n")
    except Exception as e:
        print(" xxxxxxxxxxxxxxxxxxxxxxxxx Error in scraping Reddit for url xxxxxxxxxxxxxxxxxxxxxxxxx \n \t\tError = {}".format(str(e)))
        pass

    # try:
    #     ih_scraper.run()
    #     print(" \n====== IH url scraper run: Complete ======\n")
    # except Exception as e:
    #     print(" XXXXXXXXXXXX Error in scraping IH for url XXXXXXXXXXXXXXXXX \n \t\tError = {}".format(str(e)))
    #     pass

    # try:
    #     ph_scraper.run()
    #     print(" \n====== PH url scraper run: Complete ======\n")
    # except Exception as e:
    #     print(" XXXXXXXXXXXX Error in scraping PH for url XXXXXXXXXXXXXXXXX \n \t\tError = {}".format(str(e)))
    #     pass

    print(" ******************** All url scrapers ran successfully *****************\n")


