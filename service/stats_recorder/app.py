from os.path import abspath

import click
from flask import Flask
import logging

from service.common.gunicorn_app import number_of_workers, StandaloneApplication
from service.common.setup_log import setup_log

app = Flask(__name__)
logger = logging.getLogger(__name__)


def setup_blueprints():
    from service.stats_recorder.stats_routes import stats_routes
    app.register_blueprint(stats_routes)


@click.command()
@click.option('--debug/--no-debug', default=True, help='Run in debug mode.')
@click.option('--json-log/--normal-log', default=False, help='Generate JSON log.')
@click.option('--http/--https', default=True, help='Run in http/https mode.')
@click.option('--port', default=5001, help='The server port.')
@click.option('--host', default='0.0.0.0', help='The server host.')
def run_app(debug: bool, json_log: bool, http: bool, port: int, host: str):
    if debug:
        setup_log(enable_json_logging=json_log)
        setup_blueprints()
        app.run(host=host, port=port, debug=debug)
    else:
        setup_log(enable_json_logging=json_log)
        setup_blueprints()
        options = {
            'bind': f'{host}:{port}',
            'workers': number_of_workers(debug=debug),
            'pidfile': None,
        }
        if not http:
            options['certfile'] = abspath(__file__ + '/../../../.secret/star_phoenixsvc_io_cabundle.pem')
            options['keyfile'] = abspath(__file__ + '/../../../.secret/star_phoenixsvc_io_privatekey.pem')
            logger.info('Running in https mode')
        StandaloneApplication(app, options).run()


if __name__ == '__main__':
    run_app()
