import logging
import csv
import requests
import re
import queue
import threading
import time
from urllib.parse import urljoin 

class WebsiteCrawler(threading.Thread):
    def __init__(self, url, regex_pattern, output_csv):
        super().__init__()
        self.url = url
        self.regex_pattern = re.compile(regex_pattern)
        self.output_csv = output_csv
        self.queue = queue.Queue()
        self.visited_urls = set()  # Set to keep track of visited URLs
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.queue.put(self.url)
        self.visited_urls.add(self.url)

        while not self.queue.empty():
            current_url = self.queue.get()
            self.logger.info(f"Crawling: {current_url}")

            response = requests.get(current_url)

            if response.status_code == 200:
                # Get the contents of the page
                page_content = response.content.decode()

                # Find all matching regex patterns in the page content
                matches = self.regex_pattern.finditer(page_content)

                # Write the matches to the CSV file
                with open(self.output_csv, "a", newline="") as f:
                    writer = csv.writer(f)
                    for match in matches:
                        description = "Found on page: {}".format(current_url)
                        writer.writerow([match.group(), description])

                for link in re.findall(r'<a href="(.*?)">', response.content.decode()):
                    absolute_url = urljoin(current_url, link)  # Convert relative URL to absolute URL
                    if absolute_url not in self.visited_urls:
                        self.queue.put(absolute_url)
                        self.visited_urls.add(absolute_url)

            else:
                self.logger.error(f"Failed to crawl page: {current_url}")

        # Signal that the thread is done
        self.queue.task_done()

def main():
    # Create a list of website URLs
    website_urls = [
        "https://darknetlive.com/",
    ]

    # Create a regex pattern
    regex_pattern = re.compile(r'\b[a-z2-7]{16,56}\.(onion|i2p)\b')

    # Create a CSV file
    output_csv = "generalised_output.csv"

    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Create a thread pool
    thread_pool = []
    for website_url in website_urls:
        thread = WebsiteCrawler(website_url, regex_pattern, output_csv)
        thread_pool.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in thread_pool:
        thread.queue.join()

if __name__ == "__main__":
    main()
