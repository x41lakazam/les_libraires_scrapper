# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from .items import BookItem
from leslibraires.constants import *
import datetime

class BookPipeline:

    def process_item(self, item, spider):
        item.setdefault('_librairies', [])
        item['_librairies'] = list(filter(lambda lib: lib not in UNTRUSTED_LIBRARIES, item['_librairies']))

        return item

class CsvBookWriterPipeline:

    def open_spider(self, spider):
        print("[*] Creating CSV file")
        self.valid_items_count = 0

        open("running.state", 'w').write('1')
        self.csv_file = open("results.csv", 'w')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=BookItem.keys())
        self.csv_writer.writeheader()

    def process_item(self, item, spider):
        print(f"Checking {item}")
        if item.validate():
            print("[v] Book {} is valid".format(item['title']))
            self.csv_writer.writerow(item.as_dict())
            self.valid_items_count += 1
        else:
            print("[x] Book {} is invalid:".format(item['title']))

        return item

    def close_spider(self, spider):
        self.csv_file.close()
        now = datetime.datetime.now()
        today = "{}/{}/{}".format(now.day, now.month, now.year)
        open("last_crawl_date.txt", "w").write(str(today))
        open("running.state", 'w').write('0')

        print(f"Finished, {self.valid_items_count} books found")

