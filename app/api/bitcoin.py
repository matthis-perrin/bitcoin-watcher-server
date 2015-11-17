from app.api.core.utils import api
from app.exception import MyBitsException
from pycoin.key import Key
from pycoin.encoding import EncodingError

@api()
def generate(context, request, api_version,
             xpub=None, start=0, count=1):
    if not xpub:
        raise MyBitsException('Parameter `xpub` missing')

    start = int(start)
    count = int(count)

    if not 0 < count <= 20:
        raise MyBitsException('Parameter `count` must be between 1 and 20')

    try:
        mpk = Key.from_text(xpub)
    except EncodingError:
        raise MyBitsException('Invalid `xpub`')

    return [str(key.address()) for key in mpk.children(max_level=count-1, start_index=start, include_hardened=False)]
