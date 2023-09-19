pip install scrapy

scrapy startproject onion_crawler
cd onion_crawler

scrapy genspider onion_spider myspider.com

-----------

To run crawler:

scrapy crawl onion_spider -a start_urls=https://thehiddenwiki.org,https://oniondir.biz


------------

to run onion_scraper

brew install tor

Start the Tor service. On macOS and Linux, you can use tor & to start it in the background.


In the end
pkill tor



