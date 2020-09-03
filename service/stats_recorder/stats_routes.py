import logging

from flask import Blueprint, current_app, request

stats_routes = Blueprint('stats_blueprint', __name__)

logger = logging.getLogger(__name__)


@stats_routes.route('/record', methods=['POST'])
def record_message():
    if not request.json:
        return 'Invalid Request', 400

    title = request.json['title']
    body = request.json['body']

    logger.info(f'title: {title}\nbody: {body}')

    return {'bar': 'foobar'}, 200


@stats_routes.route('/record/status', methods=['GET'])
def get_status():
    return {'bar': 'foobar'}, 200
