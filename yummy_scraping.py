import scrapy
import json
import re
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from scrapy.downloadermiddlewares.offsite import OffsiteMiddleware

class FlexibleOffsiteMiddleware(OffsiteMiddleware):
    """ Custom Middleware to handle URLs with ports """
    
    def should_follow(self, request, spider):
        if not self.host_regex:
            return True
        # Ensure we handle hostnames without the port number
        hostname = urlparse(request.url).hostname
        return bool(self.host_regex.search(hostname))

class ReconCrawler(scrapy.Spider):
    """ Main Spider class for web reconnaissance """
    
    name = 'recon_crawler'
    
    def __init__(self, start_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).hostname]
        self.crawled_data = {
            'emails': set(),
            'links': set(),
            'external_files': set(),
            'js_files': set(),
            'form_fields': set(),
            'images': set(),
            'videos': set(),
            'audio': set(),
            'comments': set(),
        }

    def parse(self, response):
        # Handle text-based responses only
        if "text" in response.headers.get('Content-Type', b'').decode():
            self.extract_data(response)
            self.crawl_links(response)

    def extract_data(self, response):
        """ Extract various elements from the response """
        # Find emails using regex
        self.crawled_data['emails'].update(
            re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
        )
        
        # Collect various types of assets and data
        self.crawled_data['js_files'].update(
            response.css('script::attr(src)').getall()
        )
        self.crawled_data['external_files'].update(
            response.css('link::attr(href), a::attr(href)').re(r'.*\.(css|pdf|docx?|xlsx?)$')
        )
        self.crawled_data['form_fields'].update(
            response.css('input::attr(name), textarea::attr(name), select::attr(name)').getall()
        )
        self.crawled_data['images'].update(
            response.css('img::attr(src)').getall()
        )
        self.crawled_data['videos'].update(
            response.css('video::attr(src), source::attr(src)').getall()
        )
        self.crawled_data['audio'].update(
            response.css('audio::attr(src), source::attr(src)').getall()
        )
        self.crawled_data['comments'].update(
            response.xpath('//comment()').getall()
        )
        
    def crawl_links(self, response):
        """ Identify links to follow and process recursively """
        for href in response.css('a::attr(href)').getall():
            # Skip email links
            if href.startswith('mailto:'):
                continue
            
            full_url = response.urljoin(href)
            parsed_url = urlparse(full_url)
            
            # Follow internal links only
            if parsed_url.hostname == urlparse(response.url).hostname:
                yield response.follow(full_url, self.parse)
            
            self.crawled_data['links'].add(full_url)

    def closed(self, reason):
        """ Handle post-crawl actions """
        for key in self.crawled_data:
            self.crawled_data[key] = list(self.crawled_data[key])
        
        # Save results as JSON
        with open('crawl_results.json', 'w') as file:
            json.dump(self.crawled_data, file, indent=4)
        
        self.log("Results saved to crawl_results.json")

def start_crawler(start_url):
    """ Entry point for starting the crawler """
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'INFO',
        'DOWNLOADER_MIDDLEWARES': {
            '__main__.FlexibleOffsiteMiddleware': 500,
        }
    })
    process.crawl(ReconCrawler, start_url=start_url)
    process.start()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Recon Crawler")
    parser.add_argument('start_url', help="URL to start the web crawling process")
    args = parser.parse_args()
    
    start_crawler(args.start_url)
