from functools import lru_cache

from scrapy.spiders import XMLFeedSpider
from scraper.items import RSSFeedItem, RSSParsedItem, RSSItemLoader


class RSSSpider(XMLFeedSpider):
    name = 'rss'
    start_urls = [
        'https://www.skatevideosite.com/feed/',
        'https://skateboarding.transworld.net/news/feed',
    ]
    iterator = 'iternodes'
    itertag = 'item'

    @lru_cache
    def feed(self, response):
        loader = RSSItemLoader(RSSFeedItem(), response.selector)
        loader.add_xpath('title', './channel/title/text()')
        loader.add_xpath('link', './channel/link/text()')
        loader.add_xpath('language', './channel/language/text()')
        loader.add_xpath('description', './channel/description/text()')
        loader.add_xpath('image', './channel/image/url/text()')
        loader.add_value('feed_url', response.url)
        item = loader.load_item()
        return item.django_model.objects.get_or_create(**item)



    def parse_node(self, response, node):
        node.remove_namespaces()
        feed, _  = self.feed(response)
        loader = RSSItemLoader(RSSParsedItem(), node)
        loader.add_xpath('title', './title/text()')
        loader.add_xpath('link', './link/text()')
        loader.add_xpath('description', './description/text()')
        loader.add_xpath('published_at', './pubDate/text()')
        loader.add_xpath('categories', './category/text()')
        loader.add_value('feed', feed)

        yield loader.load_item()
