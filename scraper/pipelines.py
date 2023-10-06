import logging
import traceback

logger = logging.getLogger(__name__)


class DataBasePipeline:
    def process_item(self, item, spider):
        if not item.is_valid():
            logger.warning(item.errors)
        try:
            item.save()
        except Exception as exc:
            logger.error("Error saving item")
            traceback.print_exception(exc)
        else:
            logger.info(
                "\n\n\nhttp://localhost:9000/api/v1/%s/%s",
                item.resource,
                item.instance.pk,
            )
        return item
