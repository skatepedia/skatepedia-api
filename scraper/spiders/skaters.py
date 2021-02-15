import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scraper.items import SkaterItem


class SkaterSpider(CrawlSpider):
    name = 'skaters'
    start_urls = ['https://theboardr.com/skaters']
    rules = (
        Rule(LinkExtractor(allow=("profile/\d+/\w+")), callback='parse_item'),
    )

    def parse_item(self, response):
        script_data = response.css("#__NEXT_DATA__::text")[0]
        data = json.loads(script_data.extract())
        skater_info = data['props']['pageProps']['skaterDetails'][0]

        yield SkaterItem({
            "name": f"{skater_info['FirstName']} {skater_info['LastName']}",
            "age": skater_info.get('Age'),
            "image": skater_info.get('Mug'),
            "style": skater_info.get('Stance'),
            "country": skater_info.get('CountryCode', '').lower(),
            "external_uuid": response.request.url
        })
