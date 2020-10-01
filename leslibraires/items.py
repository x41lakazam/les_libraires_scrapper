# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from .constants import *

class BookItem(scrapy.Item):
    title           = Field()
    author          = Field()
    edition         = Field()
    book_format     = Field()
    ean13           = Field()
    isbn            = Field()
    publish_date    = Field()
    collection      = Field()
    page_nb         = Field()
    dimensions      = Field()
    weight          = Field()
    lang            = Field()

    _librairies      = Field()


    @classmethod
    def keys(cls):
        return [
            'title',
            'author',
            'edition',
            'book_format',
            'ean13',
            'isbn',
            'publish_date',
            'collection',
            'page_nb',
            'dimensions',
            'weight',
            'lang',
        ]

    def as_dict(self):
        return dict(
            title        = self.get('title', ''),
            author       = self.get('author', ''),
            edition      = self.get('edition', ''),
            book_format  = self.get('book_format', ''),
            ean13        = self.get('ean13', ''),
            isbn         = self.get('isbn', ''),
            publish_date = self.get('publish_date', ''),
            collection   = self.get('collection', ''),
            page_nb      = self.get('page_nb', ''),
            dimensions   = self.get('dimensions', ''),
            weight       = self.get('weight', ''),
            lang         = self.get('lang', ''),
        )

    def validate(self):
        if len(self['_librairies']) < 3:
            return False

        # Add your filters here

        return True


    def __str__(self):
        return f"{self['title']} - {self['author']}"

class LeslibrairesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
