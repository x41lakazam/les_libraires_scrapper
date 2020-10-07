"""
Scrapper pour les rayons
"""
import urllib

import scrapy
from scrapy.loader import ItemLoader
from leslibraires.items import BookItem
from leslibraires.constants import *

class BooksListSpider(scrapy.Spider):
    name = "books_list"

    start_urls = START_URLS

    custom_settings = dict(
        ITEM_PIPELINES = {
            'leslibraires.pipelines.BookPipeline': 300,
            'leslibraires.pipelines.CsvBookWriterPipeline': 400,
        },
        RETRY_HTTP_CODES = [503],
    )
    if MAX_PAGES > 0:
        custom_settings['CLOSESPIDER_PAGECOUNT'] = MAX_PAGES

    def parse(self, response):
        # class ppanel-product
        books_list = response.xpath("//li[@itemtype='http://schema.org/Book']")

        books_nb = len(books_list)

        for ix, book in enumerate(books_list):

            book_item = BookItem()
            book_item['_librairies'] = []

            # Check if 'short' is one of the classes of the book disponibility
            available = book.xpath(".//span[contains(@class, 'delay')]/@class")[0].get()
            if not "short" in available.split(" "):
                continue

            details_uri = book.xpath(".//div[@class='image']/a/@href").get()
            details_url = urllib.parse.urljoin(response.url, details_uri)

            req = scrapy.Request(
                details_url,
                self.parse_book_details,
                meta=dict(book_item=book_item),
                errback=self.errorback,
                headers={('User-Agent', 'Mozilla/5.0')},
            )

            yield req

        next_page = response.xpath("//ul[@class='pagination']/li[@class='active']/following-sibling::li/a/@href")[0].get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_book_details(self, response):

        book_item = response.meta['book_item']

        book_infos = response.xpath("//div[@itemtype='http://schema.org/Book']")[0]
        main_infos = response.xpath("//div[@class='main-infos']")[0]

        author  = main_infos.xpath(".//h2/a/text()").get()
        title   = main_infos.xpath(".//h1/span/text()").get()

        def get_or_none(xpath, default=""):
            selector = response.xpath(xpath)
            if selector:
                return selector[0].get()
            else:
                return default

        book_format = get_or_none("//dl/dt[text() = 'Format']/following-sibling::dd/a/text()")
        ean13 = get_or_none("//dl/dt[text() = 'EAN13']/following-sibling::dd/text()")
        isbn  = get_or_none("//dd[@itemprop='isbn']/text()")
        edition = get_or_none("//dd[@itemprop='publisher']/a/text()")
        publish_date = get_or_none("//dd[@itemprop='datePublished']/text()")
        collection = get_or_none("//dl/dt[text() = 'Collection']/following-sibling::dd/a/text()")
        pages_nb = get_or_none("//dd[@itemprop='numberOfPages']/text()")
        dimensions = get_or_none("//dl/dt[text() = 'Dimensions']/following-sibling::dd/text()")
        weight = get_or_none("//dl/dt[text() = 'Poids']/following-sibling::dd/text()")
        lang    = get_or_none("//dd[@itemprop='inLanguage']/text()")


        weight = weight.replace(u'\xa0', ' ') # TODO: Put in pipeline

        book_item['title']   = title
        #book_item['description'] = description
        book_item['author']  = author
        book_item['book_format'] = book_format
        book_item['ean13'] = ean13
        book_item['isbn'] = isbn
        book_item['edition'] = edition
        book_item['publish_date'] = publish_date
        book_item['collection'] = collection
        book_item['page_nb'] = pages_nb
        book_item['dimensions'] = dimensions
        book_item['weight'] = weight
        book_item['lang'] = lang


        offers_uri = response.xpath("//section[@id='product-offers']/div/a/@href").get()
        if not offers_uri:
            print(f"[x] Book {title}: no offers, passing")
            yield
        else:
            offers_url = urllib.parse.urljoin(response.url, offers_uri)

            req = scrapy.Request(
                offers_url,
                self.parse_book_offers,
                meta=dict(book_item=book_item),
                dont_filter=True,
                errback=self.errorback,
                headers={('User-Agent', 'Mozilla/5.0')},
            )

            yield req

    def parse_book_offers(self, response):

        book_item = response.meta['book_item']

        librairies = response.xpath("//div[@id='offers-new']/table[contains(@class, 'all-offers')]/tbody/tr/td[3]/h3/text()").getall()

        book_item['_librairies'] = librairies

        print("Found item")

        yield book_item

    def errorback(self, failure):
        print("="*50)
        print("="*50)
        print("Failure")
        print(failure)
        print(failure.value.response)
        print("="*50)
        print("="*50)
        print("\n")

    def error_404(self, response):
        print(f"404 error: {response.url}")

