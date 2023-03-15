from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128, unique=True)
    image = models.CharField(verbose_name=_("Profile picture"), max_length=128)
    bio = models.CharField(verbose_name=_("Bio"), max_length=128)
    year_of_birth = models.PositiveSmallIntegerField(
        "birthday year", default=0, blank=True
    )
    country = models.CharField(verbose_name=_("Country"), max_length=128)
    external_uuid = models.CharField(verbose_name=_("external_url"), max_length=128)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} - {(self.country)}"

    @property
    def age(self):
        return datetime.now().year - year_of_birth


class Filmmaker(Person):
    stance = models.CharField(verbose_name=_("Stance"), max_length=128, blank=True)


class Skater(Person):
    stance = models.CharField(verbose_name=_("Stance"), max_length=128, blank=True)


class Company(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    description = models.TextField(verbose_name=_("Description"), max_length=1028)
    logo = models.URLField(verbose_name=_("Logo"), null=True)
    website = models.URLField(verbose_name=_("Website"), null=True)
    links = models.TextField(verbose_name=_("Hyperlinks"), max_length=2000)
    external_uuid = models.CharField(verbose_name=_("External_url"), max_length=128)

    skaters = models.ManyToManyField(Skater)
    similar_companies = models.ManyToManyField("self")

    class Meta:
        verbose_name_plural = _("Companies")


class VideoCategory(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128, unique=True)

    class Meta:
        verbose_name_plural = _("Video Categories")


# Category, Filmmaker, Skater, Company,
class Video(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=128)
    description = models.CharField(verbose_name=_("Description"), max_length=1028)
    slug = models.CharField(verbose_name=_("Slug"), max_length=128, unique=True)
    date = models.DateTimeField(blank=True)

    is_active = models.BooleanField(default=True)
    image = models.URLField(verbose_name=_("Video Poster"), null=True)
    runtime = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    trailer = models.URLField(verbose_name=_("Trailer Link"), null=True)
    videolink = models.URLField(verbose_name=_("Video Link"), null=True)
    external_url = models.CharField(
        verbose_name=_("external_url"), max_length=128, unique=True
    )
    links = models.JSONField(blank=True, verbose_name=_("Video Links"))

    categories = models.ForeignKey(VideoCategory, on_delete=models.PROTECT, null=True)
    skaters = models.ManyToManyField(Skater)
    filmmakers = models.ManyToManyField(
        Filmmaker,
        verbose_name=_("Filmmakers"),
    )
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    soundtracks = models.JSONField(blank=True)  # TODO:mgr move to Soundtrack
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    updated_by = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, null=True
    )
    # cids = models.JSONField(verbose_name="List of IPFS CIDs", blank=True)


class Track(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    artist = models.CharField(verbose_name=_("Artist"), max_length=128)
    links = models.JSONField(verbose_name=_("URLs"), max_length=128)


class Soundtrack(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    tracks = models.ManyToManyField(Track)
    video = models.OneToOneField(Video, on_delete=models.PROTECT)


class Clip(models.Model):
    """Skater video part or any specific video clip"""

    thumbnail = models.URLField(
        verbose_name=_("Clip Thumbnail"), max_length=128, blank=True
    )
    url = models.URLField(
        verbose_name=_("Clip URL from the main video"), max_length=128
    )
    skater = models.ForeignKey(Skater, on_delete=models.PROTECT, null=True)
    track = models.ForeignKey(Track, on_delete=models.PROTECT, null=True)
    video = models.ForeignKey(Video, on_delete=models.PROTECT, null=True)
    sort = models.PositiveSmallIntegerField(
        _("Order of the clip in the video"), default=1
    )
