import scrapy

from scraper.items import (
    VideoItem,
    SoundtrackItem,
    TrackItem,
    ClipItem
)
from scraper.utils import parse_integer


SKATELY_VIDEO_LIBRARY_URL = "http://skately.com/library/videos"


class VideoSpider(scrapy.Spider):
    """Parse Skately video library and extract movies information."""
    name = "skately"
    LIMIT = 1

    def start_requests(self):
        urls = [SKATELY_VIDEO_LIBRARY_URL] + [
            "http://skately.com/library/videos/page-%s" %(x) for x in range(2,9)
        ]
        for url in urls[:self.LIMIT]:
            yield scrapy.Request(url, self.parse)

    def parse_clips(self, response):
        """Parse video clips with media_url

        :return: list of ``ClipItem`` video clips.
        """
        clips_list = []
        clips_selector = response.css("#video-clips > ul > li")

        for selector in clips_selector:
            url = "https://www.youtube.com/watch?v={}".format(
                selector.css("input::attr(value)").extract()[1]
            )
            clips_list.append(ClipItem(**{
                "name": selector.css("a > p").extract_first(),
                "thumbnail": selector.css("a > img::attr(src)").extract_first(),
                "url": url,
            }))

        return clips_list

    def parse_video_page(self, response):
        """Parse a library video page.

        http://skately.com/library/videos/blockhead-skateboards-recycled-rubbish.

        :param response:
        :return: VideoItem
        """
        response.selector.remove_namespaces()
        brand_link = response.css("#lib-meta > ul > li:nth-child(1) > a::attr(href)").extract_first()
        director_link = response.css("#lib-meta > ul > li:nth-child(2) > a::attr(href)").extract_first()
        soundtrack_link = response.css("#lib-meta > ul > li:nth-child(5) > a::attr(href)").extract_first()

        yield response.follow(soundtrack_link, self.parse_soundtrack_page)

        video_clips = self.parse_clips(response)

        video_data = {
            "name": response.css("#lib-page-bio > h1::text").extract_first(),
            "description": response.css("#lib-page-bio > p.description::text").extract_first(),
            "image": response.css("#lib-info > div.entity.ui-corner-all > a::attr(href)").extract_first(),
            "brand": brand_link,
            "director": {
                "name": response.css("#lib-meta > ul > li:nth-child(2) > a::text").extract_first(),
                "url": director_link
            },
            "runtime": parse_integer(response.css("#lib-meta > ul > li:nth-child(3)::text").extract_first()),
            "year": parse_integer(response.css("#lib-meta > ul > li:nth-child(4)::text").extract_first()),
            "soundtrack": soundtrack_link,
            "clips": video_clips,
            "external_url": response.url,
        }
        yield VideoItem(**video_data)

    def parse_soundtrack_page(self, response):
        """Parse video soundtrack.

        :return: instance of :class:`SoundtrackItem`
        """
        songs_list = []
        songs = response.css("#col-left > div.lib-soundtrack > ul > li > div.song-list > p.song-info")
        video_link = response.css("#lib-page-bio > p:nth-child(4) > a::attr(href)").extract_first()
        for song in songs:
            name = ''
            artist = ''
            song_inf = song.css("a::text").extract_first()
            if song_inf and '-' in song_inf:
                name, artist = song_inf.split("-")

            songs_list.append({
                "name": name,
                "artist": artist,
                "itunes_url": song.css("a::attr(href)").extract_first(),
            })

        tracks = [TrackItem(**song) for song in songs_list]

        yield SoundtrackItem(
            video=video_link,
            tracks=tracks
        )

    def parse(self, response):
        videos = set(response.css("#lib-list > ul > li > div > a::attr(href)").extract())
        for video_url in list(videos)[:self.LIMIT]:
            yield scrapy.Request(video_url, self.parse_video_page)
