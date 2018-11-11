from django.utils.translation import ugettext_lazy as _
from django.db import models


class Skater(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    bio = models.CharField(verbose_name=_("Bio"), max_length=128)
    age = models.PositiveSmallIntegerField(default=0)
    style = models.CharField(verbose_name=_("Name"), max_length=128)
    country = models.CharField(verbose_name=_("Country"), max_length=128)
    external_uuid = models.CharField(verbose_name=_("external_url"), max_length=128)


class Person(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    image = models.CharField(verbose_name=_("Profile picture"), max_length=128)
    external_uuid = models.CharField(verbose_name=_("external_url"), max_length=128)


class Brand(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    description = models.TextField(verbose_name=_("Description"), max_length=1028)
    logo = models.URLField(verbose_name=_("Logo"), null=True)
    website = models.URLField(verbose_name=_("Website"), null=True)
    links = models.TextField(verbose_name=_("Hyperlinks"), max_length=2000)
    external_uuid = models.CharField(verbose_name=_("External_url"), max_length=128)

    skaters = models.ManyToManyField(Skater)
    similar_brands = models.ManyToManyField("self")


class Track(models.Model):
    name = models.CharField(verbose_name=_("Nmae"), max_length=128)
    artist = models.CharField(verbose_name=_("Artist"), max_length=128)
    itunes_url = models.CharField(verbose_name=_("Itunes url"), max_length=128)


class Soundtrack(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    tracks = models.ManyToManyField(Track)
    external_uuid = models.CharField(verbose_name=_("External_url"), max_length=128)


class Video(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    description = models.CharField(verbose_name=_("description"), max_length=1028)
    image = models.URLField(verbose_name=_("Video Poster"), null=True)
    runtime = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    external_uuid = models.CharField(verbose_name=_("external_url"), max_length=128)

    director = models.ForeignKey(Person, verbose_name=_("Director"), on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    soundtrack = models.OneToOneField(Soundtrack, on_delete=models.PROTECT)
    skaters = models.ManyToManyField(Skater)


class Clip(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    thumbnail = models.CharField(verbose_name=_("Clip Thumbnail"), max_length=128)
    url =  models.CharField(verbose_name=_("Clip URL"), max_length=128)
    video = models.ForeignKey(Video, on_delete=models.PROTECT, null=True)
