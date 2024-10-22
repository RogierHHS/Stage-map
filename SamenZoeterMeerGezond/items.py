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
    URL_afbeelding= scrapy.Field()
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

class ActiviteitenZMA(scrapy.Item):
    Titel = scrapy.Field()
    Link = scrapy.Field()
    Beschrijving = scrapy.Field()
    Startdatum = scrapy.Field()
    Categorie_1 = scrapy.Field()
    Categorie_2 = scrapy.Field()
    Categorie_3 = scrapy.Field()
    Categorie_4 = scrapy.Field()
    Url_header_afbeelding = scrapy.Field()
    Extra_beschrijving = scrapy.Field()
    Url_afbeelding = scrapy.Field()

class ActiviteitenUIT(scrapy.Item):
    Titel = scrapy.Field()
    Naam = scrapy.Field()
    Straat = scrapy.Field()
    Postcode = scrapy.Field()
    Email = scrapy.Field()
    Bedrijf_Website = scrapy.Field()
    Beschrijving = scrapy.Field()
    Datum = scrapy.Field()
    Starttijd = scrapy.Field()
    Eindtijd = scrapy.Field()
    Prijs = scrapy.Field()
    Url_plaatje = scrapy.Field()

class AppsGGD(scrapy.Item):
    App_naam = scrapy.Field()
    Beschrijving_kort = scrapy.Field()
    Lichaamsfuncties = scrapy.Field()
    Dagelijks_Functioneren = scrapy.Field()
    Mentaal_Welbevinden = scrapy.Field()
    Kwaliteit_van_Leven = scrapy.Field()    
    Zingeving = scrapy.Field()
    Meedoen = scrapy.Field()
    App_rating = scrapy.Field()
    Android_link = scrapy.Field()
    iOS_link = scrapy.Field()
    Desktop_link = scrapy.Field()
    # App_icon_base64 = scrapy.Field()
    Beschrijving_lang = scrapy.Field()

class Thuisarts(scrapy.Item):
    Onderwerp = scrapy.Field()
    Link_onderwerp = scrapy.Field()
    Samenvatting = scrapy.Field()
    Situaties = scrapy.Field()


class WorkshopsZVE(scrapy.Item):
    titel = scrapy.Field()
    organisatie = scrapy.Field()
    beschrijving_kort = scrapy.Field()
    datum = scrapy.Field()
    beschrijving_lang = scrapy.Field()
    image_url = scrapy.Field()
    link_workshop = scrapy.Field()
    aantal_bijeenkomsten = scrapy.Field()
    eerste_bijeenkomst = scrapy.Field()
    laatste_bijeenkomst = scrapy.Field()
    inschrijven_kan_tot = scrapy.Field()
    datum_bijeenkomst = scrapy.Field()

class Vierstroom(scrapy.Item):
    titel = scrapy.Field()
    beschrijving_kort = scrapy.Field()
    categorie = scrapy.Field()
    image_url = scrapy.Field()
    link = scrapy.Field()
    Beschrijving_lang = scrapy.Field()

class Scheidingspunt(scrapy.Item):
    titel = scrapy.Field()
    link = scrapy.Field()
    wat = scrapy.Field()
    voor_wie = scrapy.Field()
    wanneer = scrapy.Field()

class Evie(scrapy.Item):
    titel = scrapy.Field()
    link = scrapy.Field()
    categorieen = scrapy.Field()
    afbeelding_url = scrapy.Field()
    

    
    

    

    





    