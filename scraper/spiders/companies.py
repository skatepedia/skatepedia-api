import json

import scrapy

from scraper.items import CompanyItem


class CompanySpider(scrapy.Spider):
    """Parse Skately brand library."""

    base_url = "https://web.archive.org/web/20191003042112/"  # use web archive since page is down
    name = "companies"
    pages = range(2, 9)
    LIMIT = 10000  # Limit for debugging purposes

    def start_requests(self):
        urls = [f"{self.base_url}http://skately.com/library/brands"] + [
            f"{self.base_url}http://skately.com/library/brands/page-{x}"
            for x in self.pages
        ]
        self.logger.info(f"Scarping following {urls}")

        for url in urls[: self.LIMIT]:
            yield scrapy.Request(url, self.parse)

    def parse_brand_links(self, response):
        """Extract videos, skaters, brands from brand page."""
        brand_rel_links = response.css("#col-left > ul > li > div > a::attr(href)")
        match_url = r"[\w\d:#@%/;$()~_?\+-=\\\.&]"
        brand_rel_data = {}

        for rel_type in ("videos", "brands", "people", "ads"):
            brand_rel_data[rel_type] = brand_rel_links.re(
                f"{match_url}+{rel_type}+{match_url}*"
            )

        return brand_rel_data

    def parse_brand_page(self, response):
        """Parse a library brand page.

        http://skately.com/library/brands/blockhead-skateboards-recycled-rubbish.

        :param response:
        :return: CompanyItem
        """
        response.selector.remove_namespaces()
        rels = self.parse_brand_links(response)
        data = {
            "name": response.css("#lib-page-bio > h1::text").extract_first(),
            "description": response.css("#lib-page-bio > p::text").extract_first(),
            "logo": response.css(
                "#lib-page-info > div.entity.ui-corner-all > a > img::attr(src)"
            ).extract_first(),
            "website": response.css(
                "#lib-page-bio > ul > li:nth-child(1) > a::attr(href)"
            ).extract_first(),
            "links": response.css("#lib-page-bio > ul > li > a::attr(href)").extract(),
            "raw_data": rels,
            "videos": rels["videos"],
            "skaters": rels["people"],
            "similar_companies": rels["brands"],
            "ads": rels["ads"],
            "source_url": response.url,
        }
        yield CompanyItem(**data)

    def parse(self, response):
        brands = set(
            response.css("#lib-list > ul > li > div > a::attr(href)").extract()
        )
        for brand_url in list(brands)[: self.LIMIT]:
            yield scrapy.Request(brand_url, self.parse_brand_page)
