import scrapy


class IzIndewijkspiderSpider(scrapy.Spider):
    name = "IZ-InDeWijkSpider"
    allowed_domains = ["www.inzet-indewijk.nl"]
    start_urls = ["https://www.inzet-indewijk.nl/evenementen/"]

    def parse_details(self, response):
        activiteiten = response.css('li.UniversalListItem_item__lLGLO')

        for activiteit in activiteiten:

            yield {
                "Titel": activiteit.css("a::text").get(),
                "Link": activiteit.css("a::attr(href)").get(),
                "Datum_numeriek": activiteit.css('div.UniversalListItem_eventInformation__TKRxt time::attr(datetime)').get,
                "Datum_text": activiteit.css('div.UniversalListItem_eventInformation__TKRxt time::text').get(),
                "Beschrijving":  activiteit.css('div.UniversalListItem_teaser__mhBWx p::text').get(),
                "Starttijd" : activiteit.css('div.UniversalListItem_eventInformation__TKRxt time::text').getall()[1],
                "Eindtijd" : activiteit.css('div.UniversalListItem_eventInformation__TKRxt time::text').getall()[2],
                "Locatie": activiteit.css('span.UniversalListItem_eventInformationText__1QKSF::text').get(),
                "URL_plaatje": activiteit.css('div.UniversalListItem_imageContainer__TBU3s img::attr(src)').get(),
}
        pass
