# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from w3lib.html import remove_tags  # Deze functie kan HTML-tags verwijderen
import mysql.connector
import re

class CleanDataPipeline:
    def process_item(self, item, spider):
        # Verwijder ongewenste metadata
        item.pop('depth', None)
        item.pop('download_timeout', None)
        item.pop('download_slot', None)
        item.pop('download_latency', None)

        # Controleer op essentiële velden
        if not item['Titel'] or not item['Link']:
            raise DropItem(f"Item mist noodzakelijke gegevens: {item}")

        # Opschonen van beschrijvingen (extra witruimte verwijderen)
        if 'Beschrijving' in item:
            item['Beschrijving'] = item['Beschrijving'].strip()

        # Dit stukje code zorgt ervoor dat de witruimtes worden weggehaald en dat er geen meerdere spaties zijn (die vervang je dan met één spatie)
        if 'Extra_beschrijving' in item:

            # Verwijder de HTML-tags, maar behoud de tekst
            item['Extra_beschrijving'] = remove_tags(item['Extra_beschrijving'])

            item['Extra_beschrijving'] = item['Extra_beschrijving'].strip()  
            item['Extra_beschrijving'] = re.sub(r'\s+', ' ', item['Extra_beschrijving'])

        return item
    

class MySQLPipeline:
    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Rogier2004!',
            database='scraping_project'
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

def process_item(self, item, spider):
    # Voeg de data toe, of update bestaande data op basis van de unieke 'Link'
    self.cursor.execute("""
        INSERT INTO activiteiten 
        (Titel, Link, Datum_numeriek, Datum_text, Beschrijving, Starttijd, Eindtijd, Locatie, URL_plaatje, Extra_beschrijving)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            Titel = VALUES(Titel),
            Datum_numeriek = VALUES(Datum_numeriek),
            Datum_text = VALUES(Datum_text),
            Beschrijving = VALUES(Beschrijving),
            Starttijd = VALUES(Starttijd),
            Eindtijd = VALUES(Eindtijd),
            Locatie = VALUES(Locatie),
            URL_plaatje = VALUES(URL_plaatje),
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
        item['URL_plaatje'],
        item['Extra_beschrijving']
    ))
    self.conn.commit()
    return item

