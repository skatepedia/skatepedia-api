import uuid
from datetime import datetime

from ipfs_storage.storage import InterPlanetaryFileSystemStorage

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, auto_now=True)
    updated_by = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, null=True, blank=True
    )
    skatevideosite_id = models.PositiveIntegerField(
        verbose_name=_("skatevideosite_id"), unique=True, null=True, blank=True
    )

    # RAW Scraped data and source
    raw_data = models.JSONField(null=True, blank=True)
    source_url = models.URLField(unique=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}" if self.name else self.source_url or str(self.id)

    def save(self, *args, **kwargs):
        if self.source_url and self.__dict__.get("slug"):
            self.slug = slugify(self.source_url.split("/")[-1])
        super().save(*args, **kwargs)


class Person(BaseModel):
    name = models.CharField(
        verbose_name=_("Name"), max_length=128, null=True, blank=True
    )
    image = models.CharField(
        verbose_name=_("Profile picture"), max_length=128, null=True, blank=True
    )
    gender = models.CharField(
        verbose_name=_("Gender"), max_length=1, null=True, blank=True
    )
    bio = models.CharField(verbose_name=_("Bio"), max_length=128, null=True, blank=True)
    year_of_birth = models.PositiveSmallIntegerField(
        "birthday year", default=0, blank=True
    )
    city = models.CharField(
        verbose_name=_("City"), max_length=128, null=True, blank=True
    )
    country = models.CharField(
        verbose_name=_("Country"), max_length=128, null=True, blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} - {(self.country)}"

    @property
    def age(self):
        return datetime.now().year - self.year_of_birth


class Filmmaker(Person):
    stance = models.CharField(verbose_name=_("Stance"), max_length=128, blank=True)


class Skater(Person):
    stance = models.CharField(verbose_name=_("Stance"), max_length=128, blank=True)


class Company(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=128, blank=True)
    description = models.TextField(
        verbose_name=_("Description"), max_length=1028, blank=True
    )
    logo = models.URLField(verbose_name=_("Logo"), null=True, blank=True)
    website = models.URLField(verbose_name=_("Website"), null=True, blank=True)
    links = models.TextField(verbose_name=_("Hyperlinks"), max_length=2000, blank=True)
    skaters = models.ManyToManyField(Skater)
    similar_companies = models.ManyToManyField("self")

    class Meta:
        verbose_name_plural = _("Companies")


class VideoCategory(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=128, unique=True)

    class Meta:
        verbose_name_plural = _("Video Categories")


class Video(BaseModel):
    title = models.CharField(verbose_name=_("Title"), max_length=128, blank=True)
    slug = models.CharField(
        verbose_name=_("Slug"), max_length=128, unique=True, blank=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    image = models.URLField(verbose_name=_("Video Poster"), null=True, blank=True)
    runtime = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    trailer = models.URLField(verbose_name=_("Trailer Link"), null=True, blank=True)
    videolink = models.URLField(verbose_name=_("Video Link"), null=True, blank=True)
    links = models.JSONField(
        blank=True,
        verbose_name=_("Video Links"),
        null=True,
    )
    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(
        VideoCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    skaters = models.ManyToManyField(Skater, blank=True)
    filmmakers = models.ManyToManyField(
        Filmmaker, verbose_name=_("Filmmakers"), blank=True
    )
    cids = models.JSONField(verbose_name="List of IPFS CIDs", blank=True, null=True)
    archive_file = models.FileField(
        storage=InterPlanetaryFileSystemStorage(), null=True, blank=True
    )

    def __str__(self):
        return f"{self.title}" if self.title else self.source_url

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)
        if self.source_url and not self.slug:
            self.slug = slugify(self.source_url.split("/")[-1])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("video-detail", kwargs=dict(slug=self.slug))


class Track(BaseModel):
    name = models.CharField(
        verbose_name=_("Name"), max_length=128, unique=True, null=True, blank=True
    )
    artist = models.CharField(verbose_name=_("Artist"), max_length=128)
    links = models.JSONField(verbose_name=_("URLs"), max_length=128)


class Soundtrack(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    tracks = models.ManyToManyField(Track)
    video = models.OneToOneField(Video, on_delete=models.PROTECT)


class Spot(BaseModel):
    name = models.CharField(
        verbose_name=_("Name"), max_length=128, blank=True, null=True
    )
    location = models.URLField(
        verbose_name=_("Name"), max_length=128, blank=True, null=True
    )


class Clip(BaseModel):
    """Skater video part or any specific video clip"""

    name = models.CharField(
        verbose_name=_("Name"), max_length=128, blank=True, null=True
    )
    thumbnail = models.URLField(
        verbose_name=_("Clip Thumbnail"), max_length=128, blank=True
    )
    skaters = models.ManyToManyField(Skater)
    tracks = models.ManyToManyField(Track)
    video = models.ForeignKey(Video, on_delete=models.PROTECT, null=True)
    sort = models.PositiveSmallIntegerField(
        _("Order of the clip in the video"), default=1
    )
