import json
import logging
import time
from typing import OrderedDict
import logging.config

from pythonjsonlogger import jsonlogger


class UTCFormatter(logging.Formatter):
    converter = time.gmtime
    default_msec_format = "%s.%03d"


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
                         *args, **kwargs)


DEFAULT_LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "utc": {
            "()": UTCFormatter,
            "format": "%(asctime)sZ %(levelname)s [%(name)s:%(funcName)s:%(lineno)s] %(message)s",
        },
        "json": {
            "format": "%(asctime)sZ %(levelname)s [%(name)s:%(funcName)s:%(lineno)s] %(message)s",
            "()": SpecialJsonFormatter
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "utc",
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"handlers": ["stdout"], "level": "INFO"},
    "loggers": {
        "geventwebsocket.handler": {"level": "WARN"},
        "waitress.handler": {"level": "WARN"},
        "celery": {"level": "WARN"},
        "celery.task": {"level": "WARN"},
        "celery.worker": {"level": "WARN"}
    },
}


def setup_log(enable_json_logging: bool = True, debug: bool = True):
    conf = DEFAULT_LOG_CONFIG
    if debug:
        conf["root"]["level"] = "DEBUG"
        conf["loggers"]["geventwebsocket.handler"]["level"] = "DEBUG"
        conf["loggers"]["waitress.handler"]["level"] = "DEBUG"
        conf["loggers"]["celery"]["level"] = "DEBUG"
        conf["loggers"]["celery.task"]["level"] = "DEBUG"
        conf["loggers"]["celery.worker"]["level"] = "DEBUG"
        logger = logging.getLogger('waitress')
        logger.setLevel(logging.DEBUG)

    if enable_json_logging:
        conf["handlers"]["stdout"]["formatter"] = "json"

    logging.config.dictConfig(conf)
