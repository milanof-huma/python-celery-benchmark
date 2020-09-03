from celery import Celery

celery_app = None


def setup_celery_app(redis_uri: str):
    global celery_app
    celery_app = Celery('benchmark', broker=redis_uri)
