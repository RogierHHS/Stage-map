from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from w3lib.html import remove_tags  # Deze functie kan HTML-tags verwijderen
import mysql.connector
import re
import logging
import html
import os
from dotenv import load_dotenv

class CleanDataPipeline:
    def process_item(self, item, spider):
        logging.info(f"Processing item: {item}")

        # Verwijder ongewenste metadata voor alle spiders
        for key in ['depth', 'download_timeout', 'download_slot', 'download_latency']:
            item.pop(key, None)

        if spider.name == "IZ-InDeWijkSpider":
            self.clean_iz_item(item)
        elif spider.name == "ZTE":
            self.clean_zte_item(item)
        elif spider.name == "UIT":
            self.clean_uit_item(item)
        elif spider.name == "GGD_APP":
            self.clean_ggd_item(item)
        elif spider.name == "thuisarts":
            self.clean_thuisarts_item(item)
        elif spider.name == "scheidingspunt":
            self.clean_scheidingspunt_item(item)

        return item

    def clean_iz_item(self, item):
        # Verwijder HTML-tags uit de extra beschrijving en andere schoonmaakacties
        if 'Extra_beschrijving' in item:
            item['Extra_beschrijving'] = remove_tags(item['Extra_beschrijving'])
            item['Extra_beschrijving'] = re.sub(r'\s+', ' ', item['Extra_beschrijving']).strip()
            item['Extra_beschrijving'] = html.unescape(item['Extra_beschrijving'])

    def clean_zte_item(self, item):
        if 'Beschrijving' in item:
            item['Beschrijving'] = item['Beschrijving'].replace('\n', ' ').strip()
            item['Beschrijving'] = re.sub(r'\s+', ' ', item['Beschrijving'])

    def clean_uit_item(self, item):
        if 'Datum' in item:
            item['Datum'] = item['Datum'].replace('\n', ' ').strip()
            item['Datum'] = re.sub(r'\s+', ' ', item['Datum'])

        if 'Beschrijving' in item:
            item['Beschrijving'] = item['Beschrijving'].replace('\n', ' ').strip()
            item['Beschrijving'] = re.sub(r'\s+', ' ', item['Beschrijving'])

    def clean_ggd_item(self, item):
        if 'Beschrijving_lang' in item:
            item['Beschrijving_lang'] = remove_tags(item['Beschrijving_lang'])
            item['Beschrijving_lang'] = item['Beschrijving_lang'].replace('\n', ' ').strip()
            item['Beschrijving_lang'] = re.sub(r'\s+', ' ', item['Beschrijving_lang'])

        if 'Beschrijving_kort' in item:
            item['Beschrijving_kort'] = item['Beschrijving_kort'].replace('\r', ' ').strip()

    def clean_thuisarts_item(self, item):
        if 'Samenvatting' in item:
            item['Samenvatting'] = remove_tags(item['Samenvatting'])
            item['Samenvatting'] = re.sub(r'\s+', ' ', item['Samenvatting'])
            item['Samenvatting'] = item['Samenvatting'].replace('\n\t', ' ').strip()

        # Als je extra schoonmaakacties nodig hebt voor de situaties, voeg ze hier toe
        if 'Situaties' in item:
            for situatie in item['Situaties']:
                if 'Titel' in situatie:
                    situatie['Titel'] = situatie['Titel'].strip()
                if 'Link' in situatie:
                    situatie['Link'] = situatie['Link'].strip()
    
    def clean_scheidingspunt_item(self, item):
        # Controleer of de titel en beschrijving niet leeg zijn
        if not item['Titel'] or not item['Wat'] or not item['Voor_wie'] or not item['Wanneer']:
            raise DropItem(f"Incomplete item: {item}")


class MySQLPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__) 

    def open_spider(self, spider):
        load_dotenv()

        db_host = os.getenv('DB_HOST')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')
        db_ssl_ca = os.getenv('DB_SSL_CA')  # Removed comma

        # Ensure db_ssl_ca is a string
        if not os.path.isabs(db_ssl_ca):
            db_ssl_ca = os.path.join(os.getcwd(), db_ssl_ca)

        try:
            self.conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                ssl_ca=db_ssl_ca
            )
            self.cursor = self.conn.cursor()
            self.logger.info("Database connection established successfully.")
        except mysql.connector.Error as err:
            self.logger.error(f"Error connecting to database: {err}")
            self.conn = None

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed.")


    def process_item(self, item, spider):
        if spider.name == 'IZ-InDeWijkSpider':
            return self.process_item_iz(item)
        elif spider.name == 'ZTE':
            return self.process_item_zte(item)
        elif spider.name == 'ZMA':
            return self.process_item_zma(item)
        elif spider.name == 'UIT':  
            return self.process_item_uit(item)
        elif spider.name == 'GGD_APP':
            return self.process_item_ggd(item)
        elif spider.name == 'thuisarts':
            return self.process_item_thuisarts(item)
        elif spider.name == 'ZVE':
            return self.process_item_zve(item)
        elif spider.name == 'vierstroom':
            return self.process_item_vierstroom(item)
        elif spider.name == 'scheidingspunt':
            return self.process_item_scheidingspunt(item)
        elif spider.name == 'evie':
            return self.process_item_evie(item)
        elif spider.name == 'NLZVE':
            return self.process_item_nlzve(item)
        else:
            return item

    def process_item_iz(self, item):
        try:
            self.cursor.execute("""
                INSERT INTO activiteiten 
                (Titel, Link, Datum_numeriek, Datum_text, Beschrijving, Starttijd, Eindtijd, Locatie, URL_afbeelding, Extra_beschrijving)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    Titel = VALUES(Titel),
                    Datum_numeriek = VALUES(Datum_numeriek),
                    Datum_text = VALUES(Datum_text),
                    Beschrijving = VALUES(Beschrijving),
                    Starttijd = VALUES(Starttijd),
                    Eindtijd = VALUES(Eindtijd),
                    Locatie = VALUES(Locatie),
                    URL_afbeelding = VALUES(URL_afbeelding),
                    Extra_beschrijving = VALUES(Extra_beschrijving)
            """, (
                item['Titel'],
                item['Link'],
                item['Datum_numeriek'],
                item['Datum_text'],
                item['Beschrijving'],
                item['Starttijd'],
                item['Eindtijd'],
                item['Locatie'],
                item['URL_afbeelding'],
                item['Extra_beschrijving']
            ))
            self.conn.commit()
            self.logger.info(f"Item inserted into activiteiten: {item.get('Titel')}")
        except mysql.connector.Error as err:
            self.logger.error(f"Error inserting item {item.get('Titel')}: {err}")
            self.conn.rollback()
        return item

    def process_item_zte(self, item):
        # Query om gegevens op te slaan in de 'activiteiten_zte' tabel
        self.cursor.execute("""
            INSERT INTO activiteiten_zte 
            (Titel, Link, Url_header_afbeelding, Datum_numeriek, Datum_text, Url_afbeelding, Beschrijving)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                Titel = VALUES(Titel),
                Datum_numeriek = VALUES(Datum_numeriek),
                Datum_text = VALUES(Datum_text),
                Url_header_afbeelding = VALUES(Url_header_afbeelding),
                Url_afbeelding = VALUES(Url_afbeelding),
                Beschrijving = VALUES(Beschrijving)
        """, (
            item['Titel'],
            item['Link'],
            item['Url_header_afbeelding'],
            item['Datum_numeriek'],
            item['Datum_text'],
            item['Url_afbeelding'],
            item['Beschrijving']
        ))
        self.conn.commit()
        return item

    def process_item_zma(self, item):
        # Query om gegevens op te slaan in de 'activiteiten_zma' tabel
        self.cursor.execute("""
            INSERT INTO activiteiten_zma 
            (Titel, Link, Beschrijving, Startdatum, Categorie_1, Categorie_2, Categorie_3, Categorie_4, Url_header_afbeelding, Extra_beschrijving, Url_afbeelding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                Titel = VALUES(Titel),
                Beschrijving = VALUES(Beschrijving),
                Startdatum = VALUES(Startdatum),
                Categorie_1 = VALUES(Categorie_1),
                Categorie_2 = VALUES(Categorie_2),
                Categorie_3 = VALUES(Categorie_3),
                Categorie_4 = VALUES(Categorie_4),
                Url_header_afbeelding = VALUES(Url_header_afbeelding),
                Extra_beschrijving = VALUES(Extra_beschrijving),
                Url_afbeelding = VALUES(Url_afbeelding)
        """, (
            item['Titel'],
            item['Link'],
            item['Beschrijving'],
            item['Startdatum'],
            item['Categorie_1'],
            item['Categorie_2'],
            item['Categorie_3'],
            item['Categorie_4'],
            item['Url_header_afbeelding'],
            item['Extra_beschrijving'],
            item['Url_afbeelding']
        ))
        self.conn.commit()
        return item

    def process_item_uit(self, item):
        # Query om gegevens op te slaan in de 'activiteiten_uit' tabel
        self.cursor.execute("""
            INSERT INTO activiteiten_UIT 
            (Titel, Naam, Beschrijving, Datum, Starttijd, Eindtijd, Prijs, Straat, Postcode, Email, Bedrijf_Website, Url_plaatje)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                Naam = VALUES(Naam),
                Beschrijving = VALUES(Beschrijving),
                Datum = VALUES(Datum),
                Starttijd = VALUES(Starttijd),
                Eindtijd = VALUES(Eindtijd),
                Prijs = VALUES(Prijs),
                Straat = VALUES(Straat),
                Postcode = VALUES(Postcode),
                Email = VALUES(Email),
                Bedrijf_Website = VALUES(Bedrijf_Website),
                Url_plaatje = VALUES(Url_plaatje)
        """, (
            item['Titel'],
            item['Naam'],  
            item['Beschrijving'],
            item['Datum'],
            item['Starttijd'],
            item['Eindtijd'],
            item['Prijs'],
            item['Straat'],
            item['Postcode'],
            item['Email'],
            item['Bedrijf_Website'],
            item['Url_plaatje']
        ))
        self.conn.commit()
        return item
    

    def process_item_ggd(self, item):
        sql = """
            INSERT INTO apps_ggd 
            (App_naam, App_rating, Beschrijving_kort, Beschrijving_lang, 
            Dagelijks_Functioneren, Kwaliteit_van_Leven, Lichaamsfuncties, 
            Meedoen, Mentaal_Welbevinden, Zingeving,Android_link, iOS_link, Desktop_link)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                App_naam = VALUES(App_naam),
                App_rating = VALUES(App_rating),
                Beschrijving_kort = VALUES(Beschrijving_kort),
                Beschrijving_lang = VALUES(Beschrijving_lang),
                Dagelijks_Functioneren = VALUES(Dagelijks_Functioneren),
                Kwaliteit_van_Leven = VALUES(Kwaliteit_van_Leven),
                Lichaamsfuncties = VALUES(Lichaamsfuncties),
                Meedoen = VALUES(Meedoen),
                Mentaal_Welbevinden = VALUES(Mentaal_Welbevinden),
                Zingeving = VALUES(Zingeving),
                Android_link = VALUES(Android_link),
                iOS_link = VALUES(iOS_link),
                Desktop_link = VALUES(Desktop_link)
        """
        data = (
            item.get('App_naam'),
            item.get('App_rating'),
            item.get('Beschrijving_kort'),
            item.get('Beschrijving_lang'),
            item.get('Dagelijks_Functioneren'),
            item.get('Kwaliteit_van_Leven'),
            item.get('Lichaamsfuncties'),
            item.get('Meedoen'),
            item.get('Mentaal_Welbevinden'),
            item.get('Zingeving'),
            item.get('Android_link'),
            item.get('iOS_link'),
            item.get('Desktop_link'),
        )
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
            self.logger.info(f"Item inserted into apps_ggd: {item['App_naam']}")
        except mysql.connector.Error as err:
            self.logger.error(f"Error inserting item {item['App_naam']}: {err}")
            self.conn.rollback()
        return item
    
    def process_item_thuisarts(self, item):
        try:
            # Loop door elke situatie en sla deze op samen met het onderwerp
            for situatie in item.get('Situaties', []):
                self.cursor.execute("""
                    INSERT INTO thuisarts (Onderwerp, Link_onderwerp, Samenvatting, Situatie_Titel, Situatie_Link)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        Samenvatting = VALUES(Samenvatting),
                        Situatie_Link = VALUES(Situatie_Link)
                """, (
                    item.get('Onderwerp'),
                    item.get('Link_onderwerp'),
                    item.get('Samenvatting'),
                    situatie.get('Titel'),
                    situatie.get('Link')
                ))
            self.conn.commit()
            self.logger.info(f"Item verwerkt voor onderwerp: {item['Onderwerp']}")
        except mysql.connector.Error as err:
            self.logger.error(f"Error bij verwerken van item {item['Onderwerp']}: {err}")
            self.conn.rollback()
        return item
    
    
    def process_item_zve(self, item):
        # Query om gegevens op te slaan in de 'activiteiten_zve' tabel
        try:
            self.cursor.execute("""
                INSERT INTO workshops 
                (titel, organisatie, beschrijving_kort, beschrijving_lang, datum, image_url, link_workshop, aantal_bijeenkomsten, eerste_bijeenkomst, laatste_bijeenkomst, inschrijven_kan_tot, datum_bijeenkomst)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    organisatie = VALUES(organisatie),
                    beschrijving_kort = VALUES(beschrijving_kort),
                    beschrijving_lang = VALUES(beschrijving_lang),
                    datum = VALUES(datum),
                    image_url = VALUES(image_url),
                    aantal_bijeenkomsten = VALUES(aantal_bijeenkomsten),
                    eerste_bijeenkomst = VALUES(eerste_bijeenkomst),
                    laatste_bijeenkomst = VALUES(laatste_bijeenkomst),
                    inschrijven_kan_tot = VALUES(inschrijven_kan_tot),
                    datum_bijeenkomst = VALUES(datum_bijeenkomst)
            """, (
                item.get('Titel'),
                item.get('Organisatie'),
                item.get('Beschrijving_kort'),
                item.get('Beschrijving_lang'),
                item.get('Datum'),
                item.get('Image_url'),
                item.get('Link_workshop'),
                item.get('Aantal_bijeenkomsten'),
                item.get('Eerste_bijeenkomst'),
                item.get('Laatste_bijeenkomst'),
                item.get('Inschrijven_kan_tot'),
                item.get('Datum_bijeenkomst')
            ))
            self.conn.commit()
            self.logger.info(f"Item inserted into activiteiten_zve: {item.get('titel')}")
        except mysql.connector.Error as err:
            self.logger.error(f"Error inserting item {item.get('titel')}: {err}")
            self.conn.rollback()
        return item


    def process_item_vierstroom(self, item):
        # Query om gegevens op te slaan in de 'vierstroom' tabel
        try:
            self.cursor.execute("""
                INSERT INTO vierstroom_nieuws
                (titel, beschrijving_kort, categorie, image_url, link, Beschrijving_lang)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    beschrijving_kort = VALUES(beschrijving_kort),
                    categorie = VALUES(categorie),
                    image_url = VALUES(image_url),
                    link = VALUES(link),
                    Beschrijving_lang = VALUES(Beschrijving_lang)
                    
        """, (
            item.get('Titel'),
            item.get('Beschrijving_kort'),
            item.get('Categorie'),
            item.get('Image_url'),
            item.get('Link'),
            item.get('Beschrijving_lang')
        ))
            self.conn.commit()
            self.logger.info(f"Item inserted into vierstroom_nieuws: {item.get('titel')}")
        except mysql.connector.Error as err:
            self.logger.error(f"Error inserting item {item.get('titel')}: {err}")
            self.conn.rollback()
        return item
                                
    def process_item_scheidingspunt(self, item):
        # Query om gegevens op te slaan in de 'scheidingspunt' tabel
        try:
            self.cursor.execute("""
                INSERT INTO activiteiten_scheidingpunt
                (titel, link, wat, voor_wie, wanneer)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    titel = VALUES(titel),
                    wat = VALUES(wat),
                    voor_wie = VALUES(voor_wie),
                    wanneer = VALUES(wanneer),
                    link = VALUES(link)
        """, (
            item.get('Titel'),
            item.get('Link'),
            item.get('Wat'),
            item.get('Voor_wie'),
            item.get('Wanneer')
        ))
            self.conn.commit()
            self.logger.info(f"Item inserted into scheidingspunt: {item.get('titel')}")
        except mysql.connector.Error as err:
            self.logger.error(f"Error inserting item {item.get('titel')}: {err}")
            self.conn.rollback()
        return item
    
    def process_item_evie(self, item):
        try:
            self.cursor.execute("""
                INSERT INTO evie_data
                (Titel, Categorieën, Link, Afbeelding_url, Beschrijving, Link_naar_meer_info, Tekst_knop)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    Titel = VALUES(Titel),
                    Categorieën = VALUES(Categorieën),
                    Link = VALUES(Link),
                    Afbeelding_url = VALUES(Afbeelding_url),
                    Beschrijving = VALUES(Beschrijving),
                    Link_naar_meer_info = VALUES(Link_naar_meer_info),
                    Tekst_knop = VALUES(Tekst_knop)
            """, (
                item.get('Titel'),
                ','.join(item.get('Categorieën', [])),
                item.get('Link'),
                item.get('Afbeelding_url'),
                item.get('Beschrijving'),
                item.get('Link_naar_meer_info'),
                item.get('Tekst_knop')
            ))
            self.conn.commit()
            self.logger.info(f"Item inserted into evie_activiteiten: {item.get('Titel')}")
        except mysql.connector.Error as err:
            self.logger.error(f"Error inserting item {item.get('Titel')}: {err}")
            self.conn.rollback()
        return item
    

    def process_item_nlzve(self, item):
    # Query om gegevens op te slaan in de 'activiteiten_nlzve' tabel
        self.cursor.execute("""
            INSERT INTO activiteiten_nlzve 
            (Titel, Locatie, Begintijd, Eindtijd, Beschrijving_kort, Beschrijving_lang, Link, Afbeelding_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                Titel = VALUES(Titel),
                Locatie = VALUES(Locatie),
                Begintijd = VALUES(Begintijd),
                Eindtijd = VALUES(Eindtijd),
                Beschrijving_kort = VALUES(Beschrijving_kort),
                Beschrijving_lang = VALUES(Beschrijving_lang),
                Link = VALUES(Link),
                Afbeelding_url = VALUES(Afbeelding_url)
        """, (
            item['Titel'],
            item['Locatie'],
            item['Begintijd'],
            item['Eindtijd'],
            item['Beschrijving_kort'],
            item['Beschrijving_lang'],
            item['Link'],
            item['Afbeelding_url']
        ))
        self.conn.commit()
        return item

        
    