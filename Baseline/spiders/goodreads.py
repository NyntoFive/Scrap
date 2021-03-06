import scrapy
from scrapy.loader import ItemLoader
from Baseline.items import QuoteItem


class GoodReadsSpider(scrapy.Spider):
    # identify
    name = "goodreads"

    # Requests
    def start_requests(self):
        url = "https://www.goodreads.com/quotes?page=1"

        yield scrapy.Request(url=url, callback=self.parse)

    # Response
    def parse(self, response):
        for quote in response.selector.xpath('//div[@class="quote"]'):
            loader = ItemLoader(item=QuoteItem(), selector=quote, response=response)

            loader.add_xpath("text", ".//div[@class='quoteText']/text()[1]")
            loader.add_xpath("author", './/div[@class="quoteText"]/child::span/text()')
            loader.add_xpath(
                "tags", './/div[@class="greyText smallText left"]/a/text()'
            )
            yield loader.load_item()

        # /quotes?page=2
        next_page = response.selector.xpath(
            '//a[@class="next_page"]/@href'
        ).extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
