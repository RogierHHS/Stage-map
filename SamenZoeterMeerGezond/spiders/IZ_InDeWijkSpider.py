import scrapy
from SamenZoeterMeerGezond.items import ActiviteitenIZ

class IzIndewijkspiderSpider(scrapy.Spider):
    name = "IZ-InDeWijkSpider"
    allowed_domains = ["www.inzet-indewijk.nl"]
    start_urls = ["https://www.inzet-indewijk.nl/evenementen/"]
    
    # Exporteren naar JSON en instellen van throttling parameters
    custom_settings = {
        'FEEDS': {
            'activiteiten_iz.json': {
                'format': 'json',
                'overwrite': True,
            }
        },
        'ITEM_PIPELINES': {
            'zoetermeerwijzer.pipelines.CleanDataPipeline': 300,
            'zoetermeerwijzer.pipelines.MySQLPipeline': 400,
        }
    }
    
    def parse(self, response):
        activiteiten = response.css('li.UniversalListItem_item__lLGLO')

        # Loop door alle activiteiten op de huidige pagina
        for activiteit in activiteiten:
            # Maak een nieuw ActiviteitenIZ item aan voor elke activiteit
            activiteit_iz = ActiviteitenIZ()
            
            # Vul het activiteit_iz item met de gescrapede basisinformatie
            activiteit_iz['Titel'] = activiteit.css("a::text").get()
            activiteit_iz['Link'] = response.urljoin(activiteit.css("a::attr(href)").get())
            activiteit_iz['Datum_numeriek'] = activiteit.css('div.UniversalListItem_eventInformation__TKRxt time::attr(datetime)').get()
            activiteit_iz['Datum_text'] = activiteit.css('div.UniversalListItem_eventInformation__TKRxt time::text').get()
            activiteit_iz['Beschrijving'] = activiteit.css('div.UniversalListItem_teaser__mhBWx p::text').get()
            activiteit_iz['Starttijd'] = activiteit.css('div.UniversalListItem_eventInformation__TKRxt time::text').getall()[1] if len(activiteit.css('div.UniversalListItem_eventInformation__TKRxt time::text').getall()) > 1 else None
            activiteit_iz['Eindtijd'] = activiteit.css('div.UniversalListItem_eventInformation__TKRxt time::text').getall()[2] if len(activiteit.css('div.UniversalListItem_eventInformation__TKRxt time::text').getall()) > 2 else None
            activiteit_iz['Locatie'] = activiteit.css('span.UniversalListItem_eventInformationText__1QKSF::text').get()
            activiteit_iz['URL_afbeelding'] = activiteit.css('div.UniversalListItem_imageContainer__TBU3s img::attr(src)').get() or "Geen afbeelding"

            # Volg de link naar de detailpagina voor aanvullende informatie per activiteit
            yield response.follow(activiteit_iz['Link'], callback=self.parse_details, meta={'activiteit_iz': activiteit_iz})

        # Paginering: Vind de link naar de volgende pagina en volg deze
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.log(f'Volgende pagina: {next_page_url}')  # Log de volgende pagina-URL
            yield response.follow(next_page_url, callback=self.parse)

    def parse_details(self, response):
        # Haal het activiteit_iz item op dat is doorgegeven via meta
        activiteit_iz = response.meta['activiteit_iz']

        # Combineer alle tekst uit de relevante divs met p-, h4-, en strong-tags
        extra_beschrijving = response.css('div.ContentDetailsContainer_introBorder__onvXD p, div.ContentDetailsContainer_introBorder__onvXD h4, div.ContentDetailsContainer_introBorder__onvXD strong::text').getall()
    
        # Voeg extra tekst uit eventuele andere content containers (zoals de vorige div-selectors)
        extra_beschrijving += response.css('div.text-container p, div.text-container h4, div.text-container strong::text').getall()

        # Nog bredere fallback met een XPath-selector die op zoek gaat naar alle tekst in de <div> met class 'content'
        if not extra_beschrijving:
            extra_beschrijving = response.xpath('//div[contains(@class, "content")]//p//text()').getall()

        # Combineer de teksten, zelfs als ze langer zijn, en verwijder extra witruimtes
        volledige_beschrijving = ' '.join(extra_beschrijving).strip()

        # Voeg de extra beschrijving toe aan het activiteit_iz item
        activiteit_iz['Extra_beschrijving'] = volledige_beschrijving

        # Yield het volledige activiteit_iz item
        yield activiteit_iz




