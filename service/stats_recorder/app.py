import click
from flask import Flask
import logging
from waitress import serve
from service.common.setup_log import setup_log

app = Flask(__name__)
logger = logging.getLogger(__name__)


def setup_blueprints():
    from service.stats_recorder.stats_routes import stats_routes
    app.register_blueprint(stats_routes)


@click.command()
@click.option('--debug', default=True, help='Run in debug mode.')
@click.option('--port', default=5001, help='The server port.')
@click.option('--host', default='0.0.0.0', help='The server host.')
def run_app(debug: bool, port: int, host: str):
    if debug:
        setup_log(enable_json_logging=False)
        setup_blueprints()
        app.run(host=host, port=port, debug=debug)
    else:
        setup_log(enable_json_logging=True)
        setup_blueprints()
        serve(app, host=host, port=port)


if __name__ == '__main__':
    run_app()
