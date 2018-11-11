# -*- coding: utf-8 -*-
# https://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Compose, TakeFirst
from scrapy_djangoitem import DjangoItem

from skatepedia.db.models import (
    Skater,
    Person,
    Brand,
    Video,
    Clip,
    Soundtrack,
    Track,
)


class SkaterItem(DjangoItem):
    django_model = Skater


class PersonItem(DjangoItem):
    django_model = Person


class BrandItem(DjangoItem):
    django_model = Brand

    videos = scrapy.Field()
    skaters = scrapy.Field()
    similar_brands = scrapy.Field()
    ads = scrapy.Field()


class VideoItem(DjangoItem):
    django_model = Video
    clips = scrapy.Field()
    brand = scrapy.Field()
    soundtrack = scrapy.Field()
    director = scrapy.Field()
    skaters = scrapy.Field()


class ClipItem(DjangoItem):
    django_model = Clip


class SoundtrackItem(DjangoItem):
    django_model = Soundtrack
    tracks = scrapy.Field()


class TrackItem(DjangoItem):
    django_model = Track


class RankItem(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()
    points = scrapy.Field()
    skater = scrapy.Field()


class SkaterItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class VideoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
