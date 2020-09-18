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
@click.option('--debug/--no-debug', default=True, help='Run in debug mode.')
@click.option('--json-log/--normal-log', default=False, help='Generate JSON log.')
@click.option('--redis-uri', default='redis://:redispassword@localhost:6333/0', help='Redis broker URI.')
def run_app(debug: bool, redis_uri: str, json_log: bool = True):
    setup_log(debug=debug, enable_json_logging=json_log)

    setup_celery_app(redis_uri)
    register_tasks()

    args = []
    if debug:
        args.append("--loglevel=DEBUG")
    else:
        args.append("--loglevel=INFO")
    args.append("-c")
    args.append("24")
    args.append("-P")
    args.append("threads")
    from service.common.celery_setup import celery_app
    celery_app.worker_main(args)


if __name__ == '__main__':
    run_app()
