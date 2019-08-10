# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback


class DataBasePipeline(object):
    def process_item(self, item, spider):
        item.process()
        try:
            item.save()
        except Exception as exc:
            traceback.print_exception(exc)
            print(item, "not saved")
            pass

        return item
