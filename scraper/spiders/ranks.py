import scrapy

from scraper.items import RankItem


class RankSpider(scrapy.Spider):
    allowed_domains = ["https://theboardr.com/"]
    disciplines = {
        "1": "Street",
        "2": "Park Terrain",
        "3": "Vert Bowl",
        "4": "Big Air",
    }

    def start_requests(self):
        urls = [
            'https://theboardr.com/globalrank',
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
