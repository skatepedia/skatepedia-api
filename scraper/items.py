# -*- coding: utf-8 -*-
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from w3lib.html import (
    remove_tags,
    replace_escape_chars,
    strip_html5_whitespace
)
from scrapy.loader import ItemLoader
from scrapy_djangoitem import DjangoItem
from scrapy.loader.processors import TakeFirst, MapCompose

from skatepedia.db.models import (
    Clip,
    Track,
    Video,
    Person,
    Skater,
    Brand,
    Soundtrack,
    RSSFeed,
    RSSItem
)


class SkaterItem(DjangoItem):
    django_model = Skater


class PersonItem(DjangoItem):
    django_model = Person


class BrandItem(DjangoItem):
    django_model = Brand

    videos = scrapy.Field()
    skaters = scrapy.Field()
    similar_companies = scrapy.Field()
    ads = scrapy.Field()


class VideoItem(DjangoItem):
    django_model = Video


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


class RSSFeedItem(DjangoItem):
    django_model = RSSFeed


class RSSParsedItem(DjangoItem):
    django_model = RSSItem


class RSSItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    feed_in = TakeFirst()
    category_out = MapCompose()


class SkaterItemLoader(ItemLoader):
    bio_in = MapCompose(strip_html5_whitespace, replace_escape_chars)
    country_in = MapCompose(strip_html5_whitespace, replace_escape_chars)
    age_in = MapCompose(int)


class VideoItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    year_in = MapCompose(int)
