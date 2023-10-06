"""
TRIBUTE  and RESPECT to skately for gathering all the skateboarding data along the years and to webarchive to keep track of it.

The spiders in this module know how to parse the archived content of the Skately library.


Brand - Company
Video
Skater
Track
Clip
Spot
"""
import re
import json
from abc import ABC, abstractmethod
from contextlib import suppress

import scrapy

from scraper.items import (
    ClipItem,
    TrackItem,
    VideoItem,
    SkaterItem,
    CompanyItem,
    SoundtrackItem
)
from scraper.utils import parse_integer

ARCHIVE_BASE_URL = "https://web.archive.org/web/20191003042112/"
LIBRARY_RESOURCE_TYPES = (
    "videos",
    "brands",
    "skaters",
    "people",
    "soundtracks",
    "spots",
)


def parse_relations(links, resources=None):
    """Extract videos, skaters, brands from brand page."""
    match_url = r"[\w\d:#@%/;$()~_?\+-=\\\.&]"
    resources = resources or LIBRARY_RESOURCE_TYPES
    return {
        rel_type: list(set(links.re(f"{match_url}+{rel_type}+{match_url}*")))
        for rel_type in resources
    }


def _first(elements):
    return next(iter(elements), None)


class SkatelySpider(ABC, scrapy.Spider):
    pages = range(2, 9)  # Number of Skately library resource pages
    LIMIT = 1  # Limit scraped items per for debugging purposes

    @property
    @abstractmethod
    def resource(self):
        raise NotImplementedError

    @abstractmethod
    def parse_page(self, response):
        raise NotImplementedError

    def start_requests(self):
        video_library_url = (
            f"{ARCHIVE_BASE_URL}http://skately.com/library/{self.resource}"
        )
        urls = [video_library_url] + [
            f"{ARCHIVE_BASE_URL}http://skately.com/library/{self.resource}/page-%s"
            % (x)
            for x in self.pages
        ]
        for url in urls[: self.LIMIT]:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        resource_urls = set(
            response.css("#lib-list > ul > li > div > a::attr(href)").extract()
        )
        for url in list(resource_urls)[: self.LIMIT]:
            yield scrapy.Request(url, self.parse_page)


def parse_brand_page(response):
    """Parse a library brand page.

    http://skately.com/library/brands/blockhead-skateboards-recycled-rubbish.

    :param response:
    :return: CompanyItem
    """
    response.selector.remove_namespaces()
    rel_links = response.css("#col-left > ul > li > div > a::attr(href)")
    rels = parse_relations(rel_links, resources=["people", "videos", "brands"])
    data = {
        "source_url": response.url,
        "name": response.css("#lib-page-bio > h1::text").extract_first(),
        "description": response.css("#lib-page-bio > p::text").extract_first(),
        "logo": response.css(
            "#lib-page-info > div.entity.ui-corner-all > a > img::attr(src)"
        ).extract_first(),
        "website": response.css(
            "#lib-page-bio > ul > li:nth-child(1) > a::attr(href)"
        ).extract_first(),
        "links": response.css("#lib-page-bio > ul > li > a::attr(href)").extract(),
    }
    data.update(
        {
            "skaters_urls": rels.get("people", []),
            "videos_urls": rels.get("videos", []),
            "similar_companies_urls": rels.get("brands", []),
        }
    )
    yield CompanyItem(**data)


def parse_people_page(response):
    """Parse a library people page.

    http://skately.com/library/people/mark-gonzales

    :param response:
    :return: SkaterItem
    """
    response.selector.remove_namespaces()
    data = {
        "name": response.css("#lib-page-bio > h1::text").extract_first(),
        "image": response.css(
            "meta[property='og:image']::attr(content)"
        ).extract_first(),
        "bio": response.css("meta[name='description']::attr(content)").extract_first(),
        "source_url": response.url,
    }
    labels = response.css("#lib-page-bio > ul > li > strong::text").extract()
    values = response.css("#lib-page-bio > ul > li::text").extract()

    for label, value in zip(labels, values):
        with suppress(AttributeError):
            if label == "Born:":
                data["year_of_birth"] = re.search("\d{4}", value).group(0)
            elif label == "Stance:":
                data["stance"] = value.strip()
            elif label == "Hometown:":
                data["city"] = value.strip()

    yield SkaterItem(**data)


def parse_clips(clips, video_url):
    return [
        ClipItem(
            {
                "skaters": [
                    SkaterItem(
                        {
                            "name": skater["name"],
                            "image": f"{ARCHIVE_BASE_URL}http://skately.com/{skater['image']}",
                            "source_url": f"{ARCHIVE_BASE_URL}http://skately.com/{skater['permalink']}",
                        }
                    )
                    for skater in clip.get("people", [])
                ],
                "tracks": [
                    TrackItem(
                        {
                            "name": song["song_title"],
                            "artist": song["song_artist"],
                            "links": {"itunes": song["song_itunes_url"]},
                        }
                    )
                    for song in clip.get("songs", [])
                ],
                "video_url": video_url,
                "sort": index,
            }
        )
        for index, clip in enumerate(clips)
    ]


def parse_video_page(response):
    """Parse a library video page.

    http://skately.com/library/videos/blockhead-skateboards-recycled-rubbish.

    :param response: Scrapy response
    :return: VideoItem
    """
    response.selector.remove_namespaces()
    rel_links = response.css("#lib-meta > ul > li > a::attr(href)")
    rels = parse_relations(rel_links)
    # Video page contains a videoclip_data JS variable with all the soundtrack information
    scripts = response.css("script").getall() or []
    scripts_text = "".join(scripts)
    pattern = re.compile(r"videoclip_data=(\{.*?\});", flags=re.DOTALL)
    clip_data = json.loads((pattern.findall(scripts_text) or [{}])[0]).values()

    if not clip_data and (soundtrack_link := _first(rels["soundtracks"])):
        yield response.follow(soundtrack_link, parse_soundtrack_page)

    skaters_urls = response.css("#tag-people > li a::attr(href)").extract()
    filmmakers_urls = rels["people"]

    data = {
        "title": response.css("#lib-page-bio > h1::text").extract_first(),
        "description": response.css(
            "#lib-page-bio > p.description::text"
        ).extract_first(),
        "image": response.css(
            "#lib-info > div.entity.ui-corner-all > a::attr(href)"
        ).extract_first(),
        "runtime": parse_integer(
            response.css("#lib-meta > ul > li:nth-child(3)::text").extract_first()
        ),
        "year": parse_integer(
            response.css("#lib-meta > ul > li:nth-child(4)::text").extract_first()
        ),
        "company_url": _first(rels.get("brands", [])),
        "skaters_urls": skaters_urls,
        "filmmakers_urls": filmmakers_urls,
        "source_url": response.url,
    }

    data["raw_data"] = {**data}
    clip_items = parse_clips(clip_data, response.url)

    for item in (VideoItem(**data), *clip_items):
        yield item


def parse_soundtrack_page(response):
    """Parse video soundtrack.

    :return: instance of :class:`SoundtrackItem`
    """
    songs_list = []
    songs = response.css(
        "#col-left > div.lib-soundtrack > ul > li > div.song-list > p.song-info"
    )
    name = response.css("#lib-page-bio > h1::text").extract_first().strip()
    video_link = _first(
        parse_relations(
            response.css("#lib-page-bio > p > a::attr(href)"), resources=["videos"]
        )["videos"]
    )

    songs_list = []
    for song in songs:
        name = ""
        artist = ""
        song_inf = song.css("a::text").extract_first()
        if song_inf and "-" in song_inf:
            name, artist = song_inf.split("-")

        songs_list.append(
            {
                "name": name,
                "artist": artist,
                "links": [song.css("a::attr(href)").extract_first()],
            }
        )

    tracks = [TrackItem(**song) for song in songs_list]

    yield SoundtrackItem(name=name, video=video_link, tracks=tracks)


class PeopleSpider(SkatelySpider):
    """Parse Skately people library."""

    name = "skately-people"
    resource = "people"
    pages = range(2, 54)

    def parse_page(self, response):
        return parse_people_page(response)


class SpotSpider(SkatelySpider):
    """Parse Skately spot library.

    https://web.archive.org/web/20170619231904/http://skately.com/library/spots/7th-street-elementary-school
    """

    name = "skately-spots"
    resource = "spots"
    pages = range(2, 5)

    def parse_page(self, response):
        return parse_spot_page(response)


class BrandSpider(SkatelySpider):
    """Parse archived Skately brand library.

    https://web.archive.org/web/20190715034702/http://skately.com/library/brands/blind-skateboards
    """

    name = "skately-brands"
    resource = "brands"

    def parse_page(self, response):
        return parse_brand_page(response)


class VideoSpider(SkatelySpider):
    """Parse Skately video library."""

    name = "skately-videos"
    resource = "videos"
    LIMIT = 1

    def parse_page(self, response):
        return parse_video_page(response)
