from celery import Celery
import celery.signals

celery_app = None


def setup_celery_app(redis_uri: str):
    global celery_app
    celery_app = Celery('benchmark', broker=redis_uri)


@celery.signals.setup_logging.connect
def on_setup_logging(**kwargs):
    pass
