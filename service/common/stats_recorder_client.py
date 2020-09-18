import logging

import requests
from requests_toolbelt.utils import dump

from firebase_admin import messaging
from firebase_admin.messaging import AndroidConfig

logger = logging.getLogger(__name__)


class ApiClient:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def call(self, title: str = '', body: str = ''):
        try:
            rsp = requests.post(f'{self.host}:{self.port}/record', json={'title': title, 'body': body}, timeout=2)
            if rsp.status_code - 400 >= 0:
                data = dump.dump_response(rsp)
                logger.warning(data)
        except Exception as e:
            logger.warning(f"Request failed due to [{e}]")




class FirebaseAdminClient(ApiClient):

    def call(self, title: str = '', body: str = ''):

        token = "asfdjkladjfkaldjfklajdfkl2j13klj132kljkl"

        messages = []
        message = messaging.Message(
            notification=messaging.Notification(title=title,
                                                body=body),
            token=token,
            data=None,
            android=AndroidConfig(priority=10, ttl=45)
        )

        messages.append(message)

        if len(messages) == 0:
            batch_rsp = messaging.send_all(messages)
            i = 0
            failed_ids = []
            for rsp in batch_rsp.responses:
                if rsp.exception:
                    if rsp.exception.http_response.status_code in [404, 400]:
                        failed_ids.append(token)
                    else:
                        logger.warning(f"failed fcm batch send: {token}")

                i += 1
            return failed_ids
