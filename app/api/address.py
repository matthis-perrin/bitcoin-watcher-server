from app.api.core.utils import api
from app.config import Config
from app.db.user_address import UserAddress
from app.exception import MyBitsException


blockcypher_config = Config.get('blockcypher')
api_key = blockcypher_config.get('api_key')

@api(enforce_user=True)
def add(context, request, api_version, user,
        address=None):

    if not address:
        raise MyBitsException('Parameter `address` missing')

    # Store the user address in DB
    UserAddress.add(user.user_id, address, 'XPUB')
