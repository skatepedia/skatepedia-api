from django.db import models
from django.utils.translation import ugettext_lazy as _


class RSSFeed(models.Model):
    title = models.TextField(verbose_name=_("Title"), max_length=256)
    link = models.URLField(verbose_name=_("Link"), max_length=1024)
    description = models.CharField(verbose_name=_("Description"), null=True, max_length=1024, blank=True)
    image = models.URLField(verbose_name=_("Image"), max_length=1024, null=True)
    language = models.CharField(verbose_name=_("Language"), max_length=128, blank=True)
    feed_url = models.URLField(verbose_name=_("Feed url"), unique=True)


class RSSItem(models.Model):
    title = models.TextField(verbose_name=_("Title"), max_length=256)
    link = models.URLField(verbose_name=_("Link"), max_length=1024)
    description = models.CharField(verbose_name=_("Description"), null=True, max_length=1024, blank=True)
    published_at = models.CharField(verbose_name=_("Published at"), max_length=128)
    categories = models.CharField(verbose_name=_("Categories"), null=True, max_length=128, blank=True)
    creator = models.CharField(verbose_name=_("Creator"), max_length=128, blank=True)
    feed = models.ForeignKey(RSSFeed, null=True, on_delete=models.PROTECT)


class Skater(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    bio = models.CharField(verbose_name=_("Bio"), max_length=128, blank=True)
    age = models.PositiveSmallIntegerField(verbose_name=_("Age"), null=True, blank=True)
    style = models.CharField(verbose_name=_("Style"), max_length=128, blank=True)
    image = models.URLField(verbose_name=_("Image"), max_length=512, blank=True)
    country = models.CharField(verbose_name=_("Country"), max_length=128, blank=True)
    external_uuid = models.CharField(verbose_name=_("external_url"), max_length=128)

    def __str__(self):
        return f"{self.name} - {(self.country)}"


class Person(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    image = models.CharField(verbose_name=_("Profile picture"), max_length=128)
    external_uuid = models.CharField(verbose_name=_("external_url"), max_length=128)


class Brand(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    description = models.TextField(verbose_name=_("Description"), max_length=1024)
    logo = models.URLField(verbose_name=_("Logo"), null=True)
    website = models.URLField(verbose_name=_("Website"), null=True)
    links = models.TextField(verbose_name=_("Hyperlinks"), max_length=2000)
    external_uuid = models.CharField(verbose_name=_("External_url"), max_length=128)

    members = models.CharField(verbose_name=_("Members"), max_length=1024, blank=True)
    similar_brands = models.CharField(verbose_name=_("Related Brands"), max_length=1024,  blank=True)


class Track(models.Model):
    name = models.CharField(verbose_name=_("Nmae"), max_length=128)
    artist = models.CharField(verbose_name=_("Artist"), max_length=128)
    itunes_url = models.CharField(verbose_name=_("Itunes url"), max_length=128)


class Soundtrack(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    tracks = models.CharField(max_length=1024)
    external_uuid = models.CharField(verbose_name=_("External_url"), max_length=128)


class Video(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128, blank=True, null=True)

    country = models.CharField(verbose_name=_("Country"), max_length=128, blank=True, null=True)
    description = models.CharField(verbose_name=_("description"), max_length=1028, blank=True, null=True)
    image = models.URLField(verbose_name=_("Video Poster"), null=True, blank=True)
    runtime = models.PositiveSmallIntegerField(null=True, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    category = models.CharField(verbose_name=_("Category"), max_length=24, blank=True, null=True)
    external_uuid = models.CharField(verbose_name=_("external_url"), max_length=128)

    director = models.CharField(verbose_name=_("Director"), max_length=1024, blank=True, null=True)
    brand = models.CharField(verbose_name=_("Brand"), max_length=512, blank=True, null=True);
    soundtrack = models.CharField(verbose_name=_("Soundtrack"), max_length=2056, blank=True, null=True);
    skaters = models.CharField(verbose_name=_("Skaters"), max_length=2056, blank=True, null=True)


class Clip(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    thumbnail = models.CharField(verbose_name=_("Clip Thumbnail"), max_length=128)
    url = models.CharField(verbose_name=_("Clip URL"), max_length=128)
    video = models.CharField(verbose_name=_("Video"), max_length=512)
