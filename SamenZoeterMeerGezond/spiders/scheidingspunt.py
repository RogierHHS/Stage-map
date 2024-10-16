import scrapy
from SamenZoeterMeerGezond.items import Scheidingspunt


class ScheidingspuntSpider(scrapy.Spider):
    name = "scheidingspunt"
    allowed_domains = ["www.scheidingspunt.nl"]
    start_urls = ["https://www.scheidingspunt.nl/home"]

    # Pagina-instelling voor JSON-export en het instellen van de MySQL pipeline
    custom_settings = {
        'FEEDS': {
            'scheidingspunt_aanbod.json': {
                'format': 'json',
                'overwrite': True,
            }
        },
        'ITEM_PIPELINES': {
            'SamenZoeterMeerGezond.pipelines.CleanDataPipeline': 300,
            'SamenZoeterMeerGezond.pipelines.MySQLPipeline': 400,
        },
        
    }

    def parse(self, response):
        # Selecteer alle activiteit-items in de lijst
        activities = response.css('div.k2ItemsBlock ul li')

        for activity in activities:
            activiteit_item = Scheidingspunt()

            # Scrape de titel en link van de activiteit
            activiteit_item['titel'] = activity.css('h3 a.moduleItemTitle::text').get(default='').strip()
            activiteit_item['link'] = response.urljoin(activity.css('h3 a.moduleItemTitle::attr(href)').get())

            # Scrape de beschrijving (Wat, Voor wie, Wanneer)
            beschrijving = activity.css('div.moduleItemIntrotext').get()

            # Extract de velden voor "Wat", "Voor wie" en "Wanneer"
            activiteit_item['wat'] = activity.css('div.moduleItemIntrotext p:contains("Wat")::text').get(default='').strip()
            activiteit_item['voor_wie'] = activity.css('div.moduleItemIntrotext p:contains("Voor wie")::text').get(default='').strip()
            activiteit_item['wanneer'] = activity.css('div.moduleItemIntrotext p:contains("Wanneer")::text').get(default='').strip()

            # Yield het item om op te slaan in de output (bijv. JSON of een database)
            yield activiteit_item

        # Ga naar de volgende pagina als er een "volgende pagina"-link is
        # next_page = response.css('a.next::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page, self.parse)