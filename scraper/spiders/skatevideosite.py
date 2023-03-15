import re

from scrapy import Request
from w3lib.html import remove_tags
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from scraper.items import VideoItem, VideoItemLoader


class SkateVideoSiteSpider(CrawlSpider):
    name = "skatevideosite"
    start_urls = ["https://www.skatevideosite.com"]
    rules = (
        Rule(LinkExtractor(allow=("/videos")), callback="parse_archive"),
        Rule(LinkExtractor(allow=("/videos/\w+")), callback="parse_video"),
    )

    def parse_archive(self, response):
        import ipdb

        ipdb.set_trace()
        article_urls = response.css("article.post .entry-title a::attr(href)").extract()
        for article_url in article_urls:
            yield Request(article_url, self.parse_video)

    def parse_video(self, response):
        """Parse a video page.

        :param response:
        :return: VideoItem
        """

        import ipdb

        ipdb.set_trace()

        video_info = {}
        info_mapping = {
            "Year": "year",
            "Length": "runtime",
            "Video by": "director",
            "Company": "brand",
            "Category": "category",
            "Country": "country",
        }
        info_keys = [
            remove_tags(column)
            for column in response.css(".videoinfo tr > td:nth-child(1)").extract()
        ]
        info_values = [
            remove_tags(column)
            for column in response.css(".videoinfo tr > td:nth-child(2)").extract()
        ]

        for key, value in zip(info_keys, info_values):
            video_info[info_mapping.get(key)] = value

        runtime = re.findall("\d+", video_info.get("runtime"))

        video_data = {
            "name": response.css("h1.entry-title::text").extract_first(),
            "image": response.css("img.cover::attr(src)").extract_first(),
            "director": video_info.get("director"),
            "runtime": runtime[0] if runtime else None,
            "year": video_info.get("year"),
            "brand": video_info.get("brand"),
            "category": video_info.get("category"),
            "soundtrack": remove_tags(response.css("#soundtrack").extract_first()),
            "skaters": remove_tags(response.css("#skaters").extract_first()),
            "external_uuid": response.url,
        }
        video = VideoItemLoader(item=VideoItem(**video_data))

        yield video.load_item()
