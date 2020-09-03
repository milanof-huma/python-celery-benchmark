import click
import logging

from service.common.celery_setup import setup_celery_app
from service.common.setup_log import setup_log

logger = logging.getLogger(__name__)


def register_tasks():
    from service.celery_worker.tasks import api_client_task
    from service.common.celery_setup import celery_app
    celery_app.register_task(api_client_task)


@click.command()
@click.option('--debug', default=True, help='Run in debug mode.')
@click.option('--redis-uri', default='redis://:redispassword@localhost:6333/0', help='Redis broker URI.')
def run_app(debug: bool, redis_uri: str):
    setup_log(enable_json_logging=False)

    setup_celery_app(redis_uri)
    register_tasks()

    args = []
    if debug:
        args.append("--loglevel=DEBUG")
        args.append("-E")
    args.append("-P")
    args.append("solo")
    from service.common.celery_setup import celery_app
    celery_app.worker_main(args)


if __name__ == '__main__':
    run_app()
