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
    Titel = scrapy.Field()
    Organisatie = scrapy.Field()
    Beschrijving_kort = scrapy.Field()
    Datum = scrapy.Field()
    Beschrijving_lang = scrapy.Field()
    Image_url = scrapy.Field()
    Link_workshop = scrapy.Field()
    Aantal_bijeenkomsten = scrapy.Field()
    Eerste_bijeenkomst = scrapy.Field()
    Laatste_bijeenkomst = scrapy.Field()
    Inschrijven_kan_tot = scrapy.Field()
    Datum_bijeenkomst = scrapy.Field()

class Vierstroom(scrapy.Item):
    Titel = scrapy.Field()
    Beschrijving_kort = scrapy.Field()
    Categorie = scrapy.Field()
    Image_url = scrapy.Field()
    Link = scrapy.Field()
    Beschrijving_lang = scrapy.Field()

class Scheidingspunt(scrapy.Item):
    Titel = scrapy.Field()
    Link = scrapy.Field()
    Wat = scrapy.Field()
    Voor_wie = scrapy.Field()
    Wanneer = scrapy.Field()

class Evie(scrapy.Item):
    Titel = scrapy.Field()
    Link = scrapy.Field()
    Categorieën = scrapy.Field()
    Afbeelding_url = scrapy.Field()
    Beschrijving = scrapy.Field()
    Link_naar_meer_info = scrapy.Field()
    Tekst_knop = scrapy.Field()

class NLZVE(scrapy.Item):
    Titel = scrapy.Field()
    Link = scrapy.Field()
    Afbeelding_url = scrapy.Field()
    Beschrijving_kort = scrapy.Field()
    Locatie = scrapy.Field()
    Begintijd = scrapy.Field()
    Eindtijd = scrapy.Field()
    Beschrijving_lang = scrapy.Field()
    

    
    

    

    





    