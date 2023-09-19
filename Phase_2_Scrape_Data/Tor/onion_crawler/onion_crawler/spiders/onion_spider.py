import scrapy
import time
import re

class OnionSpider(scrapy.Spider):
    name = "onion_spider"
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'output.csv',
    }
    
    def __init__(self, *args, **kwargs):
        super(OnionSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',')
        # Extract the domains from the start_urls
        self.allowed_domains = [re.sub(r'^https?://(www\.)?', '', url) for url in self.start_urls]
        # Updated regex pattern to match both old (16 characters) and new (56 characters) onion links
        self.onion_pattern = re.compile(r'\b[a-z2-7]{16,56}\.onion\b')
    
    def parse(self, response):
        # Extract and log onion links from the current page
        links = re.findall(self.onion_pattern, response.text)
        for link in links:
            self.log(f'Found onion link: {link} on {response.url}')
            yield {
                'onion_link': link,
                'source_url': response.url
            }
        
        # Follow links to the next pages
        # Only follow links that are on the allowed_domains
        next_links = response.css('a::attr(href)').getall()
        for next_link in next_links:
            if any(domain in next_link for domain in self.allowed_domains):
                self.log(f'Following link: {next_link}')
                # Add a delay of 1 second between API calls
                time.sleep(1)
                yield response.follow(next_link, self.parse)
