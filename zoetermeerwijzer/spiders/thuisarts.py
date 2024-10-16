import scrapy
from zoetermeerwijzer.items import Thuisarts 

class ThuisartsSpider(scrapy.Spider):
    name = "thuisarts"
    allowed_domains = ["thuisarts.nl"]
    start_urls = ["https://www.thuisarts.nl/overzicht/onderwerpen"]

    # Pagina-instelling voor JSON-export en het instellen van de MySQL pipeline
    custom_settings = {
        'FEEDS': {
            'Thuisarts_onderwerpen.json': {
                'format': 'json',
                'overwrite': True,
            }
        },
        # 'DOWNLOAD_DELAY': 2,  # Voorkom overbelasting van de server
        # 'AUTOTHROTTLE_ENABLED': True,
        # 'AUTOTHROTTLE_START_DELAY': 1,
        # 'AUTOTHROTTLE_MAX_DELAY': 10,
        'ITEM_PIPELINES': {
            'zoetermeerwijzer.pipelines.CleanDataPipeline': 300,  # Pipeline voor data schoonmaak
            'zoetermeerwijzer.pipelines.MySQLPipeline': 400,  # Pipeline voor MySQL-opslag
        }
    }

    def parse(self, response):
        subject_lists = response.css('ul.subject-list')

        for subject_list in subject_lists:
            onderwerpen = subject_list.css('li a')
            for onderwerp in onderwerpen:
                onderwerp_naam = onderwerp.css('::text').get()
                relatieve_link = onderwerp.css('::attr(href)').get()
                volledige_link = response.urljoin(relatieve_link)

                # Schedule een request naar de detailpagina
                yield scrapy.Request(
                    url=volledige_link,
                    callback=self.parse_detail,
                    meta={'Onderwerp': onderwerp_naam, 'Link_onderwerp': volledige_link}
                )

    def parse_detail(self, response):
        onderwerp = response.meta['Onderwerp']
        link_onderwerp = response.meta['Link_onderwerp']

        # Haal de samenvatting op
        samenvatting_items = response.css('div.subject-summary ul li::text').getall()
        if samenvatting_items:
            samenvatting = ' '.join(samenvatting_items)
        else:
            samenvatting = 'Geen samenvatting beschikbaar'

        # Haal de situaties op
        situation_links = response.css('div.field--name-field-pg-situation div.field__item a')
        situaties = []

        for situation_link in situation_links:
            titel = situation_link.css('span::text').get()
            relatieve_link = situation_link.css('::attr(href)').get()
            volledige_link = response.urljoin(relatieve_link)
            situaties.append({
                'Titel': titel,
                'Link': volledige_link
            })

        # Maak het item aan
        thuisarts = Thuisarts()
        thuisarts['Onderwerp'] = onderwerp
        thuisarts['Link_onderwerp'] = link_onderwerp
        thuisarts['Samenvatting'] = samenvatting
        thuisarts['Situaties'] = situaties

        yield thuisarts
