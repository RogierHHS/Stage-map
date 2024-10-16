import scrapy
from SamenZoeterMeerGezond.items import ActiviteitenUIT

class UITAgendaSpider(scrapy.Spider):
    name = "UIT"
    allowed_domains = ["uitagendazoetermeer.nl"]
    start_urls = ["https://www.uitagendazoetermeer.nl/uitagenda?calendar_range=&search=&sort=calendar&order=asc"]

    custom_settings = {
        'FEEDS': {
            'JSON_bestanden/activiteiten_UIT.json': {  # Geef hier de map aan
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
        activities = response.css('ul.tiles.tiles--doorway.tiles--small.list__overview li')

        for activity in activities:
            detail_url = activity.css('a.tile__link-overlay::attr(href)').get(default=None)
            if detail_url:
                detail_url = response.urljoin(detail_url)
                yield scrapy.Request(url=detail_url, callback=self.parse_details)
                
            #Paginering
            next_page = response.css('ul.pager li.pager__item--next a::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield response.follow(next_page_url, callback=self.parse)

    def parse_details(self, response):
        activiteit_uit = ActiviteitenUIT()

        # Titel ophalen
        activiteit_uit['Titel'] = response.css('h1.item__title::text').get(default=None)

        # Beschrijving ophalen (alle paragrafen samenvoegen)
        beschrijving_full = response.css('div.item-details__long-description__full p::text').getall()
        beschrijving_short = response.css('div.item-details__long-description__short p::text').getall()
        beschrijving = ' '.join(beschrijving_full).strip() if beschrijving_full else ' '.join(beschrijving_short).strip()

        # Verwijder \n en extra spaties in de spider
        beschrijving = ' '.join(beschrijving.split())  # Verwijder extra spaties en \n
        activiteit_uit['Beschrijving'] = beschrijving if beschrijving else None

        # Locatiegegevens
        locatie = response.css('address.odp-contact-information__address::text').getall()
        activiteit_uit['Naam'] = locatie[0].strip() if len(locatie) > 0 else None
        activiteit_uit['Straat'] = locatie[1].strip() if len(locatie) > 1 else None
        activiteit_uit['Postcode'] = locatie[2].strip() if len(locatie) > 2 else None

        # Email en bedrijfswebsite
        email = response.css('li.contact-options__option--email a::attr(href)').get()
        if email and email.startswith('mailto:'):
            activiteit_uit['Email'] = email.replace('mailto:', '')
        else:
            activiteit_uit['Email'] = None

        activiteit_uit['Bedrijf_Website'] = response.css('li.contact-options__option--url a::attr(href)').get()

        # Datum, start- en eindtijd
        activiteit_uit['Datum'] = response.css('span.calendar__date::text').get()
        tijd = response.css('span.calendar__time::text').get()

        if tijd:
            tijden = tijd.split(' - ')
            starttijd = tijden[0].strip()
            eindtijd = tijden[1].strip() if len(tijden) > 1 else None
            activiteit_uit['Starttijd'] = starttijd
            activiteit_uit['Eindtijd'] = eindtijd
        else:
            activiteit_uit['Starttijd'] = None
            activiteit_uit['Eindtijd'] = None

        # Prijs ophalen
        activiteit_uit['Prijs'] = response.css('ul.feature-item__prices-wrapper li.feature-item__price span.feature-item__price-value::text').get(default=None)
        if activiteit_uit['Prijs']:
            activiteit_uit['Prijs'] = activiteit_uit['Prijs'].strip()

        # Url van plaatje
        activiteit_uit['Url_plaatje'] = response.css('picture img::attr(src)').get(default=None)

        # Het item teruggeven aan de pipeline
        yield activiteit_uit
