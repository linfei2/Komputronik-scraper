import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def format_price(value):
    try:
        return float(value.replace('\xa0', ''))
    except ValueError:
        pass


class KomputronikItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip, format_price), output_processor=TakeFirst())
    processor_type = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    graphics_card = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    motherboard_chipset = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
