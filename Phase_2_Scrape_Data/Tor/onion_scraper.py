import scrapy
import csv
from scrapy.crawler import CrawlerProcess
import logging

class OnionSpider(scrapy.Spider):
    name = "onion_spider"
    
    # Set custom settings
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': logging.INFO,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
        },
        'FEEDS': {
            'scraped_data.json': {
                'format': 'json',
                'overwrite': True
            },
            'captcha_or_signup.csv': {
                'format': 'csv',
                'overwrite': True
            }
        },
        'http_proxy': 'http://127.0.0.1:9050',  # Using Tor as a proxy
        'https_proxy': 'http://127.0.0.1:9050'  # Using Tor as a proxy
    }

    
    # def start_requests(self):
    #     # Read the onion links from the CSV file
    #     with open('merged_onion_links.csv', newline='') as file:
    #         start_urls = [("http://" + row[0]) if not row[0].startswith("http://") else row[0] for row in csv.reader(file)]
    #         for url in start_urls:
    #             yield scrapy.Request(url=url, callback=self.parse, errback=self.handle_error)
    def start_requests(self):
    # Read the onion links from the CSV file
        with open('merged_onion_links.csv', newline='') as file:
            start_urls = [("https://" + row[0]) if not row[0].startswith("http://") and not row[0].startswith("https://") else row[0] for row in csv.reader(file)]
            for url in start_urls:
                yield scrapy.Request(url=url, callback=self.parse, errback=self.handle_error)


    def parse(self, response):
        # If the page contains a captcha or requires sign-up
        if "captcha" in response.text.lower() or "sign up" in response.text.lower():
            yield {'onion_link': response.url, 'comment': 'captcha or sign up'}
            return

        # Scrape the text content of the page
        text_content = response.xpath("//text()").getall()
        text_content = ' '.join(text_content)
        
        # Yield the scraped text content
        yield {'onion_link': response.url, 'text_content': text_content}

        # Follow links to next pages
        next_pages = response.css('a::attr(href)').getall()
        for next_page in next_pages:
            if next_page.startswith("/"):
                next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse, errback=self.handle_error)

    def handle_error(self, failure):
        # Log errors
        self.log(f'Error occurred: {failure}')

if __name__ == "__main__":
    # Create a CrawlerProcess with custom settings
    process = CrawlerProcess({
        'http_proxy': 'http://127.0.0.1:9050',  # Using Tor as a proxy
        'https_proxy': 'http://127.0.0.1:9050'  # Using Tor as a proxy
    })
    
    # Startthe spider
    process.crawl(OnionSpider)
    process.start()
