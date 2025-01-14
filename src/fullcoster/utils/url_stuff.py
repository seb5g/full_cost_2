import urllib.parse as urlparse
from urllib.parse import parse_qs

#
# url = 'http://foo.appspot.com/abc?def=ghi'
# parsed = urlparse.urlparse(url, allow_fragments=False)
# print(parse_qs(parsed.query)['def'])
# url = 'foo.appspot.com/#/abc?def=ghi&poject=fhjk'

def get_field_from_url(url, field):
    parsed = urlparse.urlparse(url, allow_fragments=False)
    return parse_qs(parsed.query).get(field, [None])[0]