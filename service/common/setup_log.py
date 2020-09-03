import json
import logging
from typing import OrderedDict

from pythonjsonlogger import jsonlogger


def setup_log(enable_json_logging: bool = True):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    def json_translate(*args, **kwargs):
        if len(args) > 0:
            if isinstance(args[0], OrderedDict):
                level_name = args[0].get("levelname", None)
                args[0]["level"] = level_name
                args[0]["severity"] = level_name
        return json.dumps(*args, **kwargs)

    class SpecialJsonFormatter(jsonlogger.JsonFormatter):

        def __init__(self, *args, **kwargs):
            super().__init__(json_serializer=json_translate, json_encoder=json.JSONEncoder,
                             fmt="%(asctime)sZ %(levelname)s [%(name)s:%(funcName)s:%(lineno)s] %(message)s", *args,
                             **kwargs)

    if enable_json_logging:
        log_handler = logging.StreamHandler()
        formatter = SpecialJsonFormatter()
        log_handler.setFormatter(formatter)
        logger.handlers = []
        logger.addHandler(log_handler)
