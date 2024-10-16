import scrapy
from SamenZoeterMeerGezond.items import AppsGGD
import re


class GgdAppSpider(scrapy.Spider):
    name = "GGD_APP"
    allowed_domains = ["ggdappstore.nl"]
    start_urls = ["https://ggdappstore.nl/Appstore/Homepage/Sessie,Medewerker,Button"]

    # Pagina-instelling voor JSON-export en het instellen van de MySQL pipeline
    custom_settings = {
        'FEEDS': {
            'App_Data_GGD.json': {
                'format': 'json',
                'overwrite': True,
            }
        },
        'ITEM_PIPELINES': {
            'zoetermeerwijzer.pipelines.CleanDataPipeline': 300,
            'zoetermeerwijzer.pipelines.MySQLPipeline': 400,
        },
        
    }

    def parse(self, response):
        app_category = response.css('div#header-categorien a::attr(href)').getall()

        for category in app_category:
            # Dit verwijdert de spaties die in de link zitten, zonder dit krijg je een andere link
            volledige_link = response.urljoin(category).strip().replace(" ", "")
            yield response.follow(volledige_link, callback=self.parse_category)

    def parse_category(self, response):
        apps = response.css('div#apps div.col-xs-12.col-sm-6.col-md-4.app')

        for app in apps:
            # Linken met de aangemaakte .items()
            Apps_GGD = AppsGGD()

            # De naam van de app en de korte beschrijving
            Apps_GGD["App_naam"] = app.css('div.app-container h3::text').get()
            Apps_GGD["Beschrijving_kort"] = app.css('div.app-description-short::text').get()

            # Bepalen van de categorieën, controleer per categorie-icoon
            categories = app.css('div.app-element.app-category span.cat-icon')
            Apps_GGD["Lichaamsfuncties"] = 1 if categories.css('.cat-lichaam') else 0
            Apps_GGD["Dagelijks_Functioneren"] = 1 if categories.css('.cat-dagelijksleven') else 0
            Apps_GGD["Mentaal_Welbevinden"] = 1 if categories.css('.cat-psyche') else 0
            Apps_GGD["Kwaliteit_van_Leven"] = 1 if categories.css('.cat-geluk') else 0
            Apps_GGD["Zingeving"] = 1 if categories.css('.cat-zingeving') else 0
            Apps_GGD["Meedoen"] = 1 if categories.css('.cat-relaties') else 0

            # Sterrenrating: Tel het aantal volledige en halve sterren
            full_stars = len(app.css('div.app-element.app-score i.fa-star'))
            half_stars = len(app.css('div.app-element.app-score i.fa-star-half-o'))
            star_count = full_stars + 0.5 * half_stars
            Apps_GGD["App_rating"] = star_count

            # Platform links: Android, iOS, Desktop
            Apps_GGD["Android_link"] = app.css('a.platform-android::attr(href)').get() or None
            Apps_GGD["iOS_link"] = app.css('a.platform-ios::attr(href)').get() or None
            Apps_GGD["Desktop_link"] = app.css('a.platform-internet::attr(href)').get() or None

            # # Base64-code van app-icoon ophalen
            # icon_style = app.css('div.app-icon::attr(style)').get()
            # if icon_style:
            #     # Controleer of de base64-string aanwezig is in het style-attribuut
            #     match = re.search(r'url\(data:image;base64,(.*?)\)', icon_style)
            #     if match:
            #         base64_string = match.group(1)
            #         Apps_GGD["App_icon_base64"] = base64_string
            #     else:
            #         # Als de regex geen match vindt
            #         Apps_GGD["App_icon_base64"] = None
            # else:
            #     # Als het style-attribuut niet aanwezig is
            #     Apps_GGD["App_icon_base64"] = None

            # Extra informatie link
            extra_info_link = app.css('a.btn.btn-orange.pull-right::attr(href)').get()
            if extra_info_link:
                extra_info_url = response.urljoin(extra_info_link)
                request = scrapy.Request(extra_info_url, callback=self.parse_extra_info)
                request.meta['item'] = Apps_GGD
                yield request
            else:
                Apps_GGD["Beschrijving_lang"] = None
                yield Apps_GGD

    def parse_extra_info(self, response):
        Apps_GGD = response.meta.get('item')
        if not Apps_GGD:
            self.logger.error('Apps_GGD is None in parse_extra_info')
            return
        try:
            beschrijvingen = response.css('div#beschrijving div.row div.col-xs-12::text').getall()
            extra_beschrijving = " ".join(beschrijvingen).strip()
            Apps_GGD["Beschrijving_lang"] = extra_beschrijving if extra_beschrijving else None
        except Exception as e:
            self.logger.error(f'Error extracting description: {e}')
            Apps_GGD["Beschrijving_lang"] = None
        yield Apps_GGD
