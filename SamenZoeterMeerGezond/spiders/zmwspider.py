import scrapy


class ZmwspiderSpider(scrapy.Spider):
    name = "zmwspider"
    allowed_domains = ["www.zoetermeerwijzer.nl"]
    start_urls = ["https://www.zoetermeerwijzer.nl/"]

    def parse(self, response):
        pass
