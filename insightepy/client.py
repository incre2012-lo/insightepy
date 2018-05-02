# -*- coding: utf-8 -*-
import json
import traceback
from typing import Dict, List

from urllib3 import HTTPConnectionPool

from insightepy import conf
from insightepy.core import Logger
from insightepy.extractors import Extractor
from insightepy.response import Response

HOST_ADDR = conf.config.get('server', 'host')
HOST_PORT = conf.config.get('server', 'port')
ROUTE_PREFIX = conf.config.get('server', 'route_prefix')

logger = Logger('InsightePy')


class API(object):
    def __init__(self, client_id: str, client_secret: str, auth_token: str) -> None:
        self.print_hello_message()
        self._cid = client_id
        self._csecret = client_secret
        self._auth_token = auth_token
        self.pool = HTTPConnectionPool(HOST_ADDR + ':' + HOST_PORT, timeout=600)

    @staticmethod
    def print_hello_message():
        logger.info('--------------------------------')
        logger.info('----- Hello from InsightePy ----')
        logger.info('--------------------------------')

    def make_request(self, method: str, url: str, fields: Dict[str, str]) -> Response:
        # adding user information to field
        fields['cid'] = self._cid
        fields['csecret'] = self._csecret
        fields['authtoken'] = self._auth_token
        logger.debug('Making request with: {}'.format(fields))
        r = self.pool.request(method, ROUTE_PREFIX + url, fields=fields)
        print(r.status)
        """
        response : accepted 
        run till r.status =200 
        """
        if r.status == 200:
            logger.debug('Got raw response:  {}'.format(r.data))
            try:
                response = Response(json.loads(r.data))
                logger.debug('Built Response: {}'.format(response.__repr__()))
                return response
            except Exception as e:
                logger.error('Encountered error while parsing response: {}'.format(str(e)))
                logger.error(traceback.format_exc())
        else:
            logger.error('Got a NOT OK Response Code: status={}'.format(r.status))
            logger.error(traceback.format_exc())

    def say_hello(self):
        logger.info('Running Say Hello')
        return self.make_request(
            'GET',
            '/hello',
            dict()
        )

    def single_extract(self, verbatim: str, lang: str, extractors: List[Extractor] = None) -> Response:
        """
        Extract insight for a single verbatim
        :param lang: language of the sentence {en/fr/de}
        :param verbatim: Unicode sentence
        :param extractors: list of feature extractors
        :return: dict response from Compute Engine
        """
        logger.info('Running Single Extract on: {}'.format(verbatim))
        return self.make_request(
            'GET',
            '/extract',
            dict(
                verbatim=verbatim,
                lang=lang,
                extractors=json.dumps([_.to_dict() for _ in extractors] if extractors else [])
            )
        )

    def multi_extract(self, lang: str,S3BucketName :str,S3AccessKey: str,S3AccessSecret: str,S3FileLoc:str, extractors: List[Extractor] = None) -> Response:
        """
        Extract insight for a single verbatim
        :param lang: language of the sentence {en/fr/de}
        :param verbatim: Unicode sentence
        :param extractors: list of feature extractors
        :return: dict response from Compute Engine
        """
        #logger.info('Running Multi Extract on: {}'.format(verbatim))
        return self.make_request(
            'GET',
            '/multiextract',
            dict(
               # verbatim=verbatim,
                lang=lang,
                S3BucketName=S3BucketName,
                S3AccessKey=S3AccessKey,
                S3AccessSecret=S3AccessSecret,
                S3FileLoc=S3FileLoc,
                extractors=json.dumps([_.to_dict() for _ in extractors] if extractors else [])
            )
        )