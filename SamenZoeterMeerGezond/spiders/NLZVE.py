import scrapy
from SamenZoeterMeerGezond.items import NLZVE

class NlzveSpider(scrapy.Spider):
    name = "NLZVE"
    allowed_domains = ["www.nlzve.nl"]
    start_urls = ["https://www.nlzve.nl/agenda/default.aspx"]

    custom_settings = {
        'FEEDS': {
            'JSON_bestanden/nederland_zorgt_agenda.json': {  
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
        # Loop door elke evenement-item
        for event in response.css('div.eventItem'):
            item = NLZVE()

            # Extract Titel
            title_tag = event.css('h2.itemTitle a.itemTitleLink')
            item['Titel'] = title_tag.css('::text').get().strip() if title_tag else ''

            # Extract Link met response.urljoin
            relative_link = title_tag.attrib.get('href') if title_tag else ''
            item['Link'] = response.urljoin(relative_link)

            # Extract Afbeelding_url met response.urljoin
            image_tag = event.css('div.itemImage img.image')
            relative_image_url = image_tag.attrib.get('src') if image_tag else ''
            item['Afbeelding_url'] = response.urljoin(relative_image_url)

            # Extract Beschrijving_kort
            beschrijving_paragraph = event.css('div.itemDescription p::text').get()
            item['Beschrijving_kort'] = beschrijving_paragraph.strip() if beschrijving_paragraph else 'Geen beschrijving gevonden'

            # Extract Locatie
            locatie = event.css('div.eventLocation::text').get()
            item['Locatie'] = locatie.strip() if locatie else 'Geen locatie gevonden'

        # Volg de link naar de detailpagina
            if item['Link']:
                yield response.follow(item['Link'], callback=self.parse_detail, meta={'item': item})

            
    def parse_detail(self, response):
        item = response.meta['item']

        # Extract Tijd_info
        tijd_info_text = response.css('div.eventInformation.eventStart span.icon-calendar.before::text').get()
        item['Begintijd'] = tijd_info_text.strip() if tijd_info_text else 'geen begintijd gevonden'

        # Extract Eindtijd
        eindtijd_text = response.css('div.eventInformation.eventEnd span.icon-calendar.before::text').get()
        item['Eindtijd'] = eindtijd_text.strip() if eindtijd_text else 'geen eindtijd gevonden'

        # Extract Beschrijving_lang uit zowel itemDescription als eventFullDescription
        beschrijving_kort_text = response.css('p.itemDescription span.BriefDescription::text').get()
        beschrijving_full_elements = response.css('div#ctl01_ctl02_ctl00_eventFullDescription').xpath('.//text()').getall()

        beschrijving_lang = ' '.join([
            text.strip() for text in [beschrijving_kort_text] + beschrijving_full_elements
            if text.strip()
        ])
        item['Beschrijving_lang'] = beschrijving_lang if beschrijving_lang else 'Geen uitgebreide beschrijving gevonden'

        yield item

        
            