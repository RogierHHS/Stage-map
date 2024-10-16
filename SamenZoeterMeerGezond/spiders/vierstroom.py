import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from scrapy.selector import Selector
from SamenZoeterMeerGezond.items import Vierstroom  

class vierstroom(scrapy.Spider):
    name = "vierstroom"
    allowed_domains = ["vierstroom.nl"]
    start_urls = ["https://www.vierstroom.nl/nieuws"]

    custom_settings = {
        'FEEDS': {
            'JSON_bestanden/Vierstroom_nieuws.json': {  # Geef hier de map aan
                'format': 'json',
                'overwrite': True,
            }
        },
        'ITEM_PIPELINES': {
            'SamenZoeterMeerGezond.pipelines.CleanDataPipeline': 300,
            'SamenZoeterMeerGezond.pipelines.MySQLPipeline': 400,
        }
}

    def __init__(self):
        # Initialiseer de WebDriver met Selenium Manager
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # Draai Chrome in headless modus (zonder GUI)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Gebruik Selenium Manager door geen pad op te geven
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(3)  # Wacht tot de pagina volledig laadt

        # Scroll tot het einde van de pagina
        prev_height = self.driver.execute_script("return document.body.scrollHeight")
        max_scrolls = 100
        scroll_count = 0

        while scroll_count < max_scrolls:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wacht tot nieuwe inhoud laadt

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break
            prev_height = new_height
            scroll_count += 1

        # Verkrijg de pagina bron na het scrollen
        html = self.driver.page_source
        sel = Selector(text=html)

        # Selecteer alle grid-item divs
        grid_items = sel.css('div.grid-item.w-100')

        for item in grid_items:
            nieuws_item = Vierstroom()
            # Titel
            nieuws_item['titel'] = item.css('h2.color-pink.mb-0::text').get(default='').strip()
            # URL van de header image
            nieuws_item['image_url'] = item.css('img.image__fluid.tile__image-fullwidth::attr(src)').get(default='')
            # Link naar het volledige artikel
            nieuws_item['link'] = item.css('a.btn-solid--primary::attr(href)').get(default='')
            # Korte beschrijving
            description = item.css('div.card-bullet-list.card-bullet-list--pink::text').getall()
            nieuws_item['beschrijving_kort'] = ' '.join([desc.strip() for desc in description]).strip()
            # Categorie van het nieuws
            nieuws_item['categorie'] = item.css('div.tile__icon div.leaf::text').get(default='').strip()

            # Bezoek de detailpagina en verzamel de tekst
            if nieuws_item["link"]:
                # Gebruik response.follow om de link te volgen
                yield response.follow(
                    url=nieuws_item["link"],
                    callback=self.parse_detail,
                    meta={'item': nieuws_item} )
            else:
                yield nieuws_item  # Yield het item zonder detailinformatie

        # Sluit de WebDriver
        self.driver.quit()

    def parse_detail(self, response):
        nieuws_item = response.meta['item']

        # Selecteer alle gewenste elementen in de juiste volgorde
        elements = response.xpath('//div[@class="card-bullet-list card-bullet-list--pink text-color info-page__content"]//h2 | //div[@class="card-bullet-list card-bullet-list--pink text-color info-page__content"]//p | //div[@class="card-bullet-list card-bullet-list--pink text-color info-page__content"]//em')

        combined_text = []

        # Doorloop elk geselecteerd element en haal de tekst op
        for element in elements:
            if element.root.tag == 'h2':
                # Als het element een <h2> is, haal de tekst op
                combined_text.append(element.css('::text').get())
            elif element.root.tag == 'p':
                # Als het element een <p> is, haal de tekst op
                combined_text.append(element.css('::text').get())
            elif element.root.tag == 'em':
                # Als het element een <em> is, haal de tekst op
                combined_text.append(element.css('::text').get())

        # Combineer alle tekst in één string, gescheiden door nieuwe regels
        full_text = " ".join(combined_text)
        nieuws_item['Beschrijving_lang'] = full_text
          
        yield nieuws_item
            
