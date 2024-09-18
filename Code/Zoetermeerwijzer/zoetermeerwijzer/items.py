# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZoetermeerwijzerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ActiviteitenIZ(scrapy.Item):
    Titel = scrapy.Field()
    Link = scrapy.Field()
    Datum_numeriek = scrapy.Field()
    Datum_text = scrapy.Field()
    Beschrijving = scrapy.Field()
    Starttijd = scrapy.Field()
    Eindtijd = scrapy.Field()
    Locatie = scrapy.Field()
    URL_plaatje = scrapy.Field()
    Extra_beschrijving = scrapy.Field()
    Volledige_beschrijving = scrapy.Field()

class ActiviteitenZTE(scrapy.Item):
    Titel = scrapy.Field()
    Link = scrapy.Field()
    Url_header_afbeelding = scrapy.Field()
    Datum_numeriek = scrapy.Field()
    Datum_text = scrapy.Field()
    Url_afbeelding = scrapy.Field()
    Beschrijving = scrapy.Field()

    