import logging

from flask import Blueprint, current_app, jsonify
from service.common.stats_recorder_client import ApiClient
from service.celery_worker.tasks import api_client_task

task_routes = Blueprint('task_blueprint', __name__)

logger = logging.getLogger(__name__)


@task_routes.route('/task/eager', defaults={'number_of_request': 2}, methods=['GET'])
@task_routes.route('/task/eager/<number_of_request>', methods=['GET'])
def run_workers_eager(number_of_request):
    if number_of_request:
        number_of_request = int(number_of_request)

    api_client = ApiClient(host=current_app.config['STATS_HOST'], port=current_app.config['STATS_PORT'])
    for i in range(0, number_of_request):
        api_client.call(title='hey')

    return jsonify({'status': 'success'}), 200


@task_routes.route('/task', defaults={'number_of_request': 2}, methods=['GET'])
@task_routes.route('/task/<number_of_request>', methods=['GET'])
def run_workers(number_of_request):
    if number_of_request:
        number_of_request = int(number_of_request)

    for i in range(0, number_of_request):
        api_client_task.delay(host=current_app.config['STATS_HOST'], port=current_app.config['STATS_PORT'], title='hey')

    return jsonify({'status': 'success'}), 200


@task_routes.route('/task/status', methods=['GET'])
def get_status():
    return {'bar': 'foobar'}, 200
