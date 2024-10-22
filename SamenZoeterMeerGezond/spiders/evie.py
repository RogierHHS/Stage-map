import scrapy
from SamenZoeterMeerGezond.items import Evie

class EvieNlSpider(scrapy.Spider):
    name = "evie"
    allowed_domains = ["evie.nl"]
    start_urls = ["https://evie.nl/resultaten/"]

    # Pagina-instelling voor JSON-export en het instellen van de MySQL pipeline
    custom_settings = {
        'FEEDS': {
            'JSON_bestanden/evie.json': {  
                'format': 'json',
                'overwrite': True,
            }
        },
        'ITEM_PIPELINES': {
            # 'SamenZoeterMeerGezond.pipelines.CleanDataPipeline': 300,
            # 'SamenZoeterMeerGezond.pipelines.MySQLPipeline': 400,
        }
    }

    def parse(self, response):
        # Select all the cards in the grid
        for activity in response.css('a.group'):
            evie = Evie()

            # Extract the fields and assign them to the item
            evie['titel'] = activity.css('h3::text').get()
            evie['categorieen'] = activity.css('div.flex.items-center.gap-2 span::text').getall()
            evie['link'] = activity.css('a::attr(href)').get()
            evie['afbeelding_url'] = activity.css('img::attr(src)').get()

            
            # Yield the populated item
            yield evie

        # Pagination (if needed)
        # next_page = response.css('a.next::attr(href)').get()
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)
