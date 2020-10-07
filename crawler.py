#!/usr/local/bin/python3
import scrapy
from scrapy.crawler import CrawlerProcess
from leslibraires.spiders.books_spider import BooksListSpider
import logging


process = CrawlerProcess()
process.crawl(BooksListSpider)
process.start()

print("Done !")
