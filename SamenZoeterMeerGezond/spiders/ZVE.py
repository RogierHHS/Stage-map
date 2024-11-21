import scrapy
from SamenZoeterMeerGezond.items import WorkshopsZVE  # Zorg ervoor dat het pad klopt

class ZveSpider(scrapy.Spider):
    name = "ZVE"
    allowed_domains = ["zoetermeervoorelkaar.nl"]
    start_urls = ["https://www.zoetermeervoorelkaar.nl/cursusaanbod/"]

    # Pagina-instelling voor JSON-export en het instellen van de MySQL pipeline
    custom_settings = {
        'FEEDS': {
            'JSON_bestanden/ZVE_workshops.json': {  # Geef hier de map aan
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
        workshops = response.css('article.c-card.c-card--seminar.js-card')

        for workshop in workshops:
            ZVE = WorkshopsZVE()
            ZVE['Titel'] = workshop.css('div.c-card__body a.c-card__title-link h2.c-card__title::text').get().strip()
            ZVE['Organisatie'] = workshop.css('div.c-card__body span.c-card__profile-text::text').get().strip()
            ZVE['Beschrijving_kort'] = workshop.css('div.c-card__body p.c-card__description::text').get().strip()
            datum_list = workshop.css('div.c-card__footer ul.c-card__tags li.c-card__tag::text').getall()
            ZVE['Datum'] = datum_list[-1] if datum_list else None

            # Ophalen van de relatieve link naar de detailpagina
            relative_link = workshop.css('div.c-card__body a.c-card__title-link::attr(href)').get()
            link_workshop = response.urljoin(relative_link)
            ZVE['Link_workshop'] = link_workshop

            # Ophalen van de afbeeldings-URL
            ZVE['Image_url'] = workshop.css('div.c-card__header picture.c-card__background img.c-card__background-image::attr(src)').get()

            # Maak een request naar de detailpagina en stuur het item door via meta
            yield response.follow(
                relative_link,
                callback=self.parse_detail,
                meta={'ZVE': ZVE}
            )

    def parse_detail(self, response):
        ZVE = response.meta['ZVE']
        
        # Extraheer de volledige beschrijving
        beschrijving_lang_list = response.css(
            'div.grid__cell.unit-9-12.unit-1-1--lap-portrait.unit-1-1--palm-landscape.link--underlined p::text'
        ).getall()
        beschrijving_lang = ' '.join(text.strip() for text in beschrijving_lang_list if text.strip())
        ZVE['Beschrijving_lang'] = beschrijving_lang



        # Extraheer extra variabelen uit de <dl> elementen
        dl_elements = response.css('dl.list__definition.list__definition--horizontal.list-definition--small')
    

        for dl in dl_elements:
            dt_texts = dl.css('dt::text').getall()
            dd_texts = dl.css('dd::text').getall()
            

            for dt, dd in zip(dt_texts, dd_texts):
                key = dt.strip().rstrip(':')  
                value = dd.strip()

                if key == 'Aantal bijeenkomsten':
                    ZVE['Aantal_bijeenkomsten'] = value
                elif key == 'Eerste bijeenkomst':
                    ZVE['Eerste_bijeenkomst'] = value
                elif key == 'Laatste bijeenkomst':
                    ZVE['Laatste_bijeenkomst'] = value
                elif key == 'Inschrijven kan tot':
                    ZVE['Inschrijven_kan_tot'] = value
                elif key == 'Datum bijeenkomst':
                    ZVE['Datum_bijeenkomst'] = value

        # Zorg ervoor dat ontbrekende velden op None staan
        ZVE.setdefault('Aantal_bijeenkomsten', None)
        ZVE.setdefault('Eerste_bijeenkomst', None)
        ZVE.setdefault('Laatste_bijeenkomst', None)
        ZVE.setdefault('Inschrijven_kan_tot', None)
        ZVE.setdefault('Datum_bijeenkomst', None)

        yield ZVE

