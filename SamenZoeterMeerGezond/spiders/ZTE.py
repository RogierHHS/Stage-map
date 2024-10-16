import scrapy
from datetime import datetime
from SamenZoeterMeerGezond.items import ActiviteitenZTE

class ZTESpider(scrapy.Spider):
    name = "ZTE"
    allowed_domains = ["zoetermeertegeneenzaamheid.nl"]
    start_urls = ["https://zoetermeertegeneenzaamheid.nl/nieuws/?page=1"]

    # Pagina-instelling voor JSON-export en het instellen van de MySQL pipeline
    custom_settings = {
        'FEEDS': {
            'activiteiten_zte.json': {
                'format': 'json',
                'overwrite': True,
            }
        },
        'DOWNLOAD_DELAY': 2,  # Voorkom overbelasting van de server
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'ITEM_PIPELINES': {
            'zoetermeerwijzer.pipelines.CleanDataPipeline': 300,  # Pipeline voor data schoonmaak
            'zoetermeerwijzer.pipelines.MySQLPipeline': 400,  # Pipeline voor MySQL-opslag
        }
    }

    def parse(self, response):
        activiteiten = response.css('a.card')

        for activiteit in activiteiten:
            activiteit_zte = ActiviteitenZTE()
            activiteit_zte["Titel"] = activiteit.css("h3.card__title::text").get()
            activiteit_zte["Link"] = response.urljoin(activiteit.css("a::attr(href)").get())

                 # Datum_numeriek ophalen en omzetten naar YYYY-MM-DD formaat
            datum_numeriek = activiteit.css('span.card__subhead::text').get().strip()
            try:
                activiteit_zte["Datum_numeriek"] = datetime.strptime(datum_numeriek, '%d-%m-%Y').strftime('%Y-%m-%d')
            except ValueError:
                self.logger.error(f"Incorrect date format for {datum_numeriek}")
                activiteit_zte["Datum_numeriek"] = None
            
            # Ophalen van de image URL en samenvoegen met de source URL voor de header afbeelding
            relative_image_url = activiteit.css('div.card__media picture img::attr(src)').get()
            activiteit_zte['Url_header_afbeelding'] = response.urljoin(relative_image_url)

            # Volg de link naar de detailpagina voor meer informatie
            yield response.follow(activiteit_zte['Link'], callback=self.parse_details, meta={'activiteit_zte': activiteit_zte})
                
        # Paginering: Zoek de link naar de volgende pagina en volg deze
        next_page = response.css('a.pagination__control--next::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)

         
    def parse_details(self, response):
        activiteit_zte = response.meta['activiteit_zte']

        # Haal alle tekst binnen de div.plugin-text op, inclusief de <p>- en <strong>-tags
        content_blocks = response.css('div.plugin-text *::text').getall()

        # Combineer de tekst in één string en verwijder overtollige witruimtes
        activiteit_zte['Beschrijving'] = ' '.join(content_blocks).strip()

        activiteit_zte['Datum_text'] = response.css('p.text-center.news-detail__subtitle time::text').get().strip()

        # Afbeelding ophalen als die bestaat
        image_url = response.css('div.block__inner img::attr(src)').get()
        if image_url:
            activiteit_zte['Url_afbeelding'] = response.urljoin(image_url)
        else:
            activiteit_zte['Url_afbeelding'] = None  # Geen afbeelding aanwezig

        # Yield het activiteit object met de beschrijving en eventuele afbeelding
        yield activiteit_zte

