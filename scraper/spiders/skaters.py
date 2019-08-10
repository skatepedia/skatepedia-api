import string

import scrapy

from scraper.items import SkaterItem, SkaterItemLoader


class SkaterSpider(scrapy.Spider):
    name = "skaters"
    profile_selector = {
        "name": "body > div.site-wrap > div.middle-wrapper > div > div.row.well > div:nth-child(2) > h1::text",
        "country": "body > div.site-wrap > div.middle-wrapper > div > div.row.well > div:nth-child(2) > p > a:nth-child(2)::text",
        "bio": "body > div.site-wrap > div.middle-wrapper > div > div.row.well > div:nth-child(2) > p::text",
    }
    LIMIT = 1

    def start_requests(self):
        urls = [
            f"https://theboardr.com/skateboarders_list/{letter}"
            for letter in string.ascii_uppercase
        ]
        for url in urls[: self.LIMIT]:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_skater_page(self, response):
        loader = SkaterItemLoader(item=SkaterItem(), response=response)
        loader.add_css("name", self.profile_selector["name"])
        loader.add_css("bio", self.profile_selector["bio"])
        loader.add_css("age", self.profile_selector["bio"], re=r"\d+")
        loader.add_css("style", self.profile_selector["bio"], re=r"Regular|Goofy")
        loader.add_css("country", self.profile_selector["country"])
        loader.add_value("external_uuid", response.request.url)

        yield loader.load_item()

    def parse(self, response):
        profile_links = response.css(
            "#cphMain_pnlList > div > div > a::attr(href)"
        ).extract()
        for profile_link in profile_links[: self.LIMIT]:
            yield response.follow(profile_link, self.parse_skater_page)
