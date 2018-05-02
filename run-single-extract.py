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

r = api.single_extract(
    verbatim='Hello World, how have you been? Not seen you since a long time!',
    lang='en',
    extractors=[
        extractors.NGram(n=3, name='ngram_custom'),
        extractors.HashTag(),
        extractors.Mention()
    ]
)

print(r)
pprint(r.data)
