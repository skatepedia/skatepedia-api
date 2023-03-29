import json
import datetime

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from scraper.items import SkaterItem


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
