import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pydispatch import dispatcher
from scrapy import signals
from SamenZoeterMeerGezond.items import ActiviteitenZMA
import time

class ZMASpider(scrapy.Spider):
    name = "ZMA"
    allowed_domains = ["zoetermeeractief.nl"]
    start_urls = ["https://zoetermeeractief.nl/agenda/complete-agenda"]

    # Pagina-instelling voor JSON-export en het instellen van de MySQL pipeline
    custom_settings = {
        'FEEDS': {
            'activiteiten_zma.json': {
                'format': 'json',
                'overwrite': True,
            }
        },
        # 'DOWNLOAD_DELAY': 2,  # Voorkom overbelasting van de server
        # 'AUTOTHROTTLE_ENABLED': True,
        # 'AUTOTHROTTLE_START_DELAY': 1,
        # 'AUTOTHROTTLE_MAX_DELAY': 10,
        'ITEM_PIPELINES': {
            'SamenZoeterMeerGezond.pipelines.CleanDataPipeline': 300,  # Pipeline voor data schoonmaak
            'SamenZoeterMeerGezond.pipelines.MySQLPipeline': 400,  # Pipeline voor MySQL-opslag
        }
    }


    def __init__(self, *args, **kwargs):
        super(ZMASpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Zorg dat Chrome headless draait
        self.driver = webdriver.Chrome(options=chrome_options)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # Sluit de webdriver af na het sluiten van de spider
        self.driver.quit()

    def parse(self, response):
        self.driver.get(response.url)

        # Ga door met het klikken op de 'Laad meer'-knop tot er geen meer is
        while True:
            try:
                # Wacht tot de 'Laad meer'-knop geladen is
                load_more_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "rsepro_loadmore"))
                )
                
                # Scroll naar de knop
                self.driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                time.sleep(1)  # Wacht even

                # Klik op de knop
                load_more_button.click()
                self.logger.info("Laad meer-knop geklikt, wacht op nieuwe content...")

                # Wacht tot er nieuwe activiteiten worden toegevoegd in de container
                WebDriverWait(self.driver, 10).until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, 'ul#rs_events_container li.rs_event_detail')) > len(response.css('ul#rs_events_container li.rs_event_detail'))
                )
                time.sleep(2)  # Wacht extra om zeker te zijn dat alles geladen is
            except Exception as e:
                # Als de knop niet gevonden wordt, of er is een probleem, log en breek de lus
                self.logger.info(f"Geen 'Laad meer'-knop meer beschikbaar of alle content is geladen. Fout: {e}")
                break

        # Nu alle activiteiten geladen zijn, verzamel de broncode
        page_source = self.driver.page_source
        response = scrapy.http.HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')

        # Gebruik Scrapy om de pagina te parsen
        activiteiten = response.css('ul#rs_events_container li.rs_event_detail')

        for activiteit in activiteiten:
            activiteit_zma = ActiviteitenZMA()
            activiteit_zma['Titel'] = activiteit.css('div.rs_event_details a.rs_event_link::text').get()
            activiteit_zma['Link'] = response.urljoin(activiteit.css('div.rs_event_details a.rs_event_link::attr(href)').get())
            activiteit_zma['Beschrijving'] = activiteit.css('div.eventDescription::text').get()
            activiteit_zma['Startdatum'] = activiteit.css('span.rsepro-event-starting-block b::text').get()

            categorieen = activiteit.css('span.rsepro-event-categories-block a::text').getall()
            categorieen = categorieen + [None] * (4 - len(categorieen))
            categorieen = categorieen[:4]
            activiteit_zma['Categorie_1'], activiteit_zma['Categorie_2'], activiteit_zma['Categorie_3'], activiteit_zma['Categorie_4'] = categorieen

            activiteit_zma['Url_header_afbeelding'] = response.urljoin(activiteit.css('div.rs_event_image img::attr(src)').get())

            yield response.follow(activiteit_zma['Link'], callback=self.parse_details, meta={'activiteit_zma': activiteit_zma})

    def parse_details(self, response):
        activiteit_zma = response.meta['activiteit_zma']

        extra_beschrijving = response.css('span.description p, span.description strong::text').getall()
        volledige_beschrijving = ' '.join(extra_beschrijving).strip()

        activiteit_zma['Extra_beschrijving'] = volledige_beschrijving

        img_src = response.css('span.description img::attr(src)').get()
        if img_src:
            activiteit_zma['Url_afbeelding'] = response.urljoin(img_src)
        else:
            self.logger.warning(f"Geen afbeelding gevonden voor {activiteit_zma['Titel']} op {activiteit_zma['Link']}")
            activiteit_zma['Url_afbeelding'] = None

        yield activiteit_zma
