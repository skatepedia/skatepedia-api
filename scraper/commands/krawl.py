from scrapy.commands.crawl import Command as ExistingCrawlCommand
from scrapy.exceptions import UsageError



class Command(ExistingCrawlCommand):
    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError("running 'scrapy crawl' with more than one spider is no longer supported")
        spname = args[0]

        crawl_defer = self.crawler_process.crawl(spname, **opts.spargs)

        if getattr(crawl_defer, 'result', None) is not None and issubclass(crawl_defer.result.type, Exception):
            self.exitcode = 1
        else:
            self.crawler_process.start()

            exception_count = crawl_defer.stats.get_value('downloader/exception_count')

            if exception_count:
                self.exitcode = 1

            if (
                self.crawler_process.bootstrap_failed
                or hasattr(self.crawler_process, 'has_exception') and self.crawler_process.has_exception
            ):
                self.exitcode = 1
