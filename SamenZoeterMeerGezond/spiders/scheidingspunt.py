import scrapy
from SamenZoeterMeerGezond.items import Scheidingspunt


class ScheidingspuntSpider(scrapy.Spider):
    name = "scheidingspunt"
    allowed_domains = ["www.scheidingspunt.nl"]
    start_urls = ["https://www.scheidingspunt.nl/home"]

    # Pagina-instelling voor JSON-export en het instellen van de MySQL pipeline
    custom_settings = {
        'FEEDS': {
            'JSON_bestanden/Scheidingspunt.json': { 
                'format': 'json',
                'overwrite': True,
            }
        },
        'ITEM_PIPELINES': {
            'SamenZoeterMeerGezond.pipelines.CleanDataPipeline': 300,
            'SamenZoeterMeerGezond.pipelines.MySQLPipeline': 400,
        }
}

    def parse(self, response):
        # Selecteer alle activiteit-items in de lijst
        activities = response.css('div.k2ItemsBlock ul li')

        for activity in activities:
            activiteit_item = Scheidingspunt()

            # Scrape de titel en link van de activiteit
            activiteit_item['Titel'] = activity.css('h3 a.moduleItemTitle::text').get(default='').strip()
            activiteit_item['Link'] = response.urljoin(activity.css('h3 a.moduleItemTitle::attr(href)').get())

            # Scrape de beschrijving (Wat, Voor wie, Wanneer)
            beschrijving = activity.css('div.moduleItemIntrotext').get()

            # Extract de velden voor "Wat", "Voor wie" en "Wanneer"
            activiteit_item['Wat'] = activity.css('div.moduleItemIntrotext p:contains("Wat")::text').get(default='').strip()
            activiteit_item['Voor_wie'] = activity.css('div.moduleItemIntrotext p:contains("Voor wie")::text').get(default='').strip()
            activiteit_item['Wanneer'] = activity.css('div.moduleItemIntrotext p:contains("Wanneer")::text').get(default='').strip()

            # Yield het item om op te slaan in de output (bijv. JSON of een database)
            yield activiteit_item

       