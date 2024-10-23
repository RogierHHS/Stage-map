import scrapy
from SamenZoeterMeerGezond.items import Evie

class EvieNlSpider(scrapy.Spider):
    name = "evie"
    allowed_domains = ["evie.nl"]
    start_urls = ["https://evie.nl/resultaten/"]

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
        # Loop through each activity
        for activity in response.css('a.group'):
            evie = Evie()

            # Extract basic fields
            evie['Titel'] = activity.css('h3::text').get()
            evie['Categorieën'] = activity.css('div.flex.items-center.gap-2 span::text').getall()
            evie['Link'] = activity.css('a::attr(href)').get()
            evie['Afbeelding_url'] = activity.css('img::attr(src)').get()

            # Follow the link to the detail page
            if evie['Link']:
                yield response.follow(evie["Link"], callback=self.parse_detail, meta={'evie': evie})

       

    def parse_detail(self, response):
        evie = response.meta['evie']

        # Scrape the description (including p, li, strong, etc.)
        description_parts = response.css('div#rspeak_read_3647 *::text').getall()
        if description_parts:
            description = ' '.join([part.strip() for part in description_parts if part.strip()])
            evie['Beschrijving'] = description
        else:
            evie['Beschrijving'] = 'Geen beschrijving gevonden'

        # Scrape the "Meer over de app" link (found within a specific button class)
        more_info_link = response.css('a.breakdance-link.button-atom::attr(href)').get()
        evie['Link_naar_meer_info'] = more_info_link

        # Scrape the text on the button (e.g., 'Meer over de app')
        button_text = response.css('a.breakdance-link span.button-atom__text::text').get()
        evie['Tekst_knop'] = button_text

        # Yield the populated item
        yield evie
