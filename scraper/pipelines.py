import traceback
import logging

logger = logging.getLogger(__name__)


class DataBasePipeline(object):
    def process_item(self, item, spider):
        if not item.is_valid():
            logger.warning(item.errors)
            return item
        try:
            item.save()
        except Exception as exc:
            logger.error("Error saving item")
            traceback.print_exception(exc)

        return item
