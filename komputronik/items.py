import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


def format_price(value):
    try:
        return float(value.replace("\xa0", ""))
    except ValueError:
        pass


class KomputronikItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    processor_type = scrapy.Field()
    graphics_card = scrapy.Field()
    motherboard_chipset = scrapy.Field()


class KomputronikItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    price_in = MapCompose(remove_tags, format_price)
