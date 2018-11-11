import string
import random
import scrapy
from scrapy.utils.markup import remove_tags

from scraper.items import TrackItem, SoundtrackItem

class SoundtrackSpider(scrapy.Spider):
    """Parse SKATEVIDEOSITE video library and extract soundtrack information."""
    name = "soundtracks"
    LIMIT = 1

    def start_requests(self):
        urls = [f"http://www.skatevideosite.com/soundtracks/{x}"
                for x in string.ascii_lowercase]
        for url in random.sample(urls, 2)[:self.LIMIT]:
            yield scrapy.Request(url, self.parse)

    def parse_soundtrack_page(self, response):
        """Parse video soundtrack.
        http://www.skatevideosite.com/skatevideos/girl-yeah-right/soundtrack#

        :return: instance of :class:`SoundtrackItem`
        """
        response.selector.remove_namespaces()
        track_list = []
        tracks = response.xpath('//*[@id="soundtrack"]/following-sibling::table/tr/td').extract()

        for track in tracks:
            track_info = remove_tags(track).strip().split("-")
            if len(track_info) == 3:
                _, artist, song = track_info

            if len(track_info) == 2:
                artist, song = track_info
                track_list.append(TrackItem(
                    name=song,
                    artist=artist
                ))

        yield SoundtrackItem(
            name=response.css('body > div:nth-child(4) > div > div > h1::text').extract_first(),
            tracks=track_list,
            external_uuid=response.url,
        )

    def parse(self, response):
        video_links = response.css("table > tr > td:nth-child(2) > a.videotitle::attr(href)").extract()
        for video_link in video_links[:self.LIMIT]:
            yield response.follow(video_link, self.parse_soundtrack_page)
