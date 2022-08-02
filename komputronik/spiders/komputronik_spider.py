import scrapy

from ..items import KomputronikItem, KomputronikItemLoader


class KomputronikSpiderSpider(scrapy.Spider):
    name = "komputronik_spider"
    allowed_domains = ["komputronik.pl"]
    start_urls = ["https://www.komputronik.pl/search-filter/5801/komputery-do-gier"]

    def parse(self, response):
        number_of_pages = response.xpath(
            "//div[@class='product-list-top-pagination']//li[last()-1]/a/text()"
        ).get()
        for num in range(int(number_of_pages)):
            yield scrapy.Request(
                f"https://www.komputronik.pl/search-filter/5801/komputery-do-gier?p={num+1}",
                callback=self.parse_links,
            )

    def parse_links(self, response):
        links = response.xpath("//div[@class='pe2-head']//a/@href")
        for link in links:
            yield response.follow(link.get(), callback=self.parse_item)

    def parse_item(self, response):
        loader = KomputronikItemLoader(item=KomputronikItem(), response=response)
        loader.add_xpath("name", "//section[@class='p-inner-name']/h1/text()")
        loader.add_xpath("price", "//span[@class='proper']/text()")
        loader.add_xpath(
            "processor_type",
            "//*[text()='Model procesora']/following-sibling::td/text()",
        )
        loader.add_xpath(
            "graphics_card",
            "//*[text()='Karta graficzna']/following-sibling::td//text()",
        )
        loader.add_xpath(
            "motherboard_chipset",
            "//*[text()='Chipset płyty głównej']/following-sibling::td/text()",
        )
        yield loader.load_item()
