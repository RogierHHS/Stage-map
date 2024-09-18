import scrapy
from zoetermeerwijzer.items import ActiviteitenZTE


class ZTESpider(scrapy.Spider):
    name = "ZTE"
    allowed_domains = ["zoetermeertegeneenzaamheid.nl"]
    start_urls = ["https://zoetermeertegeneenzaamheid.nl/nieuws/?page=1"]

    # Pagina-instelling voor JSON-export
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
    }

    def parse(self, response):
        activiteiten = response.css('a.card')

        for activiteit in activiteiten:
            activiteit_zte = ActiviteitenZTE()
            activiteit_zte["Titel"] = activiteit.css("h3.card__title::text").get()
            activiteit_zte["Link"] = response.urljoin(activiteit.css("a::attr(href)").get())
            activiteit_zte["Datum_numeriek"] = activiteit.css('span.card__subhead::text').get().strip()
            
            #Ophalen van de image URL en samenvoegen met de source URL
            relative_image_url = activiteit.css('div.card__media picture img::attr(src)').get()
            activiteit_zte['Image_URL'] = response.urljoin(relative_image_url)

            # Volg de link naar de detailpagina voor meer informatie
            yield response.follow(activiteit_zte['Link'], callback=self.parse_details, meta={'activiteit_zte': activiteit_zte})
                
        # Paginering: Zoek de link naar de volgende pagina en volg deze
        next_page = response.css('a.pagination__control--next::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)

         

    # def parse_details(self, response):
    #     activiteit_zte = response.meta['activiteit_zte']
    #     activiteit_zte['Beschrijving'] = response.css('div.card__content p::text').getall().strip()
    #     yield activiteit_zte
