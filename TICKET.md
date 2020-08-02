# Overall Approach

- **Dictionary**(once): Prepare a curated list of Topics & their subtopics
- **Logic**(once): 
- **Scraping**(weekly) : Scrape content-websites(HN, reddit, twitter, PH, IH etc)
    - Do Keyword detection in scraped content: (topic/subtopic)–< nXn >–(content)
    - Tag each content with category(#1.News, #2.Product for now??)
    - Store the scraped content in DB against their (topic/subtopic)
    - After all the scraping is done; assign PopI to each topic & subtopic
    - Update DB with PopI column

- **Website/Newsletter**( once ):
    - Decide whether to keep newsletter of plain website
    - Create website (and if; newsletter system)