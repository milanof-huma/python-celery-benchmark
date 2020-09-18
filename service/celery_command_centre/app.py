import click
from flask import Flask
import logging
from waitress import serve

from service.common.celery_setup import setup_celery_app
from service.common.setup_log import setup_log

app = Flask(__name__)
logger = logging.getLogger(__name__)


def setup_blueprints():
    from service.celery_command_centre.task_routes import task_routes
    app.register_blueprint(task_routes)


@click.command()
@click.option('--debug/--no-debug', default=True, help='Run in debug mode.')
@click.option('--json-log/--normal-log', default=False, help='Generate JSON log.')
@click.option('--host', default='0.0.0.0', help='The server host.')
@click.option('--port', default=5000, help='The server port.')
@click.option('--stats-host', default='https://app.phoenixsvc.io', help='The stats recorder host.')
@click.option('--stats-port', default=5001, help='The stats recorder port.')
@click.option('--redis-uri', default='redis://:redispassword@localhost:6333/0', help='Redis broker URI.')
def run_app(debug: bool, json_log: bool, host: str, port: int, stats_host: str, stats_port: int, redis_uri: str):
    app.config['STATS_HOST'] = stats_host
    app.config['STATS_PORT'] = stats_port

    if debug:
        setup_log(enable_json_logging=json_log)
        setup_celery_app(redis_uri)
        setup_blueprints()
        app.run(host=host, port=port, debug=debug)
    else:
        setup_log(enable_json_logging=json_log)
        setup_celery_app(redis_uri)
        setup_blueprints()
        serve(app, host=host, port=port)


if __name__ == '__main__':
    run_app()
