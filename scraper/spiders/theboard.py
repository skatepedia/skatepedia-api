import json
import datetime

from scrapy.spiders import Rule, Spider, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from scraper.items import RankItem, SkaterItem


class SkaterSpider(CrawlSpider):
    name = "skaters"
    start_urls = ["https://theboardr.com/skaters"]
    rules = (Rule(LinkExtractor(allow=("profile/\d+/\w+")), callback="parse_item"),)

    def parse_item(self, response):
        script_data = response.css("#__NEXT_DATA__::text")[0]
        data = json.loads(script_data.extract())
        skater_info = data["props"]["pageProps"]["skaterDetails"][0]
        year_of_birth = None
        if age := skater_info.get("Age"):
            year_of_birth = datetime.datetime.now().year - int(age)

        yield SkaterItem(
            {
                "name": f"{skater_info['FirstName']} {skater_info['LastName']}",
                "image": skater_info.get("Mug"),
                "year_of_birth": year_of_birth,
                "stance": skater_info.get("Stance"),
                "gender": skater_info.get("Gender"),
                "city": skater_info.get("City", "").lower(),
                "country": skater_info.get("CountryCode", "").lower(),
                "source_url": response.request.url,
                "raw_data": skater_info,
            }
        )


class RankSpider(Spider):
    allowed_domains = ["https://theboardr.com/"]
    disciplines = {
        "1": "Street",
        "2": "Park Terrain",
        "3": "Vert Bowl",
        "4": "Big Air",
    }

    def start_requests(self):
        urls = [
            "https://theboardr.com/globalrank",
            #     'https://theboardr.com/globalrankbrands',
            #     'https://theboardr.com/globalranksocial',
            #     'https://theboardr.com/globalranksocialyt/All'
            # ] + [f"https://theboardr.com/globalrank?discipline={x}"
            #      for x in self.disciplines
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_rank_page)

    def parse_rank_page(self, response):
        print(response.url)
        rank_positions = response.css("table > tr")
        for position in rank_positions:
            data = {
                "name": "Global Rank",
                "position": position.css("td:nth-child(1)").re(r"\d+")[0],
                "skater": position.css("td:nth-child(2) a::text").re(r"\w+ \w+")[0],
                "points": position.css("td:nth-child(4)").re(r"(\d+,\d+)")[0],
            }
            yield RankItem(**data)
