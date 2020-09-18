import logging

from service.common.celery_setup import celery_app
from service.common.stats_recorder_client import ApiClient

logger = logging.getLogger(__name__)


@celery_app.task()
def api_client_task(host: str, port: int, title: str, body: str = None):
    api_client = ApiClient(host=host, port=port)
    api_client.call(title=title, body=body)

    logger.debug("test")
