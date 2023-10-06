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

from django.db.utils import IntegrityError

from skatepedia.db.models import (
    Clip,
    Track,
    Video,
    Skater,
    Company,
    Filmmaker,
    Soundtrack
)


def get_or_create(model, unique_value, unique_field="source_url", data=None):
    query = {f"{unique_field}": unique_value}
    obj = model.objects.filter(**query).first()
    if obj:
        return obj
    if data is None:
        data = query
    return model.objects.create(**data)


class SkaterItem(DjangoItem):
    django_model = Skater
    resource = "skaters"


class FilmmakerItem(DjangoItem):
    django_model = Filmmaker
    resource = "filmmakers"


class CompanyItem(DjangoItem):
    django_model = Company

    # m2m fields
    videos_urls = scrapy.Field()
    skaters_urls = scrapy.Field()
    similar_companies_urls = scrapy.Field()

    def save(self, *args, **kwargs):
        skaters = [Skater(source_url=url) for url in self["skaters_urls"]]
        Skater.objects.bulk_create(skaters, ignore_conflicts=True)

        companies = [Company(source_url=url) for url in self["similar_companies_urls"]]
        Company.objects.bulk_create(companies, ignore_conflicts=True)

        self.instance.save()
        self.instance.skaters.add(*(skater.pk for skater in skaters))
        self.instance.similar_companies.add(*(company.pk for company in companies))

        return self.instance.save()


class VideoItem(DjangoItem):
    resource = "videos"
    django_model = Video

    # FK  fields
    category_url = scrapy.Field()
    company_url = scrapy.Field()
    # M2M fields
    skaters_urls = scrapy.Field()
    filmmakers_urls = scrapy.Field()

    def save(self, *args, **kwargs):
        if category_url := self.get("category_url"):
            category = get_or_create(VideoCategory, company_url)
            self.instance.category = category

        if company_url := self.get("company_url"):
            company = get_or_create(Company, company_url)
            self.instance.company = company

        self.instance.save(*args, **kwargs)

        skaters = []
        filmmakers = []

        for url in self.get("skaters_urls", []):
            obj = get_or_create(Skater, url)
            skaters.append(obj.pk)

        for url in self.get("filmmakers_urls", []):
            obj = get_or_create(Filmmaker, url)
            filmmakers.append(obj.pk)

        self.instance.skaters.add(*skaters)
        self.instance.filmmakers.add(*filmmakers)
        return self.instance.save()


class ClipItem(DjangoItem):
    """Depends on Video"""

    resource = "clips"
    django_model = Clip
    tracks = scrapy.Field()
    skaters = scrapy.Field()
    video_url = scrapy.Field()

    def save(self, *args, **kwargs):
        skaters = []
        tracks = []
        video_url = self["video_url"]
        video = get_or_create(Video, video_url)
        self.instance.video = video
        self.instance.save(*args, **kwargs)

        for skater in self.get("skaters", []):
            try:
                obj = skater.save()
            except IntegrityError:
                obj = get_or_create(Skater, skater.get("source_url"))
            skaters.append(obj.pk)
            self.instance.skaters.add(*skaters)

        for track in self.get("tracks", []):
            try:
                obj = track.save()
            except IntegrityError:
                obj = get_or_create(Track, track.get("name"), unique_field="name")
            tracks.append(obj.pk)
            self.instance.tracks.add(*tracks)

        return self.instance.save()


class SoundtrackItem(DjangoItem):
    django_model = Soundtrack
    tracks = scrapy.Field()
    video = scrapy.Field()


class TrackItem(DjangoItem):
    django_model = Track


class RankItem(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()
    points = scrapy.Field()
    skater = scrapy.Field()
