import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

from pprint import pprint

from insightepy import API
from insightepy import extractors

test_client = 'test-client'

api = API(
    client_id=test_client,
    client_secret=test_client,
    auth_token=test_client,
)

# r = api.say_hello()
# print(r)

r = api.multi_extract(
    lang='en',
    S3BucketName='dev.insighte',
    S3AccessKey='AKIAIK5FMFE3SH73RBWA',
    S3AccessSecret='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',
    S3FileLoc='1512493847451|140ed9df-474a-46c0-b7f1-77ce189ad953.verbatim',
    extractors=[
        extractors.NGram(n=3, name='ngram_custom'),
        extractors.HashTag(),
        extractors.Mention()
    ]
)

pprint(r)
# pprint(r.data)
