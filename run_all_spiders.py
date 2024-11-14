import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

def run_all_spiders():
    # Initialiseer het Scrapy-proces met projectinstellingen
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    
    # Laad de spiders via SpiderLoader
    spider_loader = SpiderLoader.from_settings(settings)
    spider_names = spider_loader.list()
    
    # Loop door alle spiders en voer ze één voor één uit
    for spider_name in spider_names:
        print(f"Running spider: {spider_name}")
        process.crawl(spider_name)
    
    # Start het scraping-proces
    process.start()
    print("All spiders have been executed.")

if __name__ == "__main__":
    run_all_spiders()
